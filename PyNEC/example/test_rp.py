

from PyNEC import *

#creation of a nec context
context=nec_context()
context.initialize()

#get the associated geometry
geo = context.get_geometry()

#add wires to the geometry
geo.wire(0, 36, 0, 0, 0, -0.042, 0.008, 0.017, 0.001, 1.0, 1.0)

#end of the geometry input
context.geometry_complete(0)

#add a "gn" card to specify the ground parameters
context.gn_card(-1, 0, 0, 0, 0, 0, 0, 0)

#add a "ex" card to specify an excitation
context.ex_card(1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0)

#add a "fr" card to specify the frequency 
context.fr_card(0, 2, 2400.0e6, 100.0e6)

#add a "rp" card to specify radiation pattern sampling parameters and to cause program execution
context.rp_card(0, 3, 2, 0, 5, 0, 0, 90.0, 90.0, 10.0, 10.0, 1.0, 0.0)

#get the radiation_pattern
rp = context.get_radiation_pattern(0)
print rp.get_delta_phi()
print rp.get_gain()

print dir(rp)
