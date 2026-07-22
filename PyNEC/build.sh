#!/bin/bash
# Copyright (c) 2008-2026 Tim Molteno (tim@elec.ac.nz)
#
# Build script for the PyNEC module.
# Uses uv build (https://github.com/astral-sh/uv) for modern PEP 517 builds.
#
# Author. Tim Molteno.
#
git submodule update --remote --init
# Create a symlink so setup.py (run from this dir) can resolve necpp_src/.
rm -f necpp_src
ln -s ../necpp_src .
DIR=`pwd`
cd ../necpp_src
cmake -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build
cd ${DIR}

# Generate SWIG wrapper
swig -Wall -v -c++ -python PyNEC.i

# Build with uv (modern, fast PEP 517 build)
uv build

# Or use the traditional setuptools build:
# python3 setup.py build
