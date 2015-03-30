# python-necpp
PyPI module for nec2++

This module allows you to do antenna simulations in Python using the nec2++ antenna
simulation package. This is a wrapper using SWIG of the C interface, so the syntax
is quite simple. Have a look at the file test.py, for an example of how this 
library can be used.

### Author

Tim Molteno. tim@physics.otago.ac.nz

## Instructions

To use this python module, you must have the necpp library installed on your system. This can
be installed in the main part of the necpp code distribution.

### NEC2++ source distribution

This is included as a git submodule

    git submodule add git@github.com:tmolteno/necpp necpp
    
    cd necpp; make -f Makefile.git; ./configure --without-lapack

Then you can do the usual

    python setup.py sdist

This will build a source distribution tarball

### Uploading to PyPI.

http://peterdowns.com/posts/first-time-with-pypi.html


    python setup.py sdist upload -r pypitest