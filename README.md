# Predictive Modeling of Submarine Detection via Sonar

## Overview

This simulation models the probability of detecting a submerged submarine using passive sonar systems. It estimates the acoustic signal strength of a submarine based on its speed, models transmission loss over distance, accounts for ambient noise, and calculates signal-to-noise ratio (SNR) at a given listener position. It is designed as a foundational tool for analyzing passive acoustic detection likelihood in controlled operational environments.

The current implementation models the Ohio-class submarine. Other submarine classes and refinements will be added in future versions.

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
- Ambient noise is manually specified and not calculated from environmental data.
- Cavitation begins at 21 knots and follows a polynomial growth pattern thereafter.
- Only Ohio-class submarine acoustic characteristics are modeled in the current version.

---

## Current Limitations

- Does not account for multipath propagation, thermoclines, or sea floor reflections.
- Ambient noise is static and not modeled per frequency band or source.
- Cavitation noise is estimated, not based on empirical measurements.
- No probabilistic detection model is yet implemented.
- Does not support multiple submarine profiles or dynamic inputs.

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

## Installation
### Requirements

- Python 3.7+
- NumPy
- Matplotlib (optional, for future graphing)

### Install dependencies:
```bash
pip install numpy matplotlib
```
### Running the Program

Clone the repository
```bash
git clone https://github.com/MookLags/submarine_SNR.git
cd submarine-SNR
```
Run the simulation:
```bash
python3 submarine_detection.py
```
The script will output the submarine's noise level, transmission loss, and SNR for given inputs.

---
## Example Output:
```bash
Noise level:         103.58 dB
Transmission loss:    60.04 dB
SNR:                 -6.45 dB
```

---

## Contributing

Contributions are welcome. Please ensure changes are well-documented and tested. For enhancements or bug reports, open an issue or submit a pull request.
