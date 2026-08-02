#!/usr/bin/env python
# Copyright (c) 2008-2026 Tim Molteno (tim@elec.ac.nz)

"""
setup.py file for necpp Python module.

This file handles the C extension compilation only.
All package metadata is in pyproject.toml.
"""

import datetime
import os
from glob import glob

from setuptools import Extension, setup

# ---------------------------------------------------------------------------
# Generate config.h (normally done by CMake, but needed for pip installs and
# PEP 517 isolated builds where CMake is not available).
# ---------------------------------------------------------------------------
BUILD_DIR = "necpp_src/build"
os.makedirs(BUILD_DIR, exist_ok=True)

# Try to read the version from pyproject.toml; fall back to a known default.
_version = "2.3.4"
try:
    import tomllib  # Python 3.11+
except ImportError:
    try:
        import tomli as tomllib
    except ImportError:
        pass
    else:
        with open("pyproject.toml", "rb") as _f:
            _version = tomllib.load(_f)["project"]["version"]
else:
    with open("pyproject.toml", "rb") as _f:
        _version = tomllib.load(_f)["project"]["version"]

_build_date = datetime.date.today().strftime("%Y-%m-%d")

_config_h = os.path.join(BUILD_DIR, "config.h")
with open(_config_h, "w") as _f:
    _f.write(f"""#ifndef CONFIG_H
#define CONFIG_H

#define NECPP_VERSION "{_version}"
#define NECPP_BUILD_DATE "{_build_date}"

#endif /* CONFIG_H */
""")

nec_sources = []
nec_sources.extend(
    [
        fn
        for fn in glob("necpp_src/src/*.cpp")
        if not os.path.basename(fn).endswith("_tb.cpp")
        if not os.path.basename(fn).startswith("net_solve.cpp")
        if not os.path.basename(fn).startswith("nec2cpp.cpp")
        if not os.path.basename(fn).startswith("necDiff.cpp")
        if not os.path.basename(fn).startswith("nec_wasm.cpp")
    ]
)
nec_sources.extend(glob("necpp_wrap.c"))

# config.h is auto-generated above from pyproject.toml metadata.
#
necpp_module = Extension(
    "_necpp",
    sources=nec_sources,
    include_dirs=["necpp_src/src/", "necpp_src/", "necpp_src/build/", "necpp_src/src/eigen"],
    define_macros=[("BUILD_PYTHON", "1")],
)

setup(
    ext_modules=[necpp_module],
    data_files=[("examples", ["necpp_src/example/test.py"])],
)
