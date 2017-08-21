from PyNEC import *


import unittest

class TestDipoleGain(unittest.TestCase):


  def test_example4(self):
    '''
    CEEXAMPLE 4. T ANTENNA ON A BOX OVER PERFECT GROUND
    SP 0 0 .1 .05 .05 0. 0. .01
    SP 0 0 .05 .1 .05 0. 90. .01
    GX 0 110
    SP 0 0 0. 0. .1 90. 0. .04
    GW 1 4 0. 0. .1 0. 0. .3 .001
    GW 2 2 0. 0. .3 .15 0. .3 .001
    GW 3 2 0. 0. .3 -.15 0. .3 .001
    GE 1
    GN 1
    EX 0 1 1 0 1.
    RP 0 10 4 1001 0. 0. 10. 30.
    EN
    '''
    nec = nec_create()
    nec.sp_card(0, 0.1, 0.05, 0.05, 0.0, 0.0, 0.01)
    nec.sp_card(0, .05, .1, .05, 0.0, 90.0, 0.01)
    nec.gx_card(0, 110)
    nec.sp_card(0, 0.0, 0.0, 0.1, 90.0, 0.0, 0.04)
    
    nec.wire(1, 4, 0., 0.0, 0.1, 0.0,  0.0, 0.3, .001, 1.0, 1.0)
    nec.wire(2, 2, 0., 0.0, 0.3, 0.15, 0.0, 0.3, .001, 1.0, 1.0)
    nec.wire(3, 2, 0., 0.0, 0.3, -.15, 0.0, 0.3, .001, 1.0, 1.0)

    nec.geometry_complete(1)
    nec.gn_card(1, 0, 0, 0, 0, 0, 0, 0)
    
    nec.ex_card(0, 1, 1, 0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0)
    nec.rp_card(0,10,4,1,0,0,1,0.0,0.0,10.0,30.0, 0, 0)
    
    self.assertAlmostEqual(nec_gain_max(nec,0),5.076,3)
    
    gmax = -999.0
    
    for theta_index in range(0,10):
      for phi_index in range(0,4):
        g = nec_gain(nec,0,theta_index, phi_index)
        gmax = max(g, gmax)
        
    self.assertAlmostEqual(gmax, nec_gain_max(nec,0), 5 )

    nec_delete(nec)
    

if __name__ == '__main__':
  unittest.main()
