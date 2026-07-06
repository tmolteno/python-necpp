# Copyright (c) 2008-2026 Tim Molteno (tim@elec.ac.nz)
#
# Some antenna utility functions
#
import numpy as np

def reflection_coefficient(z, z0):
  return np.abs((z - z0) / (z + z0))
