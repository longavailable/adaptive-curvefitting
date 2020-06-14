#Basic models or functions in form of f(x,...)

import numpy as np
from scipy.stats import norm
from scipy.stats import cauchy as sci_cauchy
from scipy.stats import pearson3 as sci_pearson3
from scipy.special import erf as sci_erf
from scipy.special import expit, logit

from ._helpers import funcArgsNr

#polynomial functions: constant, linear, quadratic, cubic
def constant(x, a):
	y = np.full(x.size, a)
	return y

def linear(x, a, b):
	y = a * x + b
	return y

def quadratic(x, a, b, c):
	y = a * x**2 + b * x + c
	return y

def cubic(x, a, b, c, d):
	y = a * x**3 + b * x**2 + c * x + d
	return y
	
#Gaussian functions
def gaussian(x, a, b, c):
	'''General Gaussian function
	Parameters:
		x: independent variable
		a, b, c: parameters for function
	returns:
		y: dependent variable
	'''
	y = a*np.exp(-np.power(x-b,2)/(2*np.power(c,2)))
	#y = a * c * np.sqrt(2*np.pi) * norm.pdf(x, b, c) #equivalent to above
	return y

def erf(x, a, b, c):
	'''General Gaussian error function (erf), the general cumulative distribution function (CDF) of Gaussian or normal distribution.
	Parameters:
		x: independent variable
		a, b, c: parameters for function
	returns:
		y: dependent variable
	'''
	y = a * sci_erf((x-b)/c)
	return y

#Cauchy-Lorentz function
def cauchy(x, a, b, c):
	'''General Cauchy function, the probability density function (PDF) of Cauchy or Lorentz distribution.
	Parameters:
		x: independent variable
		a, b, c: parameters for function
	returns:
		y: dependent variable
	'''
	y = a * sci_cauchy.pdf(x, loc=b, scale=c)
	return y

#Pearson
def pearson3(x, a, b, c, d):
	'''General Pearson Type 3 function, the probability density function (PDF) of Pearson type III distribution.
	https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.pearson3.html
	Parameters:
		x: independent variable
		a, b, c, d: parameters for function
	returns:
		y: dependent variable
	'''
	y = a * sci_pearson3.pdf(x, skew=b, loc=c, scale=d)
	return y

#exponential
def exponential(x, a, b):
	'''General exponential function
	Parameters:
		x: independent variable
		a, b: parameters for function
	returns:
		y: dependent variable
	'''
	#y = a*np.exp(b*x)	#natural exponential function
	y = a * b ** x	#equivalent ?
	return y

def logarithm(x, a, b):
	'''General logarithm function, inverse function to exponentiation -- y = a * log_b (x)
	'''
	if b ==1: b = b + 0.001
	y = a * np.log(x) / np.log(b)
	return y

def logistic(x, a, b, c):
	'''General logistic function, the common S-shaped curve.
	https://en.wikipedia.org/wiki/Logistic_function
	'''
	y = a * expit(b*x + c)
	return y

def reciprocal(x, a, b):
	'''Deprecated. It's a special of general power-law function. General reciprocal function
	
	Note that `np.reciprocal` doesn't work with integers.
	'''
	y = 1 /(a * x + b)
	# y = np.reciprocal(a * x + b)
	return y

#power-law
def power_law(x, a, b):
	'''General power-law function
	
	Note that `np.power` doesn't work with a negative integer power.
	Parameters:
		x: independent variable
		a, b, c: parameters for function
	returns:
		y: dependent variable
	'''
	y = a * np.power(x, float(b))
	#y = np.power(a * x + b, float(c))
	#y = a*np.power(x + b,float(c))
	return y

__custom = '''
def %s(x, %s):
	return %s
'''
			
#metadata of custom basic models/functions
basicModels = [
	{'model':constant,'name':'constant','n_para':funcArgsNr(constant)-1},
	{'model':linear,'name':'linear','n_para':funcArgsNr(linear)-1},
	{'model':quadratic,'name':'quadratic','n_para':funcArgsNr(quadratic)-1},
	{'model':cubic,'name':'cubic','n_para':funcArgsNr(cubic)-1},
	{'model':gaussian,'name':'gaussian','n_para':funcArgsNr(gaussian)-1},
	{'model':erf,'name':'erf','n_para':funcArgsNr(erf)-1},
	{'model':cauchy,'name':'cauchy','n_para':funcArgsNr(cauchy)-1},
	{'model':pearson3,'name':'pearson3','n_para':funcArgsNr(pearson3)-1},
	{'model':exponential,'name':'exponential','n_para':funcArgsNr(exponential)-1},
	{'model':logarithm,'name':'logarithm','n_para':funcArgsNr(logarithm)-1},
	{'model':logistic,'name':'logistic','n_para':funcArgsNr(logistic)-1},
	{'model':power_law,'name':'power_law','n_para':funcArgsNr(power_law)-1},
	{'model':reciprocal,'name':'reciprocal','n_para':funcArgsNr(reciprocal)-1},
	]
#list of models' name
basicModels_nameList = [model['name'] for model in basicModels]
basicModels_nonp_nameList = [model['name'] for model in basicModels[4:]]	#non-polynomial
#models=['constant', 'linear', 'quadratic', 'cubic', 'gaussian', 'erf', 'cauchy', 'exponential', 'logarithm', 'logistic', 'reciprocal', 'power_law', 'pearson3']
#models=['constant', 'linear', 'quadratic', 'cubic', 'gaussian', 'erf', 'cauchy', 'exponential', 'logarithm', 'logistic', 'power_law', 'pearson3']
