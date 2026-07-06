#!/bin/bash
# Copyright (c) 2008-2026 Tim Molteno (tim@elec.ac.nz)
# Script to build the nec2++ python module.
# Uses uv build (https://github.com/astral-sh/uv) for modern PEP 517 builds.
git submodule update --remote
rm -f necpp_src
ln -s ../necpp_src .
DIR=`pwd`
cd necpp_src
make -f Makefile.git
./configure
cd ${DIR}
PYTHON=python3

# Generate SWIG wrapper
swig -v -Inecpp_src/src/ -python necpp.i

# Build with uv (modern, fast PEP 517 build)
uv build

# Or use the traditional setuptools build:
# python3 setup.py build
# sudo python setup.py install
