#!/usr/bin/env python3
# Copyright (c) 2008-2026 Tim Molteno (tim@elec.ac.nz)
"""
Basic PyNEC usage example — demonstrates:

  1. Creating a dipole antenna with geo.wire()  (Issue #22: wire args)
  2. Getting feedpoint impedance                 (Issue #22: feedpoint impedance)
  3. Getting structure currents                  (Issue #22: segment currents)
  4. Using sc_card with multiple_patch           (Issue #28: SC card)

Run:  python basic_usage.py
"""

import numpy as np
from PyNEC import *

# ── 1. Wire arguments ──────────────────────────────────────────────────
#
# geo.wire(tag_id, segment_count,
#          xw1, yw1, zw1,   # start point (meters)
#          xw2, yw2, zw2,   # end point   (meters)
#          rad,             # wire radius (meters)
#          rdel=1.0,        # segment length ratio (1.0 = uniform)
#          rrad=1.0)        # radius taper ratio   (1.0 = no taper)
#
# Rule of thumb: use 12-20 segments per wavelength.

context = nec_context()
geo = context.get_geometry()

freq_mhz = 300.0  # 300 MHz
wavelength = 300.0 / freq_mhz
length = wavelength / 2  # half-wave dipole
radius = length / 1000

geo.wire(
    tag_id=1,
    segment_count=21,
    xw1=0,
    yw1=-length / 2,
    zw1=0,  # bottom end
    xw2=0,
    yw2=+length / 2,
    zw2=0,  # top end
    rad=radius,
)

context.geometry_complete(0)
context.fr_card(0, 1, freq_mhz, 0)

# Excite segment 11 (center)
context.ex_card(0, 1, 11, 0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0)

# Request radiation pattern (triggers calculation)
context.rp_card(0, 90, 1, 0, 5, 0, 0, 0.0, 90.0, 1.0, 1.0, 0.0, 0.0)


# ── 2. Feedpoint impedance ─────────────────────────────────────────────
#
# get_input_parameters(index) returns a nec_antenna_input object.
# Available methods:
#   .get_impedance()   -> [complex, ...]   impedance at each source
#   .get_current()     -> [complex, ...]   current at each source
#   .get_voltage()     -> [complex, ...]   voltage at each source
#   .get_power()       -> [float, ...]     power at each source
#   .get_frequency()   -> float            frequency in Hz
#   .get_tag()         -> [int, ...]       segment tag numbers
#   .get_segment()     -> [int, ...]       segment numbers

ipt = context.get_input_parameters(0)
Z = ipt.get_impedance()[0]
V = ipt.get_voltage()[0]
I = ipt.get_current()[0]
P = ipt.get_power()[0]

print("── Feedpoint ──")
print(f"  Frequency: {ipt.get_frequency():.1f} MHz")
print(f"  Impedance: {Z.real:.1f} + {Z.imag:+.1f}j Ω")
print(
    f"  VSWR (50Ω): {abs((1 + abs((Z - 50) / (Z + 50))) / (1 - abs((Z - 50) / (Z + 50)))):.3f}"
)
print()


# ── 3. Structure currents ──────────────────────────────────────────────
#
# get_structure_currents(index) returns a nec_structure_currents object.
# Available methods:
#   .get_current()                  -> [complex, ...]   currents (A)
#   .get_current_segment_number()   -> [int, ...]       segment numbers
#   .get_current_segment_tag()      -> [int, ...]       tag numbers
#   .get_current_segment_center_x() -> [float, ...]     x coords (m)
#   .get_current_segment_center_y() -> [float, ...]     y coords (m)
#   .get_current_segment_center_z() -> [float, ...]     z coords (m)
#   .get_current_segment_length()   -> [float, ...]     segment lengths (m)
#   .get_n()                        -> int              total wire segments
#   .get_m()                        -> int              total patches
#
# Also for charge densities: get_q_density(), get_q_density_segment_*()
# And for patches: get_patch_number(), get_patch_center_*(), get_patch_e_*()

sc = context.get_structure_currents(0)
currents = sc.get_current()
tags = sc.get_current_segment_tag()

print("── Segment currents (first 5) ──")
for i in range(min(5, len(currents))):
    c = currents[i]
    mag = abs(c)
    phase = np.angle(c, deg=True)
    print(f"  seg {i:2d}  tag={tags[i]:2d}  |I|={mag:.4f} A  ∠={phase:+.1f}°")
print()


# ── 4. SC card with multiple_patch ─────────────────────────────────────
#
# multiple_patch() wraps the SM card.  Immediately after it, you can add
# SC continuation cards via geo.sc_card() to define a row of patches.
# This example is adapted from necpp/tests/test_multiple_sc_cards.py.
#
#   geo.multiple_patch(nx, ny,
#       ax1, ay1, az1,   # corner 1
#       ax2, ay2, az2,   # corner 2
#       ax3, ay3, az3)   # corner 3
#
#   geo.sc_card(i2,
#       x3, y3, z3,      # corner 3 of next patch
#       x4, y4, z4)      # corner 4 of next patch

print("── SC card example ──")
ctx2 = nec_context()
g2 = ctx2.get_geometry()

g2.sp_card(3, 0.019, -0.001424, 0.078830, 0.019, 0.001424, 0.078830)
g2.sc_card(3, 0.019, 0.001424, 0.076180, 0.019, -0.001424, 0.076180)
print("  SP + SC card added successfully.")
