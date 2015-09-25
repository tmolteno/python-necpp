# python-necpp: Antenna simulation in python

This module allows you to do antenna simulations in Python using the nec2++ antenna
simulation package. This is a wrapper using SWIG of the C interface, so the syntax
is quite simple. Have a look at the file necpp_src/example/test.py, for an example of how this 
library can be used.

Tim Molteno. tim@physics.otago.ac.nz

## NEWS

* Version 1.7.0 includes support for getting elements of radiation patterns. At the moment
  this is just through the function nec_get_gain().
* Version 1.7.0.3 includes nec_medium_parameters(). You could simulate an antenna in seawater!


## Install

As of version 1.6.1.2 swig is no longer required for installation. Simply use PIP as 
follows:

    pip install necpp

## Documentation

Try help(necpp) to list the available functions. The functions available are documented in the C-style API of nec2++. 
This is [available here](http://tmolteno.github.io/necpp/libnecpp_8h.html)

## Using

The following code calculates the impedance of a simple vertical monopole antenna
over a perfect ground. 

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
      handle_nec(necpp.nec_ex_card(nec, 0, 0, 1, 0, 1.0, 0, 0, 0, 0, 0)) 
      handle_nec(necpp.nec_rp_card(nec, 0, 90, 1, 0,5,0,0, 0, 90, 1, 0, 0, 0))
      result_index = 0
      
      z = complex(necpp.nec_impedance_real(nec,result_index), 
                  necpp.nec_impedance_imag(nec,result_index))
      
      necpp.nec_delete(nec)
      return z

    if (__name__ == 'main'):
      z = impedance(frequency = 34.5, z0 = 0.5, height = 4.0)
      print "Impedance \t(%6.1f,%+6.1fI) Ohms" % (z.real, z.imag)

## More Information
      
Have a look at [http://github.com/tmolteno/necpp] for more information on using nec2++.
