#Assistant functions

import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.rcParams['figure.figsize'] = [4, 4] # width and height in inches
mpl.rcParams['savefig.dpi'] = 300
mpl.rcParams['font.size'] = 12
mpl.rcParams['lines.linewidth'] = 1.0	# in points
plt.rcParams['font.family'] = 'Times New Roman'

import pathlib
import csv
import time
import inspect

#A simple plotting function to visualize outputs
def curve_fit_plot(xdata, ydata, ydata_fit, function_name, xscale=None, yscale=None, filename_startwith='curvefit'):
	'''Plot a figure include the original data, fitted curve and residuals.
	
	Parameters:
		xdata: the independent variable where the data is measured.
			Type: array_like or object
		ydata: the dependent data.
			Type: array_like or object
		ydata_fit: the fitted dependent data.
			Type: array_like or object
		function_name: a string include function information.
			Type: string
		xscale: one of {"linear", "log", "symlog", "logit", ...}
			Type: string
			Default: None
		yscale: one of {"linear", "log", "symlog", "logit", ...}
			Type: string
			Default: None
		filename_startwith: a custom string mark as part of output filename
			Type: string
			Default: 'curvefit'
	Returns:
		None
	'''
	fig = plt.figure()
	#frame1 = fig.add_axes([.1,.3,.8,.6]) if 'power_law' not in function_name else fig.add_axes([.1,.38,.8,.52])
	frame1 = fig.add_axes([.1,.3,.8,.6])
	plt.plot(xdata, ydata, '.', label='data')
	plt.plot(xdata, ydata_fit, '-', label=function_name)
	plt.legend()
	plt.ylabel('y-data')
	plt.grid(True)
	plt.xticks([]) #disable x ticks
	
	if xscale: plt.xscale(xscale)
	if yscale: plt.yscale(yscale)
	
	#residual subplot
	frame2 = fig.add_axes([.1,.1,.8,.2])
	plt.plot(xdata,ydata_fit-ydata,'k')
	plt.ylabel('Residuals')
	plt.grid(True)
	if xscale: plt.xscale(xscale)	

	output = pathlib.Path('curvefit/%s_%s_%s.png' % (filename_startwith, function_name, str(int(time.time()*1e6))))
	output.parent.mkdir(parents=True, exist_ok=True)
	plt.savefig(output, bbox_inches = 'tight',pad_inches = 0)
	plt.close()
	#time.sleep(3)

def fileIsValid(filename):
	'''Check if a file exist and non-empty
	
	Parameters:
		filename: file to check
			Type: string, pathlib.Path
	Returns:
		boolean
	'''
	filename = pathlib.Path(filename)
	return True if filename.is_file() and filename.stat().st_size > 0 else False

def writeLogsDicts2csv(fileName, dicts):
	'''	Write a list of dictionaries to a csv-format file.
	
	Parameters:
		fileName: output filename
			Type: string, pathlib.PosixPath
		dicts: output list of dictionaries
			Type: list, dictionary
	Returns:
		Boolean
	'''
	if dicts:
		if not isinstance(dicts, (dict, list)):
			print('Failed -- check if type of object "dict" or "list" of dictionaries')
			return False
		if isinstance(dicts, dict):
			dicts = [dicts]
		headers = dicts[0].keys()
		if not fileIsValid(fileName):
			with open(fileName, 'w', newline='') as f:
				writer = csv.DictWriter(f, fieldnames=headers)
				writer.writeheader()
				writer.writerows(dicts)
			return True
		else:					
			with open(fileName, 'a', newline='') as f:
				writer = csv.DictWriter(f, fieldnames=headers)
				writer.writerows(dicts)
			return True

#functions to return a list of arguments and length of it
funcArgs = lambda f: inspect.getfullargspec(f)[0]
funcArgsNr =  lambda f: len(funcArgs(f))
