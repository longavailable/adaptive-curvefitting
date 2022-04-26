#curve fitting module -- mini-modified scipy.optimize.curve_fit

import numpy as np
from scipy.optimize import least_squares
from scipy.optimize._lsq.least_squares import prepare_bounds
from scipy.optimize._minpack_py import _wrap_func, _initialize_feasible
from scipy.linalg import svd

def curve_fit_m(f, xdata, ydata, p0=None, sigma=None, absolute_sigma=False,
              check_finite=True, bounds=(-np.inf, np.inf), method=None,
              jac=None, **kwargs):
	"""
	Instruction and source of `scipy.optimize.curve_fit` can be found in 
	https://github.com/scipy/scipy/blob/adc4f4f7bab120ccfab9383aba272954a0a12fb0/scipy/optimize/minpack.py#L511-L813
	"""
	if p0 is None:
		# determine number of parameters by inspecting the function
		from ._helpers import funcArgsNr
		n = funcArgsNr(f)-1 #except independent variable
		if n < 1:
				raise ValueError("Unable to determine number of fit parameters.")
	else:
		p0 = np.atleast_1d(p0)
		n = p0.size

	lb, ub = prepare_bounds(bounds, n)
	if p0 is None:
		p0 = _initialize_feasible(lb, ub)
	
	bounded_problem = np.any((lb > -np.inf) | (ub < np.inf))
	if method is None:
		if bounded_problem:
				method = 'trf'
		else:
				method = 'lm'

	if method == 'lm' and bounded_problem:
		raise ValueError("Method 'lm' only works for unconstrained problems. "
											"Use 'trf' or 'dogbox' instead.")

	# optimization may produce garbage for float32 inputs, cast them to float64

	# NaNs can not be handled
	if check_finite:
		ydata = np.asarray_chkfinite(ydata, float)
	else:
		ydata = np.asarray(ydata, float)

	if isinstance(xdata, (list, tuple, np.ndarray)):
		# `xdata` is passed straight to the user-defined `f`, so allow
		# non-array_like `xdata`.
		if check_finite:
				xdata = np.asarray_chkfinite(xdata, float)
		else:
				xdata = np.asarray(xdata, float)

	if ydata.size == 0:
		raise ValueError("`ydata` must not be empty!")

	# Determine type of sigma
	if sigma is not None:
		sigma = np.asarray(sigma)

		# if 1-d, sigma are errors, define transform = 1/sigma
		if sigma.shape == (ydata.size, ):
				transform = 1.0 / sigma
		# if 2-d, sigma is the covariance matrix,
		# define transform = L such that L L^T = C
		elif sigma.shape == (ydata.size, ydata.size):
			try:
				# scipy.linalg.cholesky requires lower=True to return L L^T = A
				transform = cholesky(sigma, lower=True)
			except LinAlgError:
				raise ValueError("`sigma` must be positive definite.")
		else:
			raise ValueError("`sigma` has incorrect shape.")
	else:
			transform = None

	func = _wrap_func(f, xdata, ydata, transform)
	if callable(jac):
		jac = _wrap_jac(jac, xdata, transform)
	elif jac is None and method != 'lm':
		jac = '2-point'

	if 'args' in kwargs:
		# The specification for the model function `f` does not support
		# additional arguments. Refer to the `curve_fit` docstring for
		# acceptable call signatures of `f`.
		raise ValueError("'args' is not a supported keyword argument.")

	#print(method)
	if method == 'lm':
		# Remove full_output from kwargs, otherwise we're passing it in twice.
		return_full = kwargs.pop('full_output', False)
		res = leastsq(func, p0, Dfun=jac, full_output=1, **kwargs)
		popt, pcov, infodict, errmsg, ier = res
		ysize = len(infodict['fvec'])
		cost = np.sum(infodict['fvec'] ** 2)
		if ier not in [1, 2, 3, 4]:
			raise RuntimeError("Optimal parameters not found: " + errmsg)
	else:
		# Rename maxfev (leastsq) to max_nfev (least_squares), if specified.
		if 'max_nfev' not in kwargs:
			kwargs['max_nfev'] = kwargs.pop('maxfev', None)

		res = least_squares(func, p0, jac=jac, bounds=bounds, method=method, **kwargs)

		if not res.success:
				raise RuntimeError("Optimal parameters not found: " + res.message)

		ysize = len(res.fun)
		cost = 2 * res.cost  # res.cost is half sum of squares!
		popt = res.x

		# Do Moore-Penrose inverse discarding zero singular values.
		_, s, VT = svd(res.jac, full_matrices=False)
		threshold = np.finfo(float).eps * max(res.jac.shape) * s[0]
		s = s[s > threshold]
		VT = VT[:s.size]
		pcov = np.dot(VT.T / s**2, VT)
		return_full = False

	warn_cov = False
	if pcov is None:
		# indeterminate covariance
		pcov = zeros((len(popt), len(popt)), dtype=float)
		pcov.fill(inf)
		warn_cov = True
	elif not absolute_sigma:
		if ysize > p0.size:
			s_sq = cost / (ysize - p0.size)
			pcov = pcov * s_sq
		else:
			pcov.fill(inf)
			warn_cov = True

	if warn_cov:
		warnings.warn('Covariance of the parameters could not be estimated', category=OptimizeWarning)
	
	#add `cost` output
	if return_full:
		return popt, pcov, cost, infodict, errmsg, ier
	else:
		return popt, pcov, cost
