#
# Some antenna utility functions
#
import numpy as np

def reflection_coefficient(z, z0):
  return np.abs((z - z0) / (z + z0))

def vswr(z, z0):
    Gamma = reflection_coefficient(z, z0)
    return float((1 + Gamma) / (1 - Gamma))

def mismatch(z, z0):
    Gamma = reflection_coefficient(z, z0)
    return 1 - Gamma**2

# Source: https://gist.github.com/temporaer/6755266
# 'matplotlib log-polar plots seem to be quite buggy at the time of writing.' Yes, indeed, sadly...
def plot_logpolar(ax, theta, r_, bullseye=None, **kwargs):
    min10 = np.log10(np.min(r_))
    max10 = np.log10(np.max(r_))
    if bullseye is None:
        bullseye = min10 - np.log10(0.5 * np.min(r_))
    r = np.log10(r_) - min10 + bullseye
    ax.plot(theta, r, **kwargs)
    l = np.arange(np.floor(min10), max10)
    ax.set_rticks(l - min10 + bullseye)
    # ax.set_yticklabels(["1e%d" % x for x in l])
    ax.set_yticklabels(["%d" % x for x in l])
    ax.set_rlim(0, max10 - min10 + bullseye)
    return ax
