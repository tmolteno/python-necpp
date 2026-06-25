#!/usr/bin/env python

"""
setup.py file for necpp Python module.

This file handles the C extension compilation only.
All package metadata is in pyproject.toml.
"""

import os
from glob import glob

from setuptools import Extension, setup

nec_sources = []
nec_sources.extend(
    [
        fn
        for fn in glob("necpp_src/src/*.cpp")
        if not os.path.basename(fn).endswith("_tb.cpp")
        if not os.path.basename(fn).startswith("net_solve.cpp")
        if not os.path.basename(fn).startswith("nec2cpp.cpp")
        if not os.path.basename(fn).startswith("necDiff.cpp")
    ]
)
nec_sources.extend(glob("necpp_wrap.c"))

# At the moment, the config.h file is needed, and this should be generated from the ./configure
# command in the parent directory. Use ./configure --without-lapack to avoid dependance on LAPACK
#
necpp_module = Extension(
    "_necpp",
    sources=nec_sources,
    include_dirs=["necpp_src/src/", "necpp_src/"],
    define_macros=[("BUILD_PYTHON", "1")],
)

setup(
    ext_modules=[necpp_module],
    data_files=[("examples", ["necpp_src/example/test.py"])],
)
