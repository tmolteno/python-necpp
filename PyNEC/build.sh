#!/bin/bash
#
# if [ ! -e necpp_src ]
#   then
#     ln -s ../necpp necpp_src
# fi
# git submodule update --remote
# 
pushd necpp_src
make -f Makefile.git
./configure --without-lapack
popd

swig -Wall -v -c++ -python PyNEC.i
python setup.py build