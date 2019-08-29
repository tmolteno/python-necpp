#
#  Automatically tune antenna
#
import argparse
import scipy.optimize
import numpy as np

import monopole
from antenna_util import reflection_coefficient

# A function that will be minimized when the impedance is 50 Ohms
# We convert the height and antenna length to positive
# numbers using exp. because otherwise the antenna will lie
# below ground and cause an error in simulation.
def target(x):
    global freq, target_impedance
    base_height = np.exp(x[0]) # Make it positive
    length = np.exp(x[1])  # Make it positive
    if (length > 10.0):
        return 100
    try:
        z = monopole.impedance(freq, base_height, length)
        return reflection_coefficient(z, z0=target_impedance)
    except RuntimeError as re:
        return 100

def print_result(x, f, accepted):
    log_base, log_length = x
    base_height = np.exp(log_base)
    length = np.exp(log_length)

    if accepted:
       print("Optimium base_height=%fm, h=%fm, impedance=%s Ohms" % \
        (base_height, length, monopole.impedance(freq, base_height, length)))
    else:
       print("Local_minimum=%fm, h=%fm, impedance=%s Ohms" % \
        (base_height, length, monopole.impedance(freq, base_height, length)))

if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Optimize a monopole antenna.')
    parser.add_argument('--target-impedance', type=float, default=50.0, help='Target for the optimized impedance')
    parser.add_argument('--basinhopping', action="store_true", help='Use basinhopping')
    args = parser.parse_args()

    # Starting value 
    freq = 134.5
    x0 = [-2.0, 1.0]
    target_impedance = args.target_impedance
    
    # Carry out the minimization

    if args.basinhopping:
        result = scipy.optimize.basinhopping(target, x0, disp=True, T=1.0, niter_success=10)
    else:
        result = scipy.optimize.minimize(target, x0, method='Nelder-Mead')
    
    print("")
    print("***********************************************************************")
    print("*                           OPTIMIZATION COMPLETED                    *")
    print("***********************************************************************")
    print_result(result.x, None, True)
