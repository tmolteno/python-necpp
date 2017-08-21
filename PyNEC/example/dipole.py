import numpy as np
import scipy.optimize
import pylab as plt


from PyNEC import *
from antenna_util import *

from context_clean import *

import math

def geometry(freq_mhz, length, nr_segments):
  wire_radius = 0.01e-3 # 0.01 mm

  nec = context_clean(nec_context())
  nec.set_extended_thin_wire_kernel(False)

  geo = geometry_clean(nec.get_geometry())
  
  center = np.array([0,0,0])
  half   = np.array([length/2, 0, 0])

  pt1 = center - half
  pt2 = center + half

  wire_tag = 1
  geo.wire(tag_id=wire_tag, nr_segments=nr_segments, src=pt1, dst=pt2, radius=wire_radius)

  nec.geometry_complete(ground_plane=False)

  nec.set_frequency(freq_mhz)

  # Voltage excitation in the center of the antenna
  nec.voltage_excitation(wire_tag=wire_tag, segment_nr=int(nr_segments/2), voltage=1.0)

  return nec

def impedance(freq_mhz, length, nr_segments):
  nec = geometry(freq_mhz, length, nr_segments)
  nec.xq_card(0)

  index = 0
  return nec.get_input_parameters(index).get_impedance()

def create_optimization_target(freq_mhz, nr_segments):
  def target(length):
      return abs(impedance(freq_mhz, length[0], nr_segments).imag)
  return target

# It's probably possible that the antenna matches in multiple regions, pick the one around the center frequency...
def matched_range_around(nec, count, center_freq, system_impedance):
    # TODO: this is not ideal
    min_dist = float('inf')
    min_idx = None
    target_hz = center_freq * 1000000

    for idx in range(0, count):
        dist = abs(nec.get_input_parameters(idx).get_frequency() - target_hz)
        if dist < min_dist:
            min_dist = dist
            min_idx = idx

    idx = min_idx
    matched_min_freq = None
    while idx >= 0:
        ipt = nec.get_input_parameters(idx)
        z = ipt.get_impedance()
        if vswr(z, system_impedance) > 2:
            break
        matched_min_freq = ipt.get_frequency() / 1000000
        idx -= 1

    idx = min_idx
    matched_max_freq = None
    while idx < count:
        ipt = nec.get_input_parameters(idx)
        z = ipt.get_impedance()
        if vswr(z, system_impedance) > 2:
            break
        matched_max_freq = ipt.get_frequency() / 1000000
        idx += 1

    return (matched_min_freq, matched_max_freq)

if (__name__ == '__main__'):
  design_freq_mhz = 2450
  wavelength = 299792e3/(design_freq_mhz*1000000)

  initial_length = wavelength / 2 # TODO

  print "Wavelength is %0.4fm, initial length is %0.4fm" % (wavelength, initial_length)

  nr_segments = 101 # int(math.ceil(50*initial_length/wavelength))

  z = impedance(design_freq_mhz, initial_length, nr_segments)

  print "Initial impedance: (%6.1f,%+6.1fI) Ohms" % (z.real, z.imag)

  target = create_optimization_target(design_freq_mhz, nr_segments)
  optimized_result = scipy.optimize.minimize(target, np.array([initial_length]))
  optimized_length = optimized_result.x[0]

  z = impedance(design_freq_mhz, optimized_length, nr_segments)

  print "Optimized length %6.6f m, which gives an impedance of: (%6.4f,%+6.4fI) Ohms" % (optimized_length, z.real, z.imag)
  print "VSWR @ 75 Ohm is %6.6f" % vswr(z, 75)

  for system_impedance in [75, 50, 300]:
    nec = geometry(design_freq_mhz, optimized_length, nr_segments)

    count = 300
    nec.set_frequencies_linear(2300, 2600, count=count)
    nec.xq_card(0) # Execute simulation

    # TODO: add get_n_items to nec_antenna_input and co, so we can automatically deduce count etc. Much cleaner

    rng = matched_range_around(nec, count, design_freq_mhz, system_impedance)
    if rng[0] is None or rng[1] is None:
        print "VSWR is nowhere <= 2 @ %i Ohm!" % system_impedance
    else:
        bandwidth = 100.0 * (rng[1] - rng[0]) / design_freq_mhz
        print "The fractional bandwidth @ %i Ohm is %2.2f%% - %i MHz (%i Mhz to %i MHz)" % (system_impedance, bandwidth, (rng[1] - rng[0]), rng[0], rng[1])

    freqs = []
    vswrs = []
    for idx in range(0, count):
        ipt = nec.get_input_parameters(idx)
        z = ipt.get_impedance()

        freqs.append(ipt.get_frequency() / 1000000)
        vswrs.append(vswr(z, system_impedance))
        
        # print "%i MHz, Z = %6.6f @ %i" % (ipt.get_frequency(), vswr(z, system_impedance), system_impedance)

    plt.figure()
    plt.plot(freqs, vswrs)
    plt.title("VSWR of a %.2f mm long dipole for a %i Ohm system" % (optimized_length * 1000.0, system_impedance))
    plt.xlabel("Frequency (MHz)")
    plt.ylabel("VSWR")
    plt.grid(True)
    filename = "vswr_%i_MHz.pdf" % system_impedance
    print "Saving plot to file: %s" % filename
    plt.savefig(filename)
