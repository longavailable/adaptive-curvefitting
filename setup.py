
__version__ = '0.1.4'

from setuptools import setup, find_packages

with open('README.md', 'r') as fh:
	long_description = fh.read()

setup(
	name='adaptive-curvefitting',
	version=__version__,
	author='Xiaolong "Bruce" Liu, Meixiu Yu',
	author_email='liuxiaolong125@gmail.com, meixiuyu@hhu.edu.cn',
	description='A tool for adaptive selection of curve-fitting models.',
	long_description=long_description,
	long_description_content_type='text/markdown',
	url='https://github.com/longavailable/adaptive-curvefitting',
	packages=find_packages(),
	classifiers=[
		'Programming Language :: Python :: 3',
		'License :: OSI Approved :: MIT License',
		'Operating System :: OS Independent',
	],
	python_requires='>=3.6',
	install_requires=[
		'pandas',
		'matplotlib',
		'scipy',
	 ],
)