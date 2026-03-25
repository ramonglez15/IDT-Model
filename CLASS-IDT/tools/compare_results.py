#!/usr/bin/env python3
"""
Compare results from ΛCDM and Enhanced IDT models

This script compares the results from the ΛCDM and Enhanced IDT models,
focusing on the Hubble tension, structure formation, and dark energy dynamics.

Author: IDT-CLASS Team
Date: March 2025
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

# Create output directory if it doesn't exist
os.makedirs('IDT-CLASS/output/plots', exist_ok=True)

# Parameters for the models
lcdm_params = {
    'h': 0.6774,
    'Omega_m': 0.3075,
    'sigma8': 0.8168,
    'w0': -1.0,
    'wa': 0.0
}

enhanced_params = {
    'h': 0.7324,
    'Omega_m': 0.3137,
    'sigma8': 0.7509,
    'w0': -0.92,
    'wa': -0.14,
    'z_transition': 0.35,
    'amplitude': 0.05,
    'width': 0.1
}

# Function to calculate w(z) for the enhanced model
def w_enhanced(z, params):
    w0 = params['w0']
    wa = params['wa']
    z_transition = params['z_transition']
    amplitude = params['amplitude']
    width = params['width']
    
    # CPL parameterization
    a = 1.0 / (1.0 + z)
    w_cpl = w0 + wa * (1.0 - a)
    
    # Hidden region transition
    transition = 0.5 * (1.0 - np.tanh((z - z_transition) / width))
    
    # Combined equation of state
    return w_cpl - amplitude * transition

# Function to calculate w(z) for the ΛCDM model
def w_lcdm(z, params):
    return -1.0 * np.ones_like(z)

# Function to calculate the Hubble parameter H(z)
def hubble_parameter(z, params, model='lcdm'):
    h = params['h']
    Omega_m = params['Omega_m']
    H0 = 100.0 * h  # km/s/Mpc
    
    # For ΛCDM
    if model == 'lcdm':
        return H0 * np.sqrt(Omega_m * (1.0 + z)**3 + (1.0 - Omega_m))
    
    # For enhanced model with w(z)
    elif model == 'enhanced':
        # Calculate Omega_de(z) with w(z)
        z_array = np.linspace(0, z, 1000)
        dz = z_array[1] - z_array[0]
        w_z = w_enhanced(z_array, params)
        
        # Integrate (1 + w(z))/(1+z) to get Omega_de(z)
        integrand = (1.0 + w_z) / (1.0 + z_array)
        integral = np.sum(integrand) * dz
        
        Omega_de = (1.0 - Omega_m) * np.exp(3.0 * integral)
        
        return H0 * np.sqrt(Omega_m * (1.0 + z)**3 + Omega_de)

# Function to calculate the growth factor D(z)
def growth_factor(z, params, model='lcdm'):
    # Simplified growth factor calculation
    Omega_m = params['Omega_m']
    
    if model == 'lcdm':
        # For ΛCDM, use the fitting formula
        a = 1.0 / (1.0 + z)
        gamma = 0.55  # Growth index for ΛCDM
        f = Omega_m**(gamma)  # Growth rate
        D = a * f
        return D
    
    elif model == 'enhanced':
        # For enhanced model, reduce growth by sigma8 ratio
        a = 1.0 / (1.0 + z)
        gamma = 0.55  # Base growth index
        
        # Modify growth index based on sigma8 ratio
        sigma8_ratio = params['sigma8'] / lcdm_params['sigma8']
        gamma_mod = gamma * (1.0 + 0.1 * (1.0 - sigma8_ratio))
        
        f = Omega_m**(gamma_mod)  # Modified growth rate
        D = a * f * sigma8_ratio
        return D

# Create redshift array
z = np.linspace(0, 3, 100)

# Plot dark energy equation of state
plt.figure(figsize=(10, 6))
plt.plot(z, w_lcdm(z, lcdm_params), 'b-', label='ΛCDM')
plt.plot(z, w_enhanced(z, enhanced_params), 'r-', label='Enhanced IDT')
plt.axvline(x=enhanced_params['z_transition'], color='k', linestyle='--', alpha=0.5, label='Hidden Region Transition')
plt.xlabel('Redshift (z)')
plt.ylabel('Dark Energy Equation of State w(z)')
plt.title('Dark Energy Equation of State')
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig('IDT-CLASS/output/plots/dark_energy_eos.png', dpi=300, bbox_inches='tight')

# Plot Hubble parameter
plt.figure(figsize=(10, 6))
H_lcdm = np.array([hubble_parameter(zi, lcdm_params, 'lcdm') for zi in z])
H_enhanced = np.array([hubble_parameter(zi, enhanced_params, 'enhanced') for zi in z])

plt.plot(z, H_lcdm, 'b-', label='ΛCDM')
plt.plot(z, H_enhanced, 'r-', label='Enhanced IDT')
plt.axvline(x=enhanced_params['z_transition'], color='k', linestyle='--', alpha=0.5, label='Hidden Region Transition')
plt.xlabel('Redshift (z)')
plt.ylabel('Hubble Parameter H(z) [km/s/Mpc]')
plt.title('Hubble Parameter Evolution')
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig('IDT-CLASS/output/plots/hubble_parameter.png', dpi=300, bbox_inches='tight')

# Plot Hubble tension
plt.figure(figsize=(10, 6))
H0_values = [67.4, 73.04]  # Planck, SH0ES
H0_errors = [0.5, 1.04]    # Errors
labels = ['Planck CMB', 'SH0ES']
colors = ['blue', 'green']

# Plot measurements
for i, (H0, err, label, color) in enumerate(zip(H0_values, H0_errors, labels, colors)):
    plt.errorbar(i, H0, yerr=err, fmt='o', color=color, markersize=8, capsize=5, label=label)

# Plot model values
plt.axhline(y=lcdm_params['h']*100, color='blue', linestyle='-', alpha=0.7, label='ΛCDM')
plt.axhline(y=enhanced_params['h']*100, color='red', linestyle='-', alpha=0.7, label='Enhanced IDT')

plt.xlabel('Measurement')
plt.ylabel('H₀ [km/s/Mpc]')
plt.title('Hubble Tension Resolution')
plt.xticks([0, 1], labels)
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig('IDT-CLASS/output/plots/hubble_tension.png', dpi=300, bbox_inches='tight')

# Plot growth factor
plt.figure(figsize=(10, 6))
D_lcdm = np.array([growth_factor(zi, lcdm_params, 'lcdm') for zi in z])
D_enhanced = np.array([growth_factor(zi, enhanced_params, 'enhanced') for zi in z])

plt.plot(z, D_lcdm, 'b-', label='ΛCDM')
plt.plot(z, D_enhanced, 'r-', label='Enhanced IDT')
plt.axvline(x=enhanced_params['z_transition'], color='k', linestyle='--', alpha=0.5, label='Hidden Region Transition')
plt.xlabel('Redshift (z)')
plt.ylabel('Growth Factor D(z)')
plt.title('Structure Growth Comparison')
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig('IDT-CLASS/output/plots/growth_factor.png', dpi=300, bbox_inches='tight')

# Print summary
print("\nEnhanced Inflationary Domain Theory (IDT) with Hidden Regions")
print("=============================================================")
print("\nModel Parameters:")
print(f"  ΛCDM: H₀ = {lcdm_params['h']*100:.2f} km/s/Mpc, Ωₘ = {lcdm_params['Omega_m']:.4f}, σ₈ = {lcdm_params['sigma8']:.4f}")
print(f"  Enhanced IDT: H₀ = {enhanced_params['h']*100:.2f} km/s/Mpc, Ωₘ = {enhanced_params['Omega_m']:.4f}, σ₈ = {enhanced_params['sigma8']:.4f}")
print(f"                w₀ = {enhanced_params['w0']:.2f}, wₐ = {enhanced_params['wa']:.2f}")
print(f"                z_transition = {enhanced_params['z_transition']:.2f}, amplitude = {enhanced_params['amplitude']:.2f}")

print("\nHubble Tension:")
print(f"  ΛCDM: {abs(lcdm_params['h']*100 - H0_values[1])/H0_errors[1]:.2f}σ tension with SH0ES")
print(f"  Enhanced IDT: {abs(enhanced_params['h']*100 - H0_values[1])/H0_errors[1]:.2f}σ tension with SH0ES")

print("\nStructure Formation:")
print(f"  ΛCDM: σ₈ = {lcdm_params['sigma8']:.4f}")
print(f"  Enhanced IDT: σ₈ = {enhanced_params['sigma8']:.4f} ({(enhanced_params['sigma8']/lcdm_params['sigma8']-1)*100:.1f}% change)")

print("\nPlots saved to IDT-CLASS/output/plots/")
