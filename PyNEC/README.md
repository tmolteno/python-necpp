# Python NEC2++ Module

This module wraps the C++ API for antenna simulation of nec2++. It is easier to work with, and more powerful than the C-style API wrapper. Works with Python 2.7 and 3+.


## Usage

Here is an example that plots a radiation pattern.

    from PyNEC import *
    import numpy as np

    #creation of a nec context
    context=nec_context()

    #get the associated geometry
    geo = context.get_geometry()

    #add wires to the geometry
    geo.wire(0, 36, 0, 0, 0, -0.042, 0.008, 0.017, 0.001, 1.0, 1.0)
    context.geometry_complete(0)

    context.gn_card(-1, 0, 0, 0, 0, 0, 0, 0)

    #add a "ex" card to specify an excitation
    context.ex_card(1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0)

    #add a "fr" card to specify the frequency 
    context.fr_card(0, 2, 2400.0e6, 100.0e6)

    #add a "rp" card to specify radiation pattern sampling parameters and to cause program execution
    context.rp_card(0, 91, 1, 0, 5, 0, 0, 0.0, 45.0, 4.0, 2.0, 1.0, 0.0)

    #get the radiation_pattern
    rp = context.get_radiation_pattern(0)

    # Gains are in decibels
    gains_db = rp.get_gain()
    gains = 10.0**(gains_db / 10.0)
    thetas = rp.get_theta_angles() * 3.1415 / 180.0
    phis = rp.get_phi_angles() * 3.1415 / 180.0


    # Plot stuff
    import matplotlib.pyplot as plt

    ax = plt.subplot(111, polar=True)
    ax.plot(thetas, gains[:,0], color='r', linewidth=3)
    ax.grid(True)

    ax.set_title("Gain at an elevation of 45 degrees", va='bottom')
    plt.savefig('RadiationPattern.png')
    plt.show()

## Build

Requirements

* [Pandoc](https://pandoc.org/)
* [Swig](http://www.swig.org/)
* configure & make
* pip 
* setuptools
* wheel
*Note: For Windows: Compling requires [C/C++ compliers](https://wiki.python.org/moin/WindowsCompilers). Also, add the path to swig.exe to environment.*

    
        $ git clone --recursive https://github.com/tmolteno/python-necpp.git
        $ cd python-necpp
        $ cd PyNEC
        $ ./build.sh
        $ python setup.py bdist_wheel
        $ sudo python setup.py install
    
    *Note: sudo is not required in windows.*
    
## Install

    $ sudo pip install pynec
   *Note: sudo is not required in windows.*

## Testing

Requirements

* matplotlib

    $ python example/test_rp.py

   
The example directory contains the following additional examples (that are inspired by excercises from a course on antennas):

* logperiodic_opt.py is an example on how to combine PyNECPP with scipy.optimize to use a genetic algorithm to **optimize an antenna for multiple frequency bands** at the same time (which I thin is not possible in 4nec2). The resulting gains and VSWR are plotted over the frequency range of interest. This requires scipy >= 0.15.0 due to the usage of scipy.optimize.differential_evolution.
* monopole_realistic_ground_plane.py plots the vertical gain pattern of a monopole antenna. Its dimensions are optimized with a local search, and the path through the search space is visualized with a heat map.
* dipole.py does a very simple optimization of a dipole, and plots the VSWR over a given frequency range for different system impedances to file.


