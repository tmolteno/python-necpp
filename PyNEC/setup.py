#!/usr/bin/env python

"""
setup.py file for PyNEC Python module
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
nec_sources.extend(glob("PyNEC_wrap.cxx"))

nec_headers = []
nec_headers.extend(glob("../necpp_src/src/*.h"))
nec_headers.extend(glob("../necpp_src/config.h"))


# At the moment, the config.h file is needed, and this should be generated from the ./configure
# command in the parent directory. Use ./configure --without-lapack to avoid dependance on LAPACK
#
necpp_module = Extension('_PyNEC',
    sources=nec_sources,
    #swig_opts=['-v', '-I../src/', '-dhtml'],
    include_dirs=['../necpp_src/src', '../necpp_src/'],
    extra_compile_args = ['-fPIC'],
    extra_link_args = ['-shared', '-lstdc++'],
    depends=nec_headers,
    define_macros=[('BUILD_PYTHON', '1'), ('NPY_NO_DEPRECATED_API','NPY_1_7_API_VERSION')]
    )

# 
#   
#necpp_module = Extension('_necpp',
                           #sources=['necpp_wrap.c'],
                           #include_dirs=['/usr/local/include'],
                           #libraries=['necpp']
                           #)


setup (name = 'PyNEC',
       version = '1.7.0.3',
       author  = "Tim Molteno",
       author_email  = "tim@physics.otago.ac.nz",
       url  = "http://github.com/tmolteno/necpp",
       keywords = "nec2 nec2++ antenna electromagnetism radio",
       description = "Python Antenna Simulation Module (nec2++) object-oriented interface",
       data_files=[('examples', ['example/test_rp.py'])],
       ext_modules = [necpp_module],
       requires = ['numpy'],
       py_modules = ["PyNEC"],
       license='GPLv2',
       classifiers=[
          "Development Status :: 5 - Production/Stable",
          "Topic :: Scientific/Engineering",
          "Topic :: Communications :: Ham Radio",
          "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
          "Intended Audience :: Science/Research"]
       )
