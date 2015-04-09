#
#  Simple vertical monopole antenna simulation using python-necpp
#  pip install necpp
#
import necpp

def handle_nec(result):
  if (result != 0):
    print necpp.nec_error_message()

def geometry(frequency, base_height, length):
  
  conductivity = 1.45e6 # Stainless steel
  ground_conductivity = 0.002
  ground_dielectric = 10
  wavelength = 3e8/(1e6*frequency)
  segments_per_meter = 50.0 / wavelength
  
  n_segments = int(length*segments_per_meter + 0.5)
  nec = necpp.nec_create()
  handle_nec(necpp.nec_wire(nec, 1, n_segments, 0, 0, base_height, 0, 0, base_height+length, 0.002, 1.0, 1.0))
  handle_nec(necpp.nec_geometry_complete(nec, 1, 0))
  handle_nec(necpp.nec_ld_card(nec, 5, 0, 0, 0, conductivity, 0.0, 0.0))
  handle_nec(necpp.nec_gn_card(nec, 0, 0, ground_dielectric, ground_conductivity, 0, 0, 0, 0))
  handle_nec(necpp.nec_fr_card(nec, 0, 1, frequency, 0))
  handle_nec(necpp.nec_ex_card(nec, 0, 0, n_segments/3, 0, 1.0, 0, 0, 0, 0, 0)) # Voltage excitation in segment 1
  return nec

def impedance(frequency, base_height, length):
  nec = geometry(frequency, base_height, length)
  handle_nec(necpp.nec_xq_card(nec, 0)) # Execute simulation
  result_index = 0
  z = complex(necpp.nec_impedance_real(nec,result_index), necpp.nec_impedance_imag(nec,result_index))
  necpp.nec_delete(nec) # Clean up the nec object
  return z

if (__name__ == '__main__'):
  z = impedance(frequency = 134.5, base_height = 0.5, length = 4.0)
  print "Impedance at base_height=%0.2f, length=%0.2f : (%6.1f,%+6.1fI) Ohms" % (0.5, 4.0, z.real, z.imag)
