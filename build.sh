#!/bin/sh
# Script to build the nec2++ python module.
#cd necpp_src; make -f Makefile.git
cd necpp_src; ./configure --without-lapack
PYTHON=python
swig -v -Inecpp_src/src/ -python necpp.i
python setup.py build
sudo python setup.py install
