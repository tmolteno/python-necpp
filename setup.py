#!/usr/bin/env python

"""
setup.py file for necpp Python module
"""

from distutils.core import setup, Extension
from glob import glob
import os

nec_sources = ['necpp.i']
nec_sources.extend([fn for fn in glob('necpp_src/src/*.cpp') 
         if not os.path.basename(fn).endswith('_tb.cpp')
         if not os.path.basename(fn).startswith('net_solve.cpp')
         if not os.path.basename(fn).startswith('nec2cpp.cpp')
         if not os.path.basename(fn).startswith('necDiff.cpp')])
#nec_sources.extend(glob("necpp_wrap.c"))

nec_headers = []
nec_headers.extend(glob("necpp_src/src/*.h"))
nec_headers.extend(glob("necpp_src/config.h"))


# At the moment, the config.h file is needed, and this should be generated from the ./configure
# command in the parent directory. Use ./configure --without-lapack to avoid dependance on LAPACK
#
necpp_module = Extension('_necpp',
    sources=nec_sources,
    swig_opts=['-v', '-Inecpp_src/src/', '-dhtml'],
    include_dirs=['necpp_src/src/', 'necpp_src/'],
    depends=nec_headers,
    define_macros=[('BUILD_PYTHON', '1')]
    )

# 
#   
#necpp_module = Extension('_necpp',
                           #sources=['necpp_wrap.c'],
                           #include_dirs=['/usr/local/include'],
                           #libraries=['necpp']
                           #)


setup (name = 'necpp',
       version = '1.6.1',
       author  = "Tim Molteno",
       author_email  = "tim@physics.otago.ac.nz",
       url  = "http://github.com/tmolteno/necpp",
       description = "Python Antenna Simulation Module (nec2++) C-style interface",
       ext_modules = [necpp_module],
       py_modules = ["necpp"],
       license='GPLv2'
       )
