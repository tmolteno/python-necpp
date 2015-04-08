# Using python-necpp

Installation is easy with the python pip installer.  Install python-necpp with

    pip install necpp

This will download and compile the python-necpp package.

## A Simple Monopole

NEC2 was based on punch cards and an antenna model was described as a series of Cards. 
These are well documented. Nec2++ replaces these cards with function calls each 
function call the equivalent of an nec2 card

The file monopole.py shows how to model a simple vertical whip antenna.

    python monopole.py
    
will print the impedance

    Impedance at base_height=0.50, length=4.00 : ( 134.0,-461.5I) Ohms
    
## Automatically tuning the monopole
