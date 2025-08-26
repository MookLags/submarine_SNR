import numpy as np
import matplotlib.pyplot as plt
from modsim import *

'''
L0 is the 'resting' noise level of each class submarine before audibility of cavitation in dB is added to overall noise level
v0 is the knots after which cavitation will increase audibility
n is the noise scaling component
'''

ohio = System(L0=100, v0=21, n=2.5)

L0 = 100 # estimated 'resting' noise level of Ohio class sub (or similar) before audibility of cavitation in dB
v0 = 21 # knots after which cavitation will increase audibility (i.e. maximum cruise speed at L0db
n = 2.5 # noise scaling component. Assumed to be between 2 and 3 given an estimated max noise output of 110

def dLcav(v): 
  '''
  Solving A * (v - 25)** p where A is the cavitation scaling factor and p is the cavitation noise growth rate.
  Based on reasonable trial and error.
  Given the estimated max speed of a submerged Ohio (25 knots) we can solve for A:

  A = 10 / (4**p)
  Smaller values of p lead to more linear increases which are not necessarily accurate given dB are logarithmic.
  p must be higher, around 2.5 made the most sense given estimated max speed of sub.
  '''
  if v <= v0: # Below cavitation threshold so doesn't matter--0
    return 0
  else:
    return 0.3125 * (v - v0)**2.5

def get_noise_level(v, system):
  x = 1 + (v / system.v0)**system.n
  return system.L0 + 10 * (np.log(x) / np.log(10)) + dLcav(v)

def get_transmission_loss(r): 
  '''
  r = distance
  alpha = Rate at which dB dissipates as it travels through a medium (0.04 dB/km is a good rate for seawater)
  '''
  alpha = 0.00004
  return 20 * (np.log(r) / np.log(10)) + alpha * r

def get_signal_to_noise_ratio(v, r, NL, system):
  # NL = ambient noise level
  return get_noise_level(v, system) - get_transmission_loss(r) - NL

print('Noise level: ', get_noise_level(22, ohio))
print('Transmission loss: ', get_transmission_loss(100))
print('SNR: ', get_signal_to_noise_ratio(22, 1000, 50, ohio))
