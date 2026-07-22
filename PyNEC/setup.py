#!/usr/bin/env python
# Copyright (c) 2008-2026 Tim Molteno (tim@elec.ac.nz)

"""
setup.py file for PyNEC Python module

This file handles the C++ extension compilation only.
All package metadata is in pyproject.toml.

Author Tim Molteno. tim@molteno.net
"""

import os
from glob import glob

from setuptools import Extension, setup

# numpy is declared in pyproject.toml build-system.requires for PEP 517 isolated builds.
# Guard against the case where setup.py is evaluated for metadata before build deps are installed.
try:
    import numpy as np
except ImportError:
    np = None

# Generate a list of the sources.
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
nec_sources.extend(glob("PyNEC_wrap.cxx"))

# config.h is generated from cmake in the parent directory.
#
if np is not None:
    include_dirs = [np.get_include(), "necpp_src/src", "necpp_src/", "necpp_src/build/", "necpp_src/win32/", "necpp_src/src/eigen"]
else:
    # Fallback for metadata-only setup phases (e.g., egg_info) before build deps are installed
    include_dirs = ["necpp_src/src", "necpp_src/", "necpp_src/build/", "necpp_src/win32/", "necpp_src/src/eigen"]

necpp_module = Extension(
    "_PyNEC",
    sources=nec_sources,
    include_dirs=include_dirs,
    extra_compile_args=["-fPIC"],
    extra_link_args=["-lstdc++"],
    define_macros=[
        ("BUILD_PYTHON", "1"),
        ("NPY_NO_DEPRECATED_API", "NPY_1_7_API_VERSION"),
    ],
)

setup(
    ext_modules=[necpp_module],
    data_files=[("examples", ["example/test_rp.py"])],
)
