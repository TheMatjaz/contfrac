#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Package setup for the contfrac library."""

from distutils.core import setup

# noinspection PyUnresolvedReferences
import setuptools

setup(
    name='contfrac',
    version='1.0.0',
    description='Continued fractions library',
    long_description=open('README.md').read(),
    author='Matjaž Guštin',
    author_email='dev@matjaz.it',
    url='https://github.com/TheMatjaz/contfrac',
    license='BSD',
    py_modules=[
        'contfrac',
    ],
    keywords=[
        'continued',
        'fraction',
        'fractions',
        'convergent',
        'rational',
    ],
    classifiers=[
        'Development Status :: Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    python_requires='>=3',
)
