# python-necpp: Antenna simulation in python

This repository contains two wrappers for the nec2++ antenna simulation package:

* PyNEC/ contains a wrapper using SWIG of the C interface (Python module name: necpp).
* PyNECPP/ contains a wrapper of the C++ interfaces (Python module name: PyNEC). The example/ directory furthermore contains some nicer, more readable Python wrappers that make toying around with NEC a less painful experience.

Both are based on Tim Molteno (tim@physics.otago.ac.nz)'s code.

Personally, I (Bart Coppens, kde@bartcoppens.be) am more interested in a slightly cleaned-up version of the C++ interface wrappers. (I might still rename the Python module names to match the directory names, or rename the directories, or both). In particular, as mentioned above, PyNECPP/example contains context_clean.py, which separates some of the NEC cards with multiple options into multiple functions (with named arguments that make sense, rather than itmp1, itmp2, etc). I've only really done this for the code I was playing around with in the example/ subdirectory, though, lots of cards (and sub-functionalities of cards) remain unwrapped/unported. Still, I found it to be nicer.

The PyNECPP/example directory contains the following additional examples (that are inspired by excercises from a course on antennas):
* logperiodic_opt.py is an example on how to combine PyNECPP with scipy.optimize to use a genetic algorithm to **optimize an antenna for multiple frequency bands** at the same time (which I thin is not possible in 4nec2). The resulting gains and VSWR are plotted over the frequency range of interest. This requires scipy >= 0.15.0 due to the usage of scipy.optimize.differential_evolution.
* monopole_realistic_ground_plane.py plots the vertical gain pattern of a monopole antenna. Its dimensions are optimized with a local search, and the path through the search space is visualized with a heat map.
* dipole.py does a very simple optimization of a dipole, and plots the VSWR over a given frequency range for different system impedances to file.

## TODOs
The cleaner API should really be **ported to C++**, so the clean wrappers get automatically generated, and C++ can use the same cleaner interface. But for now, I'm happy with the Python wrapper :)
