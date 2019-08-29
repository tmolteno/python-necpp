#!/bin/bash
#
# Build script for the PyNEC module. 
#
# Author. Tim Molteno.
#
# FIrst have to do git submodule init
git submodule update --remote
# 
ln -s ../necpp_src .
DIR=`pwd`
cd necpp_src
make -f Makefile.git
./configure --without-lapack
cd ${DIR}

# Build PyNEC
swig3.0 -Wall -v -c++ -python PyNEC.i
python3 setup.py build
