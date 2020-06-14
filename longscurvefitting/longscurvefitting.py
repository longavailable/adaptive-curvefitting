import numpy as np
import pathlib
import time

from .scipycurvefitm import curve_fit_m
from .models import *
from .models import __custom
from ._helpers import ( curve_fit_plot,
												writeLogsDicts2csv,
												funcArgs,
												funcArgsNr )

def funcParasExpr(functions, operator='+'):
	'''Generate the expression of mixed function.
	
	Parameters:
		functions: basic models(name of models) to concatenate/mix.
			Type: list of string
		operator: arithmetic operation between basic models. If it's assined as 'piecewise', then compose a 2-piecewise function by basic models.
			Type: string
			Default: '+'
	returns:
		mixed_function: mixed function expression
			Type: string
		mixed_parameters: joined parameters for mixed_function, except independent variable `x`
			Type: string
	'''
	functions_expr = []
	parameters_expr = []
	if 'PIECEWISE' not in operator.upper():
		'''
		Basic models are added to form a new model. For example,
		
		#model-0
		def gaussian_erf(x, a1, b1, c1, a2, b2, c2):
			return gaussian(x, a1, b1, c1) + gaussian_erf(x, a2, b2, c2)
		'''
		for i, function in enumerate(functions):
			model = next(m for m in basicModels if m['name'] == function)
			parameters = ['p%d_%d' % (i, j) for j in range(model['n_para'])]
			para_expr = ', '.join(parameters)
			function_expr = '%s(x, %s)' % (function, para_expr)
			functions_expr.append(function_expr)
			parameters_expr.append(para_expr)
		mixed_function = (' %s ' % operator).join(functions_expr)
		mixed_parameters = ','.join(parameters_expr)
		return mixed_function, mixed_parameters
	else:                                                                                           
		'''
		#only for 2-piecewise function
		#an example of custom piecewise function
		
		#model-1 --primary
		#This piecewise model is uninterrupted anywhere, so it won't take effect to constant-contant pair.
		def piecewise_%s(x, x0, y0, a1, b1, c1, a2, b2):
			return np.piecewise(x, [x < x0], [lambda x: gaussian(x, a1, b1, c1) + y0 - gaussian(x0, a1, b1, c1), lambda x: linear(x, a2, b2) + y0 - linear(x0, a2, b2)])
		
		#model-2
		#This model is more common piecewise model.  Due to simplity, it's too easy to fall into a local optimal.
		def piecewise_%s(x, x0, a1, b1, c1, a2, b2):
			return np.piecewise(x, [x < x0], [lambda x: gaussian(x, a1, b1, c1), lambda x: linear(x, a2, b2)])
		'''
		modelcode = 'm-2'	if functions[0] == functions[1] == 'constant' else 'm-1'
		if len(functions) == 2:
			for i, function in enumerate(functions):
				model = next(m for m in basicModels if m['name'] == function)
				parameters = ['p%d_%d' % (i, j) for j in range(model['n_para'])]
				para_expr = ', '.join(parameters)
				if modelcode == 'm-1':
					function_expr = 'lambda x: %s(x, %s) + y0 - %s(x0, %s)' % (function, para_expr, function, para_expr)
				elif modelcode == 'm-2':
					function_expr = 'lambda x: %s(x, %s)' % (function, para_expr)
				functions_expr.append(function_expr)
				parameters_expr.append(para_expr)
			
			if modelcode == 'm-1':
				mixed_parameters = 'x0, y0,' + ','.join(parameters_expr)
			elif modelcode == 'm-2':
				mixed_parameters = 'x0,' + ','.join(parameters_expr)
			
			mixed_function = 'np.piecewise(x, [x < x0], [' + ','.join(functions_expr) + '])'
			return mixed_function, mixed_parameters

def getBounds(model, xdata, ydata):
	'''An uncomplete attemp to assign bounds to parameters.
	
	Parameters:
		model: 
			Type: function object
		xdata:
			Type: array_like or object
		ydata:
			Type: array_like or object
	Returns:
		bounds:
			Type: 2-tuple of array_like
	'''
	modelname = model.__name__
	narguments = funcArgsNr(model)-1 #except independent variable
	if modelname.startswith('piecewise'):
		index_l = max(9, int(0.05 * xdata.size))
		index_r = min(-10, -int(0.05 * xdata.size))
		x0_bound_l, x0_bound_r = np.sort(xdata)[index_l], np.sort(xdata)[index_r]
		y0_bound_l, y0_bound_r = np.sort(ydata)[index_l], np.sort(ydata)[index_r]
		bound_l = [x0_bound_l, y0_bound_l, *[-np.inf]*(narguments-2)]
		bound_r = [x0_bound_r, y0_bound_r, *[np.inf]*(narguments-2)]
		bounds = (bound_l, bound_r)
	else:
		bounds = (-np.inf, np.inf)
	return bounds
	
def generateFunction(functions, functionName=None, operator='+'):
	'''Generate or query a function / model
	
	Parameters:
		functions: if it's a function, then for the purpose of query otherwise to composite
			Type: list of string
		functionName: the name of new function
			Type: string
			Default: None
		operator: operatation between basic models.
			Type: string
			Default: '+'
	Returns:
		modelMeta: the generated model, include keys: 'model'(function object),'name','form', and 'paras_symbol'
			Type: dictionary
	'''
	if isinstance(functions, str): functions = [functions]
	
	if len(functions) == 1 and functions[0] in basicModels_nameList:
		functionName = functions[0]		#ignore argument `functionName`
		model = next(m['model'] for m in basicModels if m['name'] == functionName)
		paras_symbol = ','.join(funcArgs(model)[1:])	#string, equivalent to `mixParas`
		modelMeta = {'model':model,'name':functionName,'form':'Default','paras_symbol':paras_symbol}
		
	if len(functions) >= 2:
		if not functionName:
			prefix = 'piecewise_' if 'PIECEWISE' in operator.upper() else 'operation_'
			functionName = prefix + '_'.join(functions)
		
		mixFunc, mixParas = funcParasExpr(functions, operator=operator)
		exec(__custom % (functionName, mixParas, mixFunc))	#all were local models. Query via `locals()`
		model = locals()[functionName]	#get function object by name/string
		modelMeta = {'model':model,'name':functionName,'form':mixFunc,'paras_symbol':mixParas}
	return modelMeta

def generateModels(functions=basicModels_nameList, dataLength=0, piecewise=False, operator='+', maxCombination=2):
	'''Generate potential models.
	
	Parameters:
		functions: specified or all (default) basic models(name of models) to fit.
			Type: list of string
			Default: basicModels_nameList
		dataLength: the length or size of data
			Type: integer
			Default: 0
		piecewise: if consider custom a piecewise function. It is mandatory not to 'piecewise' when the data size is less than 20.
			Type: bool
			Default: False
		operator: operatation between basic models.
			Type: string
			Default: '+'
		maxCombination: max number of combination of basic models.
			Type: integer
			Default: 2
	Returns:
		potential_models: the generated models, include keys: 'model'(function object),'name','form', and 'paras_symbol'
			Type: list of dictionaries
	'''
	functions0 = list(set(functions) & set(basicModels_nameList))	#remove `function` which wasn't in `models`
	if len(functions0) < 2:
		print('Warning -- please use "scipy.optimize.curve_fit" directly if only model to fit;'
			'or check your "functions" is included in\n%s' %basicModels_nameList)
	
	potential_models = []
	#basic model
	if maxCombination >= 1:
		for functionName in functions0:
			#query the model information
			current_model = generateFunction(functionName)
			potential_models.append(current_model)
	
	#piecewise function model based on basic models
	if dataLength <=20: piecewise=False
	if piecewise:
		combinations_p =[[f0,f1] for f0 in functions0 for f1 in functions0]
		for funcs in combinations_p:
			#generate model
			current_model = generateFunction(funcs, operator='piecewise')
			potential_models.append(current_model)
	
	#comprehensive model via arithmetic operations on basic models - addition (substraction), multiplication, and division
	functions1 = list(set(functions) & set(basicModels_nonp_nameList))	#filter non-polynomial
	if len(functions1) > 0:
		funcs_pair = []
		if maxCombination >= 2:
			combinations_2c ={tuple(sorted([f0,f1])) for f0 in functions0 for f1 in functions1}	#unique combinations
			funcs_pair_2c = [list(t) for t in combinations_2c]
			funcs_pair = funcs_pair + funcs_pair_2c
		if maxCombination >= 3:
			combinations_3c ={tuple(sorted([f0,f1,f2])) for f0 in functions0 for f1 in functions1 for f2 in functions1}
			funcs_pair_3c = [list(t) for t in combinations_3c]
			funcs_pair = funcs_pair + funcs_pair_3c
		if maxCombination >= 4:
			combinations_4c ={tuple(sorted([f0,f1,f2,f3])) for f0 in functions0 for f1 in functions1 for f2 in functions1 for f3 in functions1}
			funcs_pair_4c = [list(t) for t in combinations_4c]
			funcs_pair = funcs_pair + funcs_pair_4c
		if maxCombination >=5:
			print('Warning -- Key word "maxCombination >= 5" is too big.')
			pass
			
		for funcs in funcs_pair:
			#generate model
			current_model = generateFunction(funcs, operator=operator)
			potential_models.append(current_model)
	return potential_models

def oneClickCurveFitting(xdata, ydata, functions=basicModels_nameList, piecewise=False, operator='+', maxCombination=2, plot_opt=10, xscale=None, yscale=None, filename_startwith='curvefit', silent=False, feedback=False, **kwargs):
	'''Make a curve-fit in batch.
	
	Parameters:
		xdata: the independent variable where the data is measured.
			Type: array_like or object
		ydata: the dependent data.
			Type: array_like or object
		functions: specified or all (default) basic models(name of models) to fit.
			Type: list of string
			Default: basicModels_nameList
		piecewise: if consider custom a piecewise function. It is mandatory not to 'piecewise' when the data size is less than 20.
			Type: bool
			Default: False
		operator: operatation between basic models.
			Type: string
			Default: '+'
		maxCombination: max number of combination of basic models.
			Type: integer
			Default: 2
		plot_opt: the number of plot for optimal models.
			Type: integer
			Default: 10
		xscale: one of {"linear", "log", "symlog", "logit", ...}
			Type: string
			Default: None
		yscale: one of {"linear", "log", "symlog", "logit", ...}
			Type: string
			Default: None
		filename_startwith: a custom string mark as part of output filename
			Type: string
			Default: 'curvefit'
		silent: minimal output to monitor
			Type: boolean
			Default: False
		feedback: if True, return the optimal model(function object), parameters
			Type: boolean
			Default: False
		kwargs: keyword arguments passed to `curve_fit_m`. Note that `bounds` and `p0` will take no effect when multi-models
			Type: dict
	Returns:
		None
	'''
	if isinstance(xdata, (np.ndarray, list)):
		xdata = np.array(xdata)
	else:
		raise TypeError('Error -- "xdata" must be array_like object')
	if isinstance(ydata, (np.ndarray, list)):
		ydata = np.array(ydata)
	else:
		raise TypeError('Error -- "xdata" must be array_like object')
	
	#generate potential models
	potential_models = generateModels(functions=functions, dataLength=xdata.size, piecewise=piecewise, operator=operator, maxCombination=maxCombination)
	
	#curve fitting
	print('Status -- %d potential models.\nCurve-fitting starts...' % len(potential_models))
	report = []
	
	if 'method' not in kwargs: kwargs['method'] = 'trf'		#`trf` or specified `method
	for m in potential_models:
		try:
			if not silent: print('\t%s' % m['name'])
			kwargs.update(bounds = getBounds(m['model'], xdata, ydata))
			popt, pcov, cost = curve_fit_m(m['model'], xdata, ydata, **kwargs)
			stdevs = np.sqrt(np.diag(pcov))
			report_current = [{'modelname':m['name'],'form':m['form'],'paras_symbol':m['paras_symbol'],'parameters':popt.tolist(),'stdevs':stdevs.tolist(),'cost':cost}]
			report = report + report_current
		except:
			pass
	print('Status -- %d modes succeeded.' % len(report))
	
	#sort and output report
	report.sort(key=lambda m: m['cost'])	#sorting
	output = pathlib.Path('curvefit/%s_report_%s.csv' % (filename_startwith, str(int(time.time()*1e6))))
	output.parent.mkdir(parents=True, exist_ok=True)
	writeLogsDicts2csv(output, report)
	
	#plot
	if plot_opt:
		print('Plotting starts...')
		report_plot = report[:plot_opt] if isinstance(plot_opt,int) and plot_opt < len(report) else report	#plot all or partly
		for m in report_plot:
			model, paras = next(m_p['model'] for m_p in potential_models if m_p['name'] == m['modelname']), m['parameters']
			ydata_fit = model(xdata, *paras)
			if xscale == 'linear': xscale=None
			if yscale == 'linear': yscale=None
			#'linear' scale will be used and plot as a default and basic
			if not silent: print('\t%s' % m['modelname'])
			curve_fit_plot(xdata, ydata, ydata_fit , m['modelname'], filename_startwith=filename_startwith)
			if xscale or yscale: curve_fit_plot(xdata, ydata, ydata_fit , m['modelname'], xscale=xscale, yscale=yscale, filename_startwith=filename_startwith)
	if feedback:
		model, paras = next(m_p['model'] for m_p in potential_models if m_p['name'] == report[0]['modelname']), report[0]['parameters']
		return model, paras
	report.clear()
	print('Reminder -- models report and figures were saved in folder "curvefit".')
