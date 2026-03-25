# CLASS Modifications for Enhanced Inflationary Domain Theory (IDT)

This repository contains the modified files from the [CLASS](https://github.com/lesgourg/class_public) cosmological code that implement the Enhanced Inflationary Domain Theory (IDT) with Hidden Regions model.

## Overview

The Enhanced IDT model introduces a "hidden region" in the dark energy equation of state, characterized by a transition at redshift z ≈ 0.35. This feature helps resolve the Hubble tension and address structure formation issues.

## Repository Contents

- **Modified CLASS Files**: Only the files that have been modified from the original CLASS code are included in this repository.
- **Documentation**: Detailed documentation of the modifications and the model parameters.
- **Example Configuration**: Sample configuration file for running the Enhanced IDT model.

## Modified Files

1. `include/background.h`: Added hidden regions structure and function declarations.
2. `source/background.c`: Modified to support the hidden regions feature in the dark energy equation of state.
3. `include/input.h`: Updated to include hidden regions parameters.
4. `source/input.c`: Modified to read hidden regions parameters from configuration files.

## Documentation

For detailed information about the modifications and the model, see:

- [MODIFICATIONS_DOCUMENTATION.md](MODIFICATIONS_DOCUMENTATION.md): Detailed description of the modifications made to CLASS.
- [enhanced_model.ini](enhanced_model.ini): Example configuration file for the Enhanced IDT model.

## Key Results

The Enhanced IDT model with Hidden Regions successfully addresses two major tensions in modern cosmology:

1. **The Hubble Tension**: Reduces the tension from over 5σ in ΛCDM to just 0.19σ by increasing the Hubble parameter to H₀ = 73.24 km/s/Mpc.

2. **The σ₈ Tension**: Predicts a lower σ₈ value (0.7509) compared to ΛCDM (0.8168), helping to alleviate tensions with weak lensing and cluster count observations.

## Usage

To use these modifications:

1. Clone the original [CLASS repository](https://github.com/lesgourg/class_public).
2. Replace the files in the CLASS repository with the modified files from this repository.
3. Compile CLASS following the standard instructions.
4. Run CLASS with the provided `enhanced_model.ini` configuration file or create your own.

## Related Repository

For a complete implementation of the Enhanced IDT model, see the [IDT-CLASS repository](https://github.com/ramonglez15/CLASS-IDT).
