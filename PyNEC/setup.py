#!/usr/bin/env python

"""
setup.py file for PyNEC Python module

Author Tim Molteno. tim@molteno.net
"""

import distutils.sysconfig
from glob import glob
import os
import numpy as np
import setuptools

# Remove silly flags from the compilation to avoid warnings.
cfg_vars = distutils.sysconfig.get_config_vars()
for key, value in cfg_vars.items():
  if type(value) == str:
    cfg_vars[key] = value.replace("-Wstrict-prototypes", "")

# Generate a list of the sources.   
nec_sources = []
nec_sources.extend([fn for fn in glob('necpp_src/src/*.cpp') 
         if not os.path.basename(fn).endswith('_tb.cpp')
         if not os.path.basename(fn).startswith('net_solve.cpp')
         if not os.path.basename(fn).startswith('nec2cpp.cpp')
         if not os.path.basename(fn).startswith('necDiff.cpp')])
nec_sources.extend(glob("PyNEC_wrap.cxx"))

nec_headers = []
nec_headers.extend(glob("necpp_src/src/*.h"))
nec_headers.extend(glob("necpp_src/config.h"))

#with open('README.txt') as f:
    #readme = f.read()


# At the moment, the config.h file is needed, and this should be generated from the ./configure
# command in the parent directory. Use ./configure --without-lapack to avoid dependance on LAPACK
#
necpp_module = setuptools.Extension('_PyNEC',
    sources=nec_sources,
    include_dirs=[np.get_include(), 'necpp_src/src', 'necpp_src/'],
    extra_compile_args = ['-fPIC'],
    extra_link_args = ['-lstdc++'],
    depends=nec_headers,
    define_macros=[('BUILD_PYTHON', '1'), ('NPY_NO_DEPRECATED_API','NPY_1_7_API_VERSION')]
    )

with open("README.md", "r") as fh:
    long_description = fh.read()
    
setuptools.setup (name = 'PyNEC',
    version = '1.7.3.4',
    author  = "Tim Molteno",
    author_email  = "tim@physics.otago.ac.nz",
    url  = "http://github.com/tmolteno/necpp",
    keywords = "nec2 nec2++ antenna electromagnetism radio",
    description = "Python Antenna Simulation Module (nec2++) object-oriented interface",
    long_description=long_description,
    long_description_content_type="text/markdown",
    include_package_data=True,
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
