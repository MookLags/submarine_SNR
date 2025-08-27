# Predictive Modeling of Submarine Detection via Sonar

## Overview

This is a simple CLI tool created for fun. It contains a suite of functions which run simulations on estimated specifications of US and Russian military submarines. Of the many limitations of this tool (see **Limitations** and **Assumptions** below), the most important to note and obvious to surmise is that of the available knowledge--or lack thereof--regarding these specifications. Most of the information necessary to collect the most accurate results of these simulations (i.e. cavitation threshold among others) is classified and inaccessible.

Therefore, many assumptions were made regarding base noise levels of submarines, cavitation thresholds, etc. Reasonable estimates were made based off of such information as the commonly sited stat that the Ohio cruises as quietly at 20 knots as the Lafayette at 6, and my own working knowledge of submarines, sound, and physics.

## Installation
### Requirements

- Python 3.7+
- NumPy
- Matplotlib (optional, for future graphing)
- Modsim (included in repo)

### Install dependencies:
```bash
pip install numpy matplotlib
```

Clone the repository
```bash
git clone https://github.com/MookLags/submarine_SNR.git
cd submarine-SNR
```

### Running the Program
As the program is still in early development, names of arguments are subject to change. To get the most up-to-date list of options of possible arguments in the terminal, you can ask for help:
```bash
python3 submarine_detection.py -h
```

which currently lists the following:
```bash
usage: submarine_detection.py [-h]
                              {ls,compare-snr,quietest-sub,loudest-sub,snr-distance}
                              ...

Submarine SNR Simulator

positional arguments:
  {ls,compare-snr,quietest-sub,loudest-sub,snr-distance}
                        Available commands
    ls                  List some useful information about documented
                        submarines.
    compare-snr         Compare SNR for all submarines at a given speed and
                        distance
    quietest-sub        Get quietest submarine at given speed and distance
    loudest-sub         Get loudest submarine at given speed and distance
    snr-distance        Plot SNR vs distance for a given submarine

options:
  -h, --help            show this help message and exit
```
I am currently focusing on developing new simulations and adding more parameters to existing functions to account for depth and temperature of water, customized/theoretical submarine specifications, and testing among others. See **Planned Enhancements** below.

---

## Core Formulas and Implementation

### 1. **Noise Level of Submarine (Source Level)**

#### Formula:

L_p(v) = L_0 + 10 * log10(1 + (v / v0)^n) + ΔL_cav(v)

#### Variables:

- \( L_0 \): Base noise level at cruising speed (dB)
- \( v \): Current submarine speed (knots)
- \( v_0 \): Reference speed, typically cavitation onset threshold (knots)
- \( n \): Empirical noise growth factor (2–3)
- \( ΔL_cav(v) \): Additional noise due to cavitation at higher speeds

#### Code Implementation:

```python
def get_noise_level(v):
    x = 1 + (v / v0)**n
    return L0 + 10 * (np.log(x) / np.log(10)) + dLcav(v)
```

### 2. **Cavitation Noise Increase**

#### Formula:

ΔL_cav(v) = 
    0                        if v ≤ v₀  
    A * (v - v₀)^p           if v > v₀
    
#### Variables:

- ΔL_cav(v): Additional noise due to cavitation at velocity v
- A: Scaling factor, estimated using known speed-noise endpoints
- p: Cavitation noise exponent, tuned to reflect logarithmic dB growth
- v₀: Cavitation onset speed (in knots)
- v: Submarine velocity (in knots)

#### Code Implementation:
```python
def dLcav(v): 
    if v <= v0:
        return 0
    else:
        return 0.3125 * (v - v0)**2.5
```

### 3. Transmission Loss (TL)

#### Formula:

TL(r) = 20 * log10(r) + α * r

#### Variables:

- r: Distance between the submarine and the listener (in meters)
- α: Absorption coefficient in seawater (typical value: 0.00004 dB/m)

#### Code Implementation:
```python
def get_transmission_loss(r): 
    alpha = 0.00004
    return 20 * (np.log(r) / np.log(10)) + alpha * r
```

### 4. Signal-to-Noise Ratio (SNR)

#### Formula:

SNR=Lp−TL−NL

#### Variables:

NL: Ambient noise level (user-defined, varies by environment)

#### Code Implementation:

```python
def get_signal_to_noise_ratio(v, r):
    NL = 50  # adjustable
    return get_noise_level(v) - get_transmission_loss(r) - NL
```
---

## Assumptions

- The ocean environment is homogeneous (constant temperature, salinity, and pressure).
- The speed of sound in water is constant.
- Submarine noise emissions are omnidirectional.
- Absorption and spreading loss are uniform over range.
- ~~Ambient noise is manually specified and not calculated from environmental data.~~
- ~~Cavitation begins at 21 knots and follows a polynomial growth pattern thereafter.~~
- ~~Only Ohio-class submarine acoustic characteristics are modeled in the current version.~~

---

## Current Limitations

- Does not account for multipath propagation, thermoclines, or sea floor reflections.
- ~~Ambient noise is static and not modeled per frequency band or source.~~
- Cavitation noise is estimated, not based on empirical measurements.
- No probabilistic detection model is yet implemented.
- ~~Does not support multiple submarine profiles or dynamic inputs.~~

---

## Planned Enhancements

### Implement detection probability modeling using a logistic function:

P_detect = 1 / (1 + e^(-k * (SNR - DT)))

Where:
- P_detect is the probability of detection
- SNR is the signal-to-noise ratio
- DT is the detection threshold
- k controls the slope of the transition region

- Add support for multiple submarine classes (e.g., Ohio, Seawolf, Lafayette)
- Decorative terminal-based UI for improved usability
- Visualization using matplotlib.pyplot (e.g., distance vs. detection likelihood)
- Handle edge cases such as:
  - Negative or zero velocity (v <= 0)
  - Zero or negative range (r <= 0)
  - Extremely low or high SNR values
- Implement unit tests for all core functions
- Model ambient noise (NL) based on environmental parameters such as depth, location, and time of day

---


## Contributing

Contributions are welcome. Please ensure changes are well-documented and tested. For enhancements or bug reports, open an issue or submit a pull request.
