# -*- encoding: utf-8 -*-

'''A setuptools script to install strip_recipes
'''

from setuptools import setup, find_packages
import os

here = os.path.abspath(os.path.dirname(__file__)

setup(
    name='strip_recipes',
    version='1.0.0',
    description='Create recipes for the LSPE/Strip tester software',
    long_description='''
Python library to easily create complex recipes to be used with the LSPE/Strip
tester software. All the Python control structures (if, while, for) can be used''',
    author='Maurizio Tomasi',
    author_email='maurizio.tomasi@unimiREMOVETHIS.it',
    url='https://github.com/ziotom78/strip_recipes',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers'
    ],
    keywords='cosmology laboratory'
)
