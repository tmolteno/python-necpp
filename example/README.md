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

    Impedance at base_height=0.50, length=4.00 : ( 142.2,-422.5I) Ohms

    
## Impedance Mismatch

Radio recevers and transmitters are designed to operate with antennas of a specific impedance (Z0). If the antenna
has a different impedance (Z_ant), this impedance mismatch causes loss of signal. 

The reflection coefficient measures how much signal is reflected at the junction between the antenna and the radio. 
The reflection coefficient (Gamma) is given by

    Gamma  = (Z_ant - Z0)/(Z_ant + Z0)

The transmission coefficient is (1.0 - Gamma) and represents how much of the original signal makes it
through this junction.

## Searching for an optimum antenna

If we minimize the reflection coefficient, then the performance of the antenna will be optimized. 
This is a relatively easy optimization. We can use matplotlib to plot the reflection coefficient
as a function of length, with the base_height of the antenna fixed.

    python impedance_plot.py
    
This shows that for short lengths, less than 10 percent of the signal makes it through. There is a local minimum (of approximately 0.3)
that occurs around 1.1m for which around 70 percent of the signal makes it through.
