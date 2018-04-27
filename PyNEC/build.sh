#!/bin/bash
#
# Build script for the PyNEC module. 
#
# Author. Tim Molteno.
#
git submodule update --remote
# 
ln -s ../necpp_src .
pushd necpp_src
make -f Makefile.git
./configure --without-lapack
popd

# Generate a README.txt from README.md
pandoc -o README.txt README.md

# Build PyNEC
swig -Wall -v -c++ -python PyNEC.i
python setup.py build
