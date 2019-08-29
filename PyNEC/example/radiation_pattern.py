#
#  Simple vertical monopole antenna simulation using python-necpp
#  pip install necpp
#
from PyNEC import *

import math

def geometry(freq, base, length):
    conductivity = 1.45e6 # Stainless steel
    ground_conductivity = 0.002
    ground_dielectric = 10

    wavelength = 3e8/(1e6*freq)
    n_seg = int(math.ceil(50*length/wavelength))

    #nec = context_clean(nec_context())
    nec = nec_context()

    geo = nec.get_geometry()
    geo.wire(1, n_seg, 0, 0, base, 0, 0, base+length, 0.002, 1.0, 1.0)
    nec.geometry_complete(1)

    nec.ld_card(5, 0, 0, 0, conductivity, 0.0, 0.0)
    nec.gn_card(0, 0, ground_dielectric, ground_conductivity, 0, 0, 0, 0)
    nec.fr_card(0, 1, freq, 0)

    # Voltage excitation one third of the way along the wire
    nec.ex_card(0, 0, int(n_seg/3), 0, 1.0, 0, 0, 0, 0, 0)

    return nec

nec = geometry(freq=123.4, base=0.5, length=4.0)
nec.rp_card(calc_mode=0, n_theta=30, n_phi=30, output_format=0, normalization=0, D=0, A=0, theta0=0, delta_theta=10, phi0=0, delta_phi=5, radial_distance=0, gain_norm=0)
nec.xq_card(0) # Execute simulation

ipt = nec.get_input_parameters(0)
z = ipt.get_impedance()
print(("Impedance is {}".format(z)))

rpt = nec.get_radiation_pattern(0)

complex_e_field = rpt.get_e_theta()
e = complex_e_field.reshape((30,30))

print((complex_e_field.size))

for t in range(30):
    for p in range(30):
        pass
        print(e[t, p])

print(dir(rpt))
