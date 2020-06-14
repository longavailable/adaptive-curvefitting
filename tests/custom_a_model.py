import numpy as np

from longscurvefitting import generateFunction

#generate a model composited by gaussian and erf function
funcs = ['gaussian','erf']
myfunc = generateFunction(funcs, functionName='myfunc', operator='+')['model']

xdata = np.linspace(0,50,10)
ydata_calculated = myfunc(xdata, 40, 10, 3, 30, 30, 4)

print(myfunc)
print(ydata_calculated)
