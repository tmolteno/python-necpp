#!/usr/bin/env python

"""
setup.py file for necpp Python module. 
"""

from distutils.core import setup, Extension
from glob import glob
import os

nec_sources = []
nec_sources.extend([fn for fn in glob('../necpp_src/src/*.cpp')
         if not os.path.basename(fn).endswith('_tb.cpp')
         if not os.path.basename(fn).startswith('net_solve.cpp')
         if not os.path.basename(fn).startswith('nec2cpp.cpp')
         if not os.path.basename(fn).startswith('necDiff.cpp')])
nec_sources.extend(glob("necpp_wrap.c"))

nec_headers = []
nec_headers.extend(glob("../necpp_src/src/*.h"))
nec_headers.extend(glob("../necpp_src/config.h"))


# At the moment, the config.h file is needed, and this should be generated from the ./configure
# command in the parent directory. Use ./configure --without-lapack to avoid dependance on LAPACK
#
necpp_module = Extension('_necpp',
    sources=nec_sources,
    include_dirs=['../necpp_src/src/', '../necpp_src/'],
    depends=nec_headers,
    define_macros=[('BUILD_PYTHON', '1')]
    )

with open('README.txt') as f:
    readme = f.read()

setup (name = 'necpp',
    version = '1.7.3.2',
    author  = "Tim Molteno",
    author_email  = "tim@physics.otago.ac.nz",
    url  = "http://github.com/tmolteno/necpp",
    keywords = "nec2 nec2++ antenna electromagnetism radio",
    description = "Python Antenna Simulation Module (nec2++) C-style interface",
    long_description=readme,
    data_files=[('examples', ['../necpp_src/example/test.py'])],
    ext_modules = [necpp_module],
    py_modules = ["necpp"],
    license='GPLv2',
    classifiers=[
    "Development Status :: 5 - Production/Stable",
    "Topic :: Scientific/Engineering",
    "Topic :: Communications :: Ham Radio",
    "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    "Intended Audience :: Science/Research"]
)
