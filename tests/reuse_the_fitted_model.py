import numpy as np

from longscurvefitting import queryModel

#fitted modelname and parameters
fitted_model = {'modelname':'operation_power_law_power_law',
								'parameters':[5, -0.4, 0.1, 0.5]
								}

#query fitted model by modelname, return a python function object
model = queryModel(fitted_model['modelname'])

#reuse it
xdata = np.linspace(1e6,1e8,20)
ydata_calculated = model(xdata, *fitted_model['parameters'])

print(ydata_calculated)