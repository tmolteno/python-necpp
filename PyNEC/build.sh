#!/bin/bash
# Script to build the nec2++ python module.
git submodule update --remote
pushd ../necpp_src
make -f Makefile.git
./configure --without-lapack
popd
pandoc -o README.txt README.md
PYTHON=python
swig -v -I../necpp_src/src/ -python necpp.i
python setup.py build
#sudo python setup.py install
