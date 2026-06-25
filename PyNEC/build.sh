#!/bin/bash
#
# Build script for the PyNEC module.
# Uses uv build (https://github.com/astral-sh/uv) for modern PEP 517 builds.
#
# Author. Tim Molteno.
#
git submodule update --remote
rm -f necpp_src
ln -s ../necpp_src .
DIR=`pwd`
cd ../necpp_src
make -f Makefile.git
./configure --without-lapack
cd ${DIR}

# Generate SWIG wrapper
swig -Wall -v -c++ -python PyNEC.i

# Build with uv (modern, fast PEP 517 build)
uv build

# Or use the traditional setuptools build:
# python3 setup.py build
