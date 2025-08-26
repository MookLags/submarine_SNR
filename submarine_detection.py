import numpy as np
import matplotlib.pyplot as plt
from modsim import *
import argparse

'''
L0 is the 'resting' noise level of each class submarine before audibility of cavitation in dB is added to overall noise level
v0 is the knots after which cavitation will increase audibility
n is the noise scaling component
A is an estimated difference in dB from dB at max speed and dB at speed of cavitation threshold
'''

ohio = System(name='Ohio', L0=100, v0=21, n=2.5, p=2.5, A=0.3125, ms=25) # max submerged speed of 25 knots
lafayette = System(name='Lafeyette', L0=103, v0=8, n=2.8, p=2.5, A=0.074, ms=21) # max submerged speed of 21 knots
seawolf = System(name='Seawolf', L0=94, v0=20, n=2.3, p=2.5, A=0.1, ms=30) # max submerged speed of ~30+ knots
los_angeles = System(name='Los Angeles', L0=98, v0=13, n=2.5, p=2.5, A=0.15, ms=30) # max submerged speed of ~30 knots
typhoon = System(name='Typhoon', L0=110, v0=7, n=3.0, p=2.5, A=0.15, ms=28) # max submerged speed of 28 knots
red_october = System(name='Red October', L0=85, v0=15, n=1.5, p=2.5, A=0.05, ms=28) # typhoon class sub, magnetohydrodynamic drive enabled

subs = [ohio, lafayette, seawolf, los_angeles, typhoon, red_october]

def print_sub_specs(subs):
  # list the sub's name, max speed, and cavitation threshold each on a separate line
  for sub in subs:
    print(f'{sub.name}\nMax Submerged Speed: {sub.ms} knots\nCavitation Threshold: Roughly {sub.L0} dB at {sub.v0} knots\n')
  pass

def dLcav(v, system): 
  '''
  Solving A * (v - 25)** p where A is the cavitation scaling factor and p is the cavitation noise growth rate.

  e.gg for Ohio:  A = 10 / (4**p) => A = 0.3125
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

### SIMULATIONS ###

def get_loudest_sub(v, r, NL, subs):
  best_snr = float('-inf')
  loudest_sub = None

  for sub in subs:
    snr = get_signal_to_noise_ratio(v, r, NL, sub)
    if snr > best_snr:
      best_snr = snr
      loudest_sub = sub.name

  return loudest_sub, best_snr

def get_quietest_sub(v, r, NL, subs):
  best_snr = float('inf')
  loudest_sub = None

  for sub in subs:
    snr = get_signal_to_noise_ratio(v, r, NL, sub)
    if snr < best_snr:
      best_snr = snr
      quietest_sub = sub.name

  return quietest_sub, best_snr

def compare_sub_snr_at_v(v, r, NL, subs):
  res = {sub.name: get_signal_to_noise_ratio(v, r, NL, sub) for sub in subs}

  names = list(res.keys())
  snrs = list(res.values())
  
  fig, ax = plt.subplots()

  ax.bar(names, snrs, color='navy')
  ax.set_ylabel('SNR (dB)')
  ax.set_xlabel('Submarine Class')
  ax.set_title(f'SNR for each submarine at {v} knots and {r}m distance\n(Ambient noise = {NL})')
  
  plt.show()

def get_snr_for_range_of_distances(v, r, NL, sub, intervals):
  distances = np.linspace(1, r, intervals)
  snrs = [get_signal_to_noise_ratio(v, d, NL, sub) for d in distances]

  plt.figure(figsize=(20, 10))
  plt.plot(distances, snrs, label=sub.name, linewidth=2, color='navy')
  plt.xlabel=('Distance (m)')
  plt.ylabel=('SNR (dB)')
  plt.title(f'SNR vs. Distance for {sub.name}-Class Submarine at {v} knots')
  plt.grid(True)
  plt.legend()
  plt.show()

def add_common_arguments(subparser):
    subparser.add_argument('--v', type=float, required=True, help='Speed in knots')
    subparser.add_argument('--r', type=float, required=True, help='Distance in meters')
    subparser.add_argument('--NL', type=float, required=True, help='Ambient noise level in dB')

def main():
  parser = argparse.ArgumentParser(description="Submarine SNR Simulator")
  subparsers = parser.add_subparsers(dest='command', help='Available commands')

  parser_print_subs = subparsers.add_parser('ls', help='List some useful information about documented submarines.')

  parser_compare = subparsers.add_parser('compare-snr', help='Compare SNR for all submarines at a given speed and distance')
  add_common_arguments(parser_compare)

  parser_quietest = subparsers.add_parser('quietest-sub', help='Get quietest submarine at given speed and distance')
  add_common_arguments(parser_quietest)

  parser_loudest = subparsers.add_parser('loudest-sub', help='Get loudest submarine at given speed and distance')
  add_common_arguments(parser_loudest)

  parser_snr_distance = subparsers.add_parser('snr-distance', help='Plot SNR vs distance for a given submarine')
  add_common_arguments(parser_snr_distance)
  parser_snr_distance.add_argument('--sub', type=float, required=True, help='Submarine class name (e.g. Ohio)')

  args = parser.parse_args()

  if args.command == 'ls':
    print_sub_specs(subs)

  elif args.command == 'compare-snr':
    compare_sub_snr_at_v(args.v, args.r, args.NL, subs)

  elif args.command == 'loudest-sub':
    sub, snr = get_loudest_sub(args.v, args.r, args.NL, subs)
    print(f'Loudest Submarine: {sub} with SNR = {snr:.2f} dB')

  elif args.command == 'quietest-sub':
    sub, snr = get_quietest_sub(args.v, args.r, args.NL, subs)
    print(f'Quietest Submarine: {sub} with SNR = {snr:.2f} dB')

  elif args.command == 'snr-vs-distance':
    selected_sub = next((s for s in subs if s.name.lower() == args.sub.lower()), None)
    if selected_sub is None:
      print(f'Submarine "{args.sub}" not found. Available subs: {[s.name for s in subs]}')
      return
    get_snr_for_range_of_distances(args.v, args.r, args.NL, selected_sub, args.intervals)

  else:
    parser.print_help()

if __name__ == '__main__':
  main()
