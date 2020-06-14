import numpy as np

from longscurvefitting import oneClickCurveFitting


xdata = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
ydata = [50,46,45,49,58,80,120,110,108,106,105,102,101,110,120,140,160,170,165,160,165]

models=['constant', 'linear', 'quadratic', 'cubic', 'gaussian', 'erf', 'cauchy', 'exponential', 'power_law', 'pearson3']
#models=['quadratic', 'cubic', 'gaussian', 'erf', 'cauchy', 'exponential']


#oneClickCurveFitting(xdata, ydata, models)
oneClickCurveFitting(xdata, ydata, models, silent=True)
#oneClickCurveFitting(xdata, ydata, models, piecewise=True, maxCombination=2, plot_opt=5)
#oneClickCurveFitting(xdata, ydata, models, maxCombination=3, plot_opt=10, xscale='log')
#oneClickCurveFitting(xdata, ydata, models, maxCombination=3, plot_opt=10, yscale='log')
#oneClickCurveFitting(xdata, ydata, models, maxCombination=3, plot_opt=10, filename_startwith='justatest')

'''
#it will return the optimal model (model, parameters), when feedback is set `True`
re = oneClickCurveFitting(xdata, ydata, models, feedback=True)
print(re)
'''