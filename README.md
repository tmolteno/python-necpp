# python-necpp: Antenna simulation in python

This repository contains two wrappers for the nec2++ antenna simulation package:

* necpp/ contains a wrapper using SWIG of the C interface (Python module name: necpp).
* PyNEC/ contains a wrapper of the C++ interfaces (Python module name: PyNEC).  The example/ directory furthermore contains some nicer, more readable Python wrappers that make toying around with NEC a less painful experience.

Both are based on Tim Molteno (tim@physics.otago.ac.nz)'s code with major cleanup by Bart Coppens.

## TODOs
The cleaner API should really be **ported to C++**, so the clean wrappers get automatically generated, and C++ can use the same cleaner interface. But for now, I'm happy with the Python wrapper :)
