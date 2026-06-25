#!/bin/bash
# Script to build the nec2++ python module.
git submodule update --remote
rm -f necpp_src
ln -s ../necpp_src .
DIR=`pwd`
cd necpp_src
make -f Makefile.git
./configure --without-lapack
cd ${DIR}
PYTHON=python3
swig -v -Inecpp_src/src/ -python necpp.i
python3 setup.py build
#sudo python setup.py install
