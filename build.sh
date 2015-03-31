#!/bin/bash
# Script to build the nec2++ python module.
pushd necpp_src
make -f Makefile.git
./configure --without-lapack
popd
pandoc -o README.txt README.md
PYTHON=python
swig -v -Inecpp_src/src/ -python necpp.i
python setup.py build
#sudo python setup.py install
