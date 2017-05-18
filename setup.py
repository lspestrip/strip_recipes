# -*- encoding: utf-8 -*-

'''A setuptools script to install strip_recipes
'''

from setuptools import setup

setup(
    name='strip_recipes',
    version='1.0.0',
    description='Create recipes for the LSPE/Strip tester software',
    long_description='''
Python library to easily create complex recipes to be used with the LSPE/Strip
tester software. All the Python control structures (if, while, for) can be used.
(LSPE is a balloon/ground experiment to search for the B-mode signal in the
polarization pattern of the Cosmic Microwave Background. Strip is the low-frequency
polarimetric instrument that will measure the sky from the ground.)''',
    author='Maurizio Tomasi',
    author_email='maurizio.tomasi@unimiREMOVETHIS.it',
    url='https://github.com/ziotom78/strip_recipes',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Topic :: Scientific/Engineering :: Astronomy',
        'Topic :: Scientific/Engineering :: Physics',
        'Topic :: Software Development :: Code Generators'
    ],
    keywords='cosmology laboratory',
    test_suite='nose.collector',
    tests_require=['nose']
)
