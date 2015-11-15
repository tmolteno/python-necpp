# python-necpp: Antenna simulation in python

This repository contains two wrappers for the nec2++ antenna simulation package:

* PyNEC/ contains a wrapper using SWIG of the C interface (Python module name: necpp)
* PyNECPP/ contains a wrapper of the C++ interfaces (Python module name: PyNEC).

Both are based on Tim Molteno (tim@physics.otago.ac.nz)'s code.

Personally, I (Bart Coppens, kde@bartcoppens.be) am more interested in a slightly cleaned-up version of the C++ interface wrappers. (I might still rename the Python module names to match the directory names, or rename the directories, or both)

## TODOs
The cleaner API should really be ported to C++, so the clean wrappers get automatically generated, and C++ can use the same cleaner interface
