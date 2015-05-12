import PyNEC


import unittest

class TestDipoleGain(unittest.TestCase):

  def test_example1(self):
    
    nec= PyNEC.nec_context()

    geo = nec.get_geometry()


    '''
    CE EXAMPLE 1. CENTER FED LINEAR ANTENNA
    GW 0 7 0. 0. -.25 0. 0. .25 .001
    GE
    EX 0 0 4 0 1.
    XQ
    LD 0 0 4 4 10. 3.000E-09 5.300E-11
    PQ
    NE 0 1 1 15 .001 0 0 0. 0. .01786
    EN    
    '''
    geo.wire(0, 7, 0., 0., .75, 0., 0., 1.25, .001, 1.0, 1.0)
    nec.geometry_complete(1)
    nec.ex_card(0, 0, 4,0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0)
    nec.xq_card(0)
    nec.ld_card(0, 0, 4, 4, 10., 3.000E-09, 5.300E-11)
    nec.pq_card(0, 0, 0, 0)
    nec.ne_card(0, 1, 1, 15, .001, 0, 0, 0., 0., .01786)
    nec.xq_card(0)
    
    ipt = nec.get_input_parameters(0)
    z = ipt.get_impedance()
    
    self.assertAlmostEqual(z[0].real,82.69792906662622)
    self.assertAlmostEqual(z[0].imag,46.30603888063429)
    

  def test_example2(self):
    ''' CMEXAMPLE 2. CENTER FED LINEAR ANTENNA. 
        CM           CURRENT SLOPE DISCONTINUITY SOURCE. 
        CM           1. THIN PERFECTLY CONDUCTING WIRE 
        CE           2. THIN ALUMINUM WIRE 
        GW 0 8 0. 0. -.25 0. 0. .25 .00001 
        GE 
        FR 0 3 0 0 200. 50. 
        EX 5 0 5 1 1. 0. 50. 
        XQ 
        LD 5 0 0 0 3.720E+07 
        FR 0 1 0 0 300. 
        EX 5 0 5 0 1. 
        XQ 
        EN
    '''
    nec = PyNEC.nec_context()
    geo = nec.get_geometry()
    geo.wire( 0, 8, 0., 0., -.25, 0., 0., .25, .00001, 1.0, 1.0)
    nec.geometry_complete(0)
    nec.fr_card(0, 3, 200., 50 )
    nec.ex_card(5, 0, 5, 1, 1.0, 0.0, 50.0, 0.0, 0.0, 0.0)
    nec.xq_card(0)

    ipt = nec.get_input_parameters(0)
    z = ipt.get_impedance()

    ''' 
                          ----- ANTENNA INPUT PARAMETERS -----
  TAG   SEG       VOLTAGE (VOLTS)         CURRENT (AMPS)         IMPEDANCE (OHMS)        ADMITTANCE (MHOS)     POWER
  NO.   NO.     REAL      IMAGINARY     REAL      IMAGINARY     REAL      IMAGINARY    REAL       IMAGINARY   (WATTS)
   0     5  1.0000E+00  0.0000E+00  6.6413E-05  1.5794E-03  2.6577E+01 -6.3204E+02  6.6413E-05  1.5794E-03  3.3207E-05
    '''
    self.assertAlmostEqual(z[0].real/26.5762,1.0,4)
    self.assertAlmostEqual(z[0].imag/-632.060,1.0,4)

    nec.ld_card(0, 0, 4, 4, 10., 3.000E-09, 5.300E-11)
    nec.fr_card(0, 3, 200., 50 )
    nec.ex_card(5, 0, 5, 1, 1.0, 0.0, 50.0, 0.0, 0.0, 0.0)
    nec.xq_card(0)

    ipt = nec.get_input_parameters(1)
    z = ipt.get_impedance()
    '''
                          ----- ANTENNA INPUT PARAMETERS -----
      TAG   SEG       VOLTAGE (VOLTS)         CURRENT (AMPS)         IMPEDANCE (OHMS)        ADMITTANCE (MHOS)     POWER
      NO.   NO.     REAL      IMAGINARY     REAL      IMAGINARY     REAL      IMAGINARY    REAL       IMAGINARY   (WATTS)
      0     5  1.0000E+00  0.0000E+00  6.1711E-04  3.5649E-03  4.7145E+01 -2.7235E+02  6.1711E-04  3.5649E-03  3.0856E-04
    ''' 
    self.assertAlmostEqual(z[0].real/47.1431, 1.0, 4)
    self.assertAlmostEqual(z[0].imag/-272.372, 1.0, 3)

     
  def test_example3(self):
    '''
    CMEXAMPLE 3. VERTICAL HALF WAVELENGTH ANTENNA OVER GROUND 
    CM           EXTENDED THIN WIRE KERNEL USED 
    CM           1. PERFECT GROUND 
    CM           2. IMPERFECT GROUND INCLUDING GROUND WAVE AND RECEIVING 
    CE              PATTERN CALCULATIONS 
    GW 0 9 0. 0. 2. 0. 0. 7. .03 
    GE 1 
    EK 
    FR 0 1 0 0 30. 
    EX 0 0 5 0 1. 
    GN 1
    RP 0 10 2 1301 0. 0. 10. 90. 
    GN 0 0 0 0 6. 1.000E-03  
    RP 0 10 2 1301 0. 0. 10. 90. 
    RP 1 10 1 0 1. 0. 2. 0. 1.000E+05 
    EX 1 10 1 0 0. 0. 0. 10.
    PT 2 0 5 5 
    XQ 
    EN
    '''
    nec = PyNEC.nec_context()
    geo = nec.get_geometry()
    geo.wire(0, 9, 0., 0.0, 2.0, 0.0, 0.0, 7.0, 0.03, 1.0, 1.0)
    nec.geometry_complete(1)
    nec.set_extended_thin_wire_kernel(True)
    nec.fr_card(0, 1, 30., 0 )
    nec.ex_card(0, 0, 5, 0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0)
    nec.gn_card(1, 0, 0, 0, 0, 0, 0, 0)
    nec.rp_card(0,10,2,1,3,0,1,0.0,0.0,10.0,90.0, 0, 0)


    ipt = nec.get_input_parameters(0)
    z = ipt.get_impedance()
    
    self.assertAlmostEqual(z[0].real,83.7552291016712)
    self.assertAlmostEqual(z[0].imag,45.32205265591289)
    #self.assertAlmostEqual(nec_gain_max(nec,0),8.393875976328134)
   
    nec.gn_card(0, 0, 6.0, 1.000E-03, 0, 0, 0, 0)
    nec.rp_card(0,10,2,1,3,0,1, 0.0,0.0,10.0,90.0, 0, 0)
    

    ipt = nec.get_input_parameters(1)
    z = ipt.get_impedance()
    
    self.assertAlmostEqual(z[0].real,86.415,3)
    self.assertAlmostEqual(z[0].imag,47.822,3)
    #self.assertAlmostEqual(nec_gain_max(nec,1),1.44837,3)

    nec.rp_card(1,10,1,0,0,0,0, 1.0,0.0,2.0,0.0, 1.000E+05, 0)
    # Not sure what to check here.
    
    nec.ex_card(1, 10, 1, 0, 0.0, 0.0, 0.0, 10.0, 0.0, 0.0)
    nec.pt_card(2, 0, 5, 5)
    # Not sure what to check here.



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
    nec = PyNEC.nec_context()
    geo = nec.get_geometry()
    geo.sp_card(0, 0.1, 0.05, 0.05, 0.0, 0.0, 0.01)
    geo.sp_card(0, .05, .1, .05, 0.0, 90.0, 0.01)
    geo.gx_card(0, 110)
    geo.sp_card(0, 0.0, 0.0, 0.1, 90.0, 0.0, 0.04)
    
    geo.wire(1, 4, 0., 0.0, 0.1, 0.0,  0.0, 0.3, .001, 1.0, 1.0)
    geo.wire(2, 2, 0., 0.0, 0.3, 0.15, 0.0, 0.3, .001, 1.0, 1.0)
    geo.wire(3, 2, 0., 0.0, 0.3, -.15, 0.0, 0.3, .001, 1.0, 1.0)

    nec.geometry_complete(1)
    nec.gn_card(1, 0, 0, 0, 0, 0, 0, 0)
    
    nec.ex_card(0, 1, 1, 0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0)
    nec.rp_card(0,10,4,1,0,0,1,0.0,0.0,10.0,30.0, 0, 0)

    ipt = nec.get_input_parameters(0)
    z = ipt.get_impedance()
    
    #self.assertAlmostEqual(nec_gain_max(nec,0),5.076,3)
    self.assertAlmostEqual(z[0].real,180.727,3)
    self.assertAlmostEqual(z[0].imag,217.654,3)

    

if __name__ == '__main__':
  unittest.main()