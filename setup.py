#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from __future__ import absolute_import
from __future__ import print_function

import io
import re
from glob import glob
from os.path import basename
from os.path import dirname
from os.path import join
from os.path import splitext

from setuptools import setup, find_packages

abstract_requirements = [
    'invoke',
    'jinja2',
    'click',
    ]

setup(
    name='bimhaw',
    version='v0.1',
    author="Samuel D. Lotz",
    author_email="samuel.lotz@salotz.info",
    description="Modern useful dotfile management",

    license="MIT",
    url="https://github.com/salotz/bimhaw",
    classifiers=[
        "Topic :: Utilities",
        'Programming Language :: Python :: 3'
    ],

    # package
    packages=find_packages(where='src'),
    package_dir={'' : 'src'},

    # modules
    # py_modules=[splitext(basename(path))[0]
    #             for path in glob('src/*.py')],

    install_requires=abstract_requirements,

    entry_points={
        'console_scripts' : ['bimhaw = bimhaw.cli:program.run'],
    },

    include_package_data=True,

    )
