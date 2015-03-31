# python-necpp: Antenna simulation in python

PyPI module for nec2++

This module allows you to do antenna simulations in Python using the nec2++ antenna
simulation package. This is a wrapper using SWIG of the C interface, so the syntax
is quite simple. Have a look at the file test.py, for an example of how this 
library can be used.

### Author

Tim Molteno. tim@physics.otago.ac.nz

## Install

    pip install necpp

## Using

    #
    #  Simple vertical monopole antenna simulation using python-necpp
    #  pip install necpp
    #
    import necpp

    def handle_nec(result):
      if (result != 0):
        print necpp.nec_error_message()

    def impedance(frequency, z0, height):
      
      nec = necpp.nec_create()
      handle_nec(necpp.nec_wire(nec, 1, 17, 0, 0, z0, 0, 0, z0+height, 0.1, 1, 1))
      handle_nec(necpp.nec_geometry_complete(nec, 1, 0))
      handle_nec(necpp.nec_gn_card(nec, 1, 0, 0, 0, 0, 0, 0, 0))
      handle_nec(necpp.nec_fr_card(nec, 0, 1, frequency, 0))
      handle_nec(necpp.nec_ex_card(nec, 0, 0, 1, 0, 1.0, 0, 0, 0, 0, 0)) # Voltage excitation in segment 1
      handle_nec(necpp.nec_rp_card(nec, 0, 90, 1, 0,5,0,0, 0, 90, 1, 0, 0, 0))
      result_index = 0
      
      z = complex(necpp.nec_impedance_real(nec,result_index), necpp.nec_impedance_imag(nec,result_index))
      
      necpp.nec_delete(nec)
      return z

    if (__name__ == 'main'):
      z = impedance(frequency = 34.5, z0 = 0.5, height = 4.0)
      print "Impedance \t(%6.1f,%+6.1fI) Ohms" % (z.real, z.imag)

## More Information
      
Have a look at [http://github.com/tmolteno/necpp] for more information on nec2++.
