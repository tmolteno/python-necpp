import numpy as np
import scipy.optimize
import matplotlib.pyplot as plt
import matplotlib as mpl


from PyNEC import *
from antenna_util import *

from context_clean import *

import math

brass_conductivity = 15600000 # mhos

""" Optimize and plot the gains/VSWR of a simple monopole antenna, that has some brass wires added that act as ground. Visualises the path in the search space explored
    by the minimization algorithm.
    Inspired by an excercise for a course on antennas. The constraints are thus not really ideal I think... """

# TODO: this probably could also be done by the GN/GD cards, but am I allowed?
def add_ground_screen(geo, start_tag, length):
    # The ground is modeled 6 radial wires (brass, radius 1 mm), equally spaced by 2pi/6, and their initial length is d = 2 cm

    src = np.array([0, 0, 0])
    radius = 0.001
    
    for i in range(0, 6):
        angle = i * (2*np.pi/6.0)
        dst = np.array([length * np.cos(angle), length * np.sin(angle), 0])
        # TODO: nr_segments (actually, more TODO: if nr_segments>=9, the geometry is invalid with this wire radius!)
        geo.wire(tag_id=start_tag+i, nr_segments=5, src=src, dst=dst, radius=radius) # TODO: nr_segments

def geometry_monopole_ground(freq_mhz, monopole_length, ground_wire_length, nr_segments):
  wire_radius = 0.0005 # 0.5 mm

  nec = context_clean(nec_context())
  nec.set_extended_thin_wire_kernel(True)

  geo = geometry_clean(nec.get_geometry())
  
  bottom = np.array([0, 0, 0])
  top    = np.array([0, 0, monopole_length])

  wire_tag = 1
  geo.wire(tag_id=wire_tag, nr_segments=nr_segments, src=bottom, dst=top, radius=wire_radius)

  add_ground_screen(geo, start_tag=2, length=ground_wire_length)

  # Everything is in brass
  nec.set_wire_conductivity(brass_conductivity)

  nec.geometry_complete(ground_plane=False) # We added our own 'ground plane'

  nec.voltage_excitation(wire_tag=wire_tag, segment_nr=1, voltage=1.0)

  return nec

def simulate_and_get_impedance(nec):
  nec.set_frequency(design_freq_mhz)

  nec.xq_card(0)

  index = 0
  return nec.get_input_parameters(index).get_impedance()

# TODO: perhaps the length <= 0 can be added through additional constraints to minimize?

design_freq_mhz = 2595
lte_high_band = [2500, 2690]
system_impedance = 50

sampled_monopole_lenths = []
sampled_ground_wire_lenths = []
sampled_results = []

def create_optimization_target(freq_mhz, nr_segments):
  def target(args):
      monopole_length, ground_wire_length = args[0], args[1]
      if monopole_length <= 0 or ground_wire_length <= 0:
          return float('inf')
      
      result = 0
      # VSWR should be < 2 in the lte_high_band
      # So let's just sum (for now, TODO) the surplus for all the VSWRs that exceed it:
      low = lte_high_band[0]
      high = lte_high_band[1]
      count = high-low

      try:
        nec = geometry_monopole_ground(design_freq_mhz, monopole_length, ground_wire_length, nr_segments)
        nec.set_frequencies_linear(low, high, count=count)

        nec.xq_card(0) # Execute simulation
      except:
          print("Caught exception")
          return float('inf')

      for idx in range(0, count):
        ipt = nec.get_input_parameters(idx)
        z = ipt.get_impedance()
        s = vswr(z, system_impedance)
        if s > 2:
            result += s - 2

      # And then maximize the gain in the horizontal plane (theta = pi/2 (90))
      # TODO: might this be possible in one step?
      gains_db = []
      for freq in range(low, high+1):
          nec = geometry_monopole_ground(design_freq_mhz, monopole_length, ground_wire_length, nr_segments)

          nec.set_frequency(freq)
          nec.radiation_pattern(thetas=Range(-90, -90, count=1), phis=Range(90,90,count=1))
          rp = nec.context.get_radiation_pattern(0)

          gains_db.append(rp.get_gain()[0][0])

      #print gains_db
      result -= np.exp(max(gains_db)) # maximize gain, hence the minus

      global sampled_monopole_lenths, sampled_ground_wire_lenths, sampled_results
      sampled_monopole_lenths.append(monopole_length)
      sampled_ground_wire_lenths.append(ground_wire_length)
      sampled_results.append(result)

      print(result)

      return result
  return target

if (__name__ == '__main__'):
  
  wavelength = 299792e3/(design_freq_mhz*1000000)

  initial_length = wavelength / 4 # quarter-wavelength monopole

  print("Wavelength is %0.4fm, initial length is %0.4fm" % (wavelength, initial_length))

  nr_segments = 15 # int(math.ceil(50*initial_length/wavelength))
  #print nr_segments

  ground_wire_length = 0.02
  z = simulate_and_get_impedance(geometry_monopole_ground(design_freq_mhz, initial_length, ground_wire_length, nr_segments))

  print("Initial impedance: (%6.1f,%+6.1fI) Ohms" % (z.real, z.imag))
  print("VSWR @ 50 Ohm is %6.6f" % vswr(z, 50))

  target = create_optimization_target(design_freq_mhz, nr_segments)
  optimized_result = scipy.optimize.minimize(target, np.array([initial_length, ground_wire_length]), method='Nelder-Mead')

  optimized_length, optimized_ground_wire_length = optimized_result.x[0], optimized_result.x[1]

  geo_opt = geometry_monopole_ground(design_freq_mhz, optimized_length, optimized_ground_wire_length, nr_segments)
  z = simulate_and_get_impedance(geo_opt)

  print("Optimized length %6.6f m and ground screen radials of length %6.6f m, which gives an impedance of: (%6.4f,%+6.4fI) Ohms" % (optimized_length, optimized_ground_wire_length, z.real, z.imag))
  print("Mismatch @ 50 Ohm is %6.6f" % mismatch(z, 50))
  print("VSWR @ 50 Ohm is %6.6f" % vswr(z, 50))

  geo_opt = geometry_monopole_ground(design_freq_mhz, optimized_length, optimized_ground_wire_length, nr_segments)
  geo_opt.set_frequency(design_freq_mhz)
  geo_opt.radiation_pattern(thetas=Range(-90, 90, count=180), phis=Range(0,0,count=1))

  #get the radiation_pattern
  rp = geo_opt.context.get_radiation_pattern(0)

  # Gains are in decibels
  gains_db = rp.get_gain()[:,0] # Is an array of theta,phi -> gain. In this case we only have one phi
  thetas = rp.get_theta_angles() * 3.1415 / 180.0
  phis = rp.get_phi_angles() * 3.1415 / 180.0

  max_idx = gains_db.argmax()
  max_gain = gains_db[max_idx]
  max_theta = thetas[max_idx]
  #print gains_db
  print("Maximal gain is %2.2f dBi, at an angle of %2.2f" % (max_gain, max_theta * 180.0 / np.pi))

  # Plot stuff

  ax = plt.subplot(111, polar=True)

  ax.plot(thetas, gains_db, color='r', linewidth=3)
  ax.set_xticks(np.pi/180. * np.linspace(180,  -180, 8, endpoint=False))
  ax.set_theta_zero_location("N")
  ax.set_rlim((-24.0, 9.0)) # TODO: automate. TODO: 4nec2 cheats and makes the lowest points (-999) the same as the lowest non-999 point :)
  ax.set_rticks(np.linspace(-24, 9, 10, endpoint=False))
  ax.grid(True)

  ax.set_title("Gain pattern in the vertical plane", va='bottom')
  plt.show()


  low = lte_high_band[0]
  high = lte_high_band[1]
  count = high-low

  # Reset the geometry, so that there is no spurious FR card left. (TODO this should really be not necessary)
  geo_opt = geometry_monopole_ground(design_freq_mhz, optimized_length, optimized_ground_wire_length, nr_segments)
  geo_opt.set_frequencies_linear(low, high, count=count)
  geo_opt.xq_card(0) # Execute simulation

  freqs = []
  vswrs = []
  for idx in range(0, count):
    ipt = geo_opt.get_input_parameters(idx)
    z = ipt.get_impedance()

    freqs.append(ipt.get_frequency() / 1000000)
    vswrs.append(vswr(z, system_impedance))

  ax = plt.subplot(111)
  ax.plot(freqs, vswrs)
  ax.set_xlabel("Frequency (MHz)")
  ax.set_ylabel("VSWR")
  ax.grid(True)
  plt.show()

  ax = plt.subplot(111)
  #print sampled_monopole_lenths
  #print sampled_ground_wire_lenths
  sampled_results = np.log(4 + np.array(sampled_results))
  #print sampled_results
  norm = mpl.colors.Normalize(vmin=min(sampled_results), vmax=max(sampled_results))
  plt.scatter(sampled_monopole_lenths, sampled_ground_wire_lenths, c=sampled_results, cmap=mpl.cm.cool, norm=norm, edgecolors='None', alpha=0.75)
  ax.set_title("Optimization path")
  plt.colorbar()
  plt.show()

