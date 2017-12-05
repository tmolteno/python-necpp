#!/bin/bash
#
# Build script for the PyNEC module. 
#
# Author. Tim Molteno.
#
git submodule update --remote

# In windows this generates error since, the make, configure,libtoolize shows ignorable error
pushd ../necpp_src
make -f Makefile.git
./configure --without-lapack
popd

# Generate a README.txt from README.md
pandoc -o README.txt README.md

# Build PyNEC
swig -Wall -v -c++ -python PyNEC.i
python setup.py build