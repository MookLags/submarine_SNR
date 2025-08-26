import numpy as np
import matplotlib.pyplot as plt
from modsim import *

'''
L0 is the 'resting' noise level of each class submarine before audibility of cavitation in dB is added to overall noise level
v0 is the knots after which cavitation will increase audibility
n is the noise scaling component
'''

ohio = System(L0=100, v0=21, n=2.5, p=2.5, A=0.3125) # max submerged speed of 25 knots
lafayette = System(L0=103, v0=8, n=2.8, p=2.5, A=0.074) # max submerged speed of 21 knots
seawolf = System(L0=94, v0=20, n=2.3, p=2.5, A=0.1) # max submerged speed of ~30+ knots
los_angeles = System(L0=98, v0=13, n=2.5, p=2.5, A=0.15) # max submerged speed of ~30 knots

L0 = 100 
v0 = 8 
n = 2.5 # noise scaling component. Assumed to be between 2 and 3 given an estimated max noise output of 110-120

def dLcav(v, system): 
  '''
  Solving A * (v - 25)** p where A is the cavitation scaling factor and p is the cavitation noise growth rate.

  A = 10 / ((v-v0)**p)
  Smaller values of p lead to more linear increases which are not necessarily accurate given dB are logarithmic.
  '''
  if v <= system.v0: # Below cavitation threshold
    return 0
  else:
    return system.A * (v - system.v0)**system.p

def get_noise_level(v, system):
  x = 1 + (v / system.v0)**system.n
  return system.L0 + 10 * (np.log(x) / np.log(10)) + dLcav(v, system)

def get_transmission_loss(r): 
  '''
  r = distance
  alpha = Rate at which dB dissipates as it travels through a medium (0.04 dB/km is a good rate for seawater).
  Using 20 to model wide open seas. Shallower waters will require 10 (cylindrical)
  '''
  alpha = 0.00004
  return 20 * (np.log(r) / np.log(10)) + alpha * r

def get_signal_to_noise_ratio(v, r, NL, system):
  # NL = ambient noise level
  return get_noise_level(v, system) - get_transmission_loss(r) - NL

print('Noise level: ', get_noise_level(21, seawolf))
print('Transmission loss: ', get_transmission_loss(10000))
print('SNR: ', get_signal_to_noise_ratio(21, 1000, 50, seawolf))
