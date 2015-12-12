import numpy as np
import scipy.optimize
import matplotlib.pyplot as plt
import matplotlib as mpl

from PyNEC import *
from antenna_util import *

from context_clean import *

import math

""" Optimize and plot the gains/VSWR of a logperiodic antenna (6 brass elements, 75 Ohm transmission lines) for both the 2.4GHz as the 5.8GHz ISM bands.
    Inspired by an excercise for a course, hence the weird constraints. """

brass_conductivity = 15600000 # mhos

tl_impedance = 75

def geometry_logperiodic(l_1, x_1, tau):
  """
      x_1 is the distance from the origin to the largest (farthest away) dipole, which has a length of l_1.
      The spacing is as follows: l_{i+1}/l_i = tau = x_{i+1}/x_i
  """
  wire_radius = 0.00025 # 0.25 mm

  # alpha = np.arctan( (l_1/2.0) / x_1 )

  nec = context_clean(nec_context())
  nec.set_extended_thin_wire_kernel(True)

  geo = geometry_clean(nec.get_geometry())

  # Dipoles should be oriented in the Z direction; they should be placed on the (positive) X axis

  x_i = x_1
  l_i = x_1
  
  # As ususal, note that nec tags start at 1, and we typically index from 0!
  dipole_center_segs = {} # Maps from NEC wire id!
  
  dipoles_count = 5

  for dipole_tag in range(1, dipoles_count + 1):
      nr_segments = int(math.ceil(50*l_i/wavelength)) # TODO this might vary when sweeping even!
      #print nr_segments

      dipole_center_segs[dipole_tag] = nr_segments / 2 + 1

      center      = np.array([x_i, 0, 0])
      half_height = np.array([0  , 0, l_i/2.0])
      top         = center + half_height
      bottom      = center - half_height

      geo.wire(tag_id=dipole_tag, nr_segments=nr_segments, src=bottom, dst=top, radius=wire_radius)

      x_i = tau * x_i
      l_i = tau * l_i

  # Everything is in brass
  nec.set_wire_conductivity(brass_conductivity)

  nec.geometry_complete(ground_plane=False)

  # The 6th tag is the smallest tag is the source element
  for dipole in range(0, dipoles_count - 1):
      src_tag = 1 + dipole # NEC indexing
      src_seg = dipole_center_segs[src_tag]

      dst_tag = src_tag + 1
      dst_seg = dipole_center_segs[dst_tag]

      nec.transmission_line((src_tag, src_seg), (dst_tag, dst_seg), tl_impedance, crossed_line=True)

  smallest_dipole_tag = dipoles_count # Again, start at 1

  nec.voltage_excitation(wire_tag=smallest_dipole_tag, segment_nr=dipole_center_segs[smallest_dipole_tag], voltage=1.0)

  return nec

start = 2300
stop  = 5900
count = stop - start


def get_gain_swr_range(l_1, x_1, tau, start=start, stop=stop, step=10):
    gains_db = []
    frequencies = []
    vswrs = []
    for freq in range(start, stop + 1, step):
        nec = geometry_logperiodic(l_1, x_1, tau)
        nec.set_frequency(freq) # TODO: ensure that we don't need to re-generate this!
        nec.radiation_pattern(thetas=Range(90, 90, count=1), phis=Range(180,180,count=1))

        rp = nec.context.get_radiation_pattern(0)
        ipt = nec.get_input_parameters(0)
        z = ipt.get_impedance()

        # Gains are in decibels
        gains_db.append(rp.get_gain()[0])
        vswrs.append(vswr(z, system_impedance))
        frequencies.append(ipt.get_frequency())

    return frequencies, gains_db, vswrs

def create_optimization_target():
  def target(args):
      l_1, x_1, tau = args
      if l_1 <= 0 or x_1 <= 0 or tau <= 0:
          return float('inf')

      try:
        result = 0

        vswr_score = 0
        gains_score = 0

        for range_low, range_high in [ (2400, 2500), (5725, 5875) ]:
            freqs, gains, vswrs = get_gain_swr_range(l_1, x_1, tau, start=range_low, stop=range_high)

            for gain in gains:
                gains_score += gain
            for vswr in vswrs:
                if vswr >= 1.8:
                    vswr = np.exp(vswr) # a penalty :)
                vswr_score += vswr

        # VSWR should minimal in both bands, gains maximal:
        result = vswr_score - gains_score

      except:
          print "Caught exception"
          return float('inf')

      print result

      return result
  return target


def simulate_and_get_impedance(nec):
  nec.set_frequency(design_freq_mhz)

  nec.xq_card(0)

  index = 0
  return nec.get_input_parameters(index).get_impedance()

system_impedance = 50 # This makes it a bit harder to optimize, given the 75 Ohm TLs, which is good for this excercise of course...

# (2.4 GHz to 2.5 GHz) and the 5.8 GHz ISM band (5.725 GHz to 5.875 GHz)

design_freq_mhz = 2450 # The center of the first range
wavelength = 299792e3/(design_freq_mhz*1000000)

majorLocator = mpl.ticker.MultipleLocator(10)
majorFormatter = mpl.ticker.FormatStrFormatter('%d')
minorLocator = mpl.ticker.MultipleLocator(1)
minorFormatter = mpl.ticker.FormatStrFormatter('%d')

def draw_frequencie_ranges(ax):
    ax.axvline(x=2400, color='red', linewidth=1)
    ax.axvline(x=2500, color='red', linewidth=1)
    ax.axvline(x=5725, color='red', linewidth=1)
    ax.axvline(x=5875, color='red', linewidth=1)

def show_report(l1, x1, tau):
    nec = geometry_logperiodic(l1, x1, tau)

    z = simulate_and_get_impedance(nec)

    print "Initial impedance: (%6.1f,%+6.1fI) Ohms" % (z.real, z.imag)
    print "VSWR @ 50 Ohm is %6.6f" % vswr(z, 50)

    nec = geometry_logperiodic(l1, x1, tau)
  
    freqs, gains, vswrs = get_gain_swr_range(l1, x1, tau, step=5)

    freqs = np.array(freqs) / 1000000 # In MHz
  
    ax = plt.subplot(111)
    ax.plot(freqs, gains)
    draw_frequencie_ranges(ax)

    ax.set_title("Gains of a 5-element log-periodic antenna")
    ax.set_xlabel("Frequency (MHz)")
    ax.set_ylabel("Gain")

    ax.yaxis.set_major_locator(majorLocator)
    ax.yaxis.set_major_formatter(majorFormatter)

    ax.yaxis.set_minor_locator(minorLocator)
    ax.yaxis.set_minor_formatter(minorFormatter)

    ax.yaxis.grid(b=True, which='minor', color='0.75', linestyle='-')

    plt.show()

    ax = plt.subplot(111)
    ax.plot(freqs, vswrs)
    draw_frequencie_ranges(ax)

    ax.set_yscale("log")
    ax.set_title("VSWR of a 6-element log-periodic antenna @ 50 Ohm impedance")
    ax.set_xlabel("Frequency (MHz)")
    ax.set_ylabel("VSWR")

    ax.yaxis.set_major_locator(majorLocator)
    ax.yaxis.set_major_formatter(majorFormatter)
    ax.yaxis.set_minor_locator(minorLocator)
    ax.yaxis.set_minor_formatter(minorFormatter)
  
    ax.yaxis.grid(b=True, which='minor', color='0.75', linestyle='-')
    plt.show()


if (__name__ == '__main__'):
  initial_l1  = wavelength / 2
  initial_x1  = wavelength / 2
  initial_tau = 0.8

  print "Wavelength is %0.4fm, initial length is %0.4fm" % (wavelength, initial_l1)
  
  print "Unoptimized antenna..."
  show_report(initial_l1, initial_x1, initial_tau)

  print "Optimizing antenna..."
  target = create_optimization_target()

  # Optimize local minimum only with gradient desce
  #optimized_result = scipy.optimize.minimize(target, np.array([initial_l1, initial_x1, initial_tau]), method='Nelder-Mead')

  # Use differential evolution:
  minimizer_kwargs = dict(method='Nelder-Mead')
  bounds = [ (0.01, 0.2), (0.01, 0.2), (0.7, 0.9) ]
  optimized_result = scipy.optimize.differential_evolution(target, bounds, seed=42, disp=True, popsize=20)

  # Basin hopping isn't so good, but could also have been an option:
  #optimized_result = scipy.optimize.basinhopping(target, np.array([initial_l1, initial_x1, initial_tau]), minimizer_kwargs=minimizer_kwargs, niter=5, stepsize=0.015, T=2.0, disp=True)

  print "Optimized antenna..."
  optimized_l1, optimized_x1, optimized_tau =  optimized_result.x[0], optimized_result.x[1], optimized_result.x[2]
  show_report(optimized_l1, optimized_x1, optimized_tau)

