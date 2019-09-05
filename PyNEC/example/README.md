# PyNEC examples

This folder contains some examples showing the use of PyNEC antenna simulation module 

## Optimizing a Monopole

The file monopole.py simulates a monopole antenna, printing out the impedance. To optimize this 

    python3 monopole.py 
    
To optimize the monopole design to achieve a particular impedance, try

    python3 optimized.py --basinhopping --target-impedance=110

This code uses standard scipy optimizers to find the best solution.
