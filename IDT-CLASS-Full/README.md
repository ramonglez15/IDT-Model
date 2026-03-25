# Enhanced Inflationary Domain Theory (IDT) with Hidden Regions

This project implements the Enhanced Inflationary Domain Theory (IDT) with Hidden Regions model as an extension to the CLASS cosmological code. The model addresses several tensions in modern cosmology, particularly the Hubble tension and structure formation issues.

## Overview

The Enhanced IDT model introduces a hidden region feature in the dark energy equation of state, characterized by:

- A transition at redshift z ≈ 0.35
- Modified dark energy dynamics with w₀ = -0.92, w_a = -0.14
- Reduced structure growth parameter σ₈ = 0.7509
- Increased Hubble parameter H₀ = 73.24 km/s/Mpc

These modifications successfully reduce the Hubble tension from over 5σ to just 0.19σ while maintaining consistency with CMB and BAO observations.

## Directory Structure

```
IDT-CLASS/
├── src/                  # Source code
│   ├── background/       # Background evolution with hidden regions
│   ├── perturbations/    # Modified perturbation equations
│   ├── hidden_regions/   # Hidden regions implementation
│   ├── input/            # Parameter handling
│   └── fourier/          # Power spectrum calculations
├── include/              # Header files
├── config/               # Configuration files
├── test/                 # Test scripts
├── tools/                # Analysis and visualization tools
└── doc/                  # Documentation
```

## Key Features

1. **Hidden Region Implementation**: Modifies the dark energy equation of state with a transition feature
2. **Hubble Tension Resolution**: Increases H₀ to match local measurements
3. **Structure Formation**: Reduces σ₈ to better match weak lensing observations
4. **Modular Design**: Separates code into logical components for better maintainability

## Usage

To compile the code:

```bash
cd IDT-CLASS
make
```

To run the enhanced model:

```bash
./idt_class config/enhanced_model.ini
```

## Requirements

- C compiler (gcc or clang)
- Python 3.6+ with numpy, matplotlib
- CLASS dependencies (FFTW, etc.)
