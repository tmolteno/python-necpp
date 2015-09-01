#
#  Simple vertical monopole antenna simulation using python-necpp
#  pip install necpp
#
from necpp import *
import math

def handle_nec(result):
  if (result != 0):
    print nec_error_message()

def geometry(freq, base, length):
  
  conductivity = 1.45e6 # Stainless steel
  ground_conductivity = 0.002
  ground_dielectric = 10
<<<<<<< HEAD
  wavelength = 3e8/(1e6*frequency)
  segments_per_meter = 50.0 / wavelength
  
  n_segments = (int(length*segments_per_meter + 0.5)/2)*2 + 1
  print n_segments
  
  nec = necpp.nec_create()
  handle_nec(necpp.nec_wire(nec, 1, n_segments, 0, 0, base_height, 0, 0, base_height+length, 0.002, 1.0, 1.0))
  handle_nec(necpp.nec_geometry_complete(nec, 1, 0))
  handle_nec(necpp.nec_ld_card(nec, 5, 0, 0, 0, conductivity, 0.0, 0.0))
  handle_nec(necpp.nec_gn_card(nec, 0, 0, ground_dielectric, ground_conductivity, 0, 0, 0, 0))
  handle_nec(necpp.nec_fr_card(nec, 0, 1, frequency, 0))
  handle_nec(necpp.nec_ex_card(nec, 0, 0, n_segments/2 + 1, 0, 1.0, 0, 0, 0, 0, 0)) # Voltage excitation in segment 1
=======

  wavelength = 3e8/(1e6*freq)
  n_seg = int(math.ceil(50*length/wavelength))
  nec = nec_create()
  handle_nec(nec_wire(nec, 1, n_seg, 0, 0, base, 0, 0, base+length, 0.002, 1.0, 1.0))
  handle_nec(nec_geometry_complete(nec, 1))
  handle_nec(nec_ld_card(nec, 5, 0, 0, 0, conductivity, 0.0, 0.0))
  handle_nec(nec_gn_card(nec, 0, 0, ground_dielectric, ground_conductivity, 0, 0, 0, 0))
  handle_nec(nec_fr_card(nec, 0, 1, freq, 0))
  # Voltage excitation one third of the way along the wire
  handle_nec(nec_ex_card(nec, 0, 0, n_seg/3, 0, 1.0, 0, 0, 0, 0, 0)) 
>>>>>>> f0e7efccfad818e3be039cc91cae14d1c46291ce
  return nec

def impedance(freq, base, length):
  nec = geometry(freq, base, length)
  handle_nec(nec_xq_card(nec, 0)) # Execute simulation
  index = 0
  z = complex(nec_impedance_real(nec,index), nec_impedance_imag(nec,index))
  nec_delete(nec)
  return z

if (__name__ == '__main__'):
  z = impedance(freq = 134.5, base = 0.5, length = 4.0)
  print "Impedance at base=%0.2f, length=%0.2f : (%6.1f,%+6.1fI) Ohms" % (0.5, 4.0, z.real, z.imag)
