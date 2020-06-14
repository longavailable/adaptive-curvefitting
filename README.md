
# Adaptive Curvefitting Tool

[![PyPI version](https://badge.fury.io/py/adaptive-curvefitting.svg)](https://badge.fury.io/py/adaptive-curvefitting)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3893596.svg)](https://doi.org/10.5281/zenodo.3893596)

Adaptive curvefitting is a tool to find potentially optimal models for your research data. It's based on [scipy], [numpy], and [matplotlib]. 

## Table of contents
- [Why is this tool?](#why-is-this-tool)
- [Installation, update and uninstallation](#installation--update-and-uninstallation)
  * [To install](#to-install)
  * [To update](#to-update)
  * [To uninstall](#to-uninstall)
- [Usage](#usage)
  * [Import the required module](#import-the-required-module)
  * [Do the curvefitting](#do-the-curvefitting)
  * [Generate a expected model](#generate-a-expected-model)
  * [Re-use the fitted curve](#re-use-the-fitted-curve)
- [Shortages](#shortages)
- [How to cite?](#how-to-cite)
- [Changelog](#changelog)

## Why is this tool

The very difference of adaptive-curvefitting with [numpy.polyfit], [scipy.optimize.curve_fit] or [scipy.optimize.least_squares] is ***the hypothesis you don’t know which model to fit***. If you already have the expected model, the methods in [scipy] and [numpy] are fantastic tools and better than this one. ***When you explore something unknown, this will be a maybe***.

## Installation, update and uninstallation

### To install

Quick installation with [pip]:
```bash
pip install adaptive-curvefitting
```

### To update

```bash
pip install --upgrade adaptive-curvefitting
```

### To uninstall

```bash
pip uninstall adaptive-curvefitting
```

## Usage

### Import the required module

In general,

```python
import longscurvefitting
```

or import the specified function:

```python
from longscurvefitting import oneClickCurveFitting
from longscurvefitting import generateFunction
from longscurvefitting import generateModels
```

### Do the curvefitting

```python
oneClickCurveFitting(xdata, ydata)
```

There are some optional arguments of `oneClickCurveFitting`. 
- functions: specified or all (default) basic models(name of models) to fit.
	- Type: list of string
	-	Default: basicModels_nameList
- piecewise: if consider custom a piecewise function. It is mandatory not to 'piecewise' when the data size is less than 20.
	- Type: bool
	- Default: False
- operator: operatation between basic models.
	- Type: string
	- Default: '+'
- maxCombination: max number of combination of basic models.
	- Type: integer
	- Default: 2
- plot_opt: the number of plot for optimal models.
	- Type: integer
	- Default: 10
- xscale: one of {"linear", "log", "symlog", "logit", ...}
	- Type: string
	- Default: None
- yscale: one of {"linear", "log", "symlog", "logit", ...}
	- Type: string
	- Default: None
- filename_startwith: a custom string mark as part of output filename
	- Type: string
	- Default: 'curvefit'
- silent: minimal output to monitor
	- Type: boolean
	- Default: False
- feedback: if True, return the optimal model(function object), parameters
	- Type: boolean
	- Default: False
- kwargs: keyword arguments passed to `curve_fit_m`. Note that `bounds` and `p0` will take no effect when multi-models.
	- Type: dict

See the complete example "[/tests/curvefitting.py]".

### Generate a expected model

Create a model composited by gaussian and erf function:

```python
funcs = ['gaussian','erf']
myfunc = generateFunction(funcs, functionName='myfunc', operator='+')['model']
```

See the complete example "[/tests/custom_a_model.py]".

### Re-use the fitted curve

See the complete example "[/tests/reuse_the_fitted_model.py]".

## Shortages

- Based on [scipy.optimize.least_squares], it cannot enhance the estimate of specified model. Evenmore, it has more limit than [scipy.optimize.least_squares]. 
For example, arguments of `bounds`, `x0` or `p0` were not supported due to the ***basic hypothesis***.

## How to cite

If this tool is useful to your research, 
<a class="github-button" href="https://github.com/longavailable/adaptive-curvefitting" aria-label="Star longavailable/adaptive-curvefitting on GitHub">star</a> and cite it as below:
```
Xiaolong Liu, & Meixiu Yu. (2020, June 14). longavailable/adaptive-curvefitting (Version v0.1.0). Zenodo. 
http://doi.org/10.5281/zenodo.3893596
```
Easily, you can import it to 
<a href="https://www.mendeley.com/import/?url=https://zenodo.org/record/3893596" class="eye-protector-processed" style="border-color: rgba(0, 0, 0, 0.35); color: rgb(0, 0, 0);"><i class="fa fa-external-link"></i> Mendeley</a>.

## Changelog

### v0.1.0

- First release.


[scipy]: https://scipy.org/scipylib/
[numpy]: https://numpy.org/
[matplotlib]: https://matplotlib.org/
[scipy.optimize.curve_fit]: https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.curve_fit.html
[numpy.polyfit]: https://numpy.org/doc/stable/reference/generated/numpy.polyfit.html?highlight=fit#numpy-polyfit
[scipy.optimize.least_squares]: https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.least_squares.html
[pip]: https://pip.pypa.io/en/stable/
[/tests/curvefitting.py]: /tests/curvefitting.py
[/tests/custom_a_model.py]: /tests/custom_a_model.py
[/tests/reuse_the_fitted_model.py]: /tests/reuse_the_fitted_model.py