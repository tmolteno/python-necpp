#!/bin/bash
# Script to build the nec2++ python module.
git submodule update --remote
ln -s ../necpp_src .
pushd ../necpp_src
make -f Makefile.git
./configure --without-lapack
popd
pandoc -o README.txt README.md
PYTHON=python
swig -v -Inecpp_src/src/ -python necpp.i
python setup.py build
python setup.py dist
#sudo python setup.py install
