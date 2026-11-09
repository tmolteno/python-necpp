#!/usr/bin/env python
# Copyright (c) 2008-2026 Tim Molteno (tim@elec.ac.nz)

"""
setup.py file for necpp Python module.

This file handles the C extension compilation only.
All package metadata is in pyproject.toml.
"""

import datetime
import os
import subprocess
import sysconfig
from glob import glob

from setuptools import Extension, setup

# ---------------------------------------------------------------------------
# ABI3 (Python stable ABI) support.
#
# Wheels are built once per platform as `cp311-abi3` (works on CPython 3.11+),
# by compiling with Py_LIMITED_API and tagging the wheel accordingly. The
# free-threaded builds (cp314t) do not support the stable ABI, so on those
# interpreters we fall back to a regular full-API build (e.g. building the
# sdist from source).
# ---------------------------------------------------------------------------
_ABI3 = not sysconfig.get_config_var("Py_GIL_DISABLED")
_LIMITED_API_MACRO = ("Py_LIMITED_API", "0x030B0000")  # CPython 3.11

# ---------------------------------------------------------------------------
# Generate config.h (normally done by CMake, but needed for pip installs and
# PEP 517 isolated builds where CMake is not available).
# ---------------------------------------------------------------------------
BUILD_DIR = "necpp_src/build"
os.makedirs(BUILD_DIR, exist_ok=True)


def _engine_sha():
    """Short commit of the bundled necpp_src engine, for provenance."""
    try:
        return subprocess.check_output(
            ["git", "-C", "necpp_src", "rev-parse", "--short", "HEAD"],
            stderr=subprocess.DEVNULL,
            text=True,
        ).strip()
    except Exception:
        return "unknown"


# Try to read the version from pyproject.toml; fall back to a known default.
_version = "2.4.0"
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
#define NECPP_ENGINE_SHA "{_engine_sha()}"

#endif /* CONFIG_H */
""")

# Embed the engine revision in the extension: the config.h macros are
# otherwise unreferenced (nec_version is only used by the nec2cpp CLI, which
# these builds exclude), so without this the string would not be linked in.
_engine_sha_c = os.path.join(BUILD_DIR, "engine_sha.c")
with open(_engine_sha_c, "w") as _f:
    _f.write(
        '#include "config.h"\n'
        "/* Referenced so the revision is strings-searchable in the binary. */\n"
        'const char necpp_engine_sha[] = "necpp_engine_sha=" NECPP_ENGINE_SHA;\n'
    )

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
# Generated above: embeds the necpp_src revision in the binary.
nec_sources.append(_engine_sha_c)

# config.h is auto-generated above from pyproject.toml metadata.
#
_ext_kwargs = {}
_macros = [("BUILD_PYTHON", "1")]
if _ABI3:
    _macros.append(_LIMITED_API_MACRO)
    _ext_kwargs["py_limited_api"] = True

necpp_module = Extension(
    "_necpp",
    sources=nec_sources,
    include_dirs=["necpp_src/src/", "necpp_src/", "necpp_src/build/", "necpp_src/src/eigen"],
    define_macros=_macros,
    **_ext_kwargs,
)

_setup_kwargs = {}
if _ABI3:
    # Tag wheels as cp311-abi3 (one wheel per platform, CPython 3.11+).
    _setup_kwargs["options"] = {"bdist_wheel": {"py_limited_api": "cp311"}}

setup(
    ext_modules=[necpp_module],
    data_files=[("examples", ["necpp_src/example/test.py"])],
    **_setup_kwargs,
)
