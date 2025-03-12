# Modifications to CLASS for IDT Model

This document lists the files that have been modified from the original CLASS (Cosmic Linear Anisotropy Solving System) code to implement the Inflationary Domain Theory (IDT) model.

## Modified Core Files

The following core files have been modified from the original CLASS repository:

- **source/background.c**: Modified to implement the IDT model's background evolution equations.
- **include/background.h**: Modified to add new structures and functions for the IDT model.
- **Makefile**: Modified to support the IDT model.

## Original CLASS Repository

The original CLASS code is from the [CLASS GitHub repository](https://github.com/lesgourg/class_public). The modifications listed above were made to implement the IDT model.

## IDT-Specific Files

All IDT-specific files, including analysis scripts, configuration files, and documentation, have been moved to the IDT directory. These include:

- Analysis scripts (analyze_*.py, run_*.py, update_*.py)
- Configuration files (hidden_region*.ini)
- Documentation (enhanced_model_documentation.md)
- Output files (*.png, mcmc_results)

## IDT Model

The Inflationary Domain Theory (IDT) proposes that the observed cosmological phenomena of dark matter and dark energy originate from gravitational interactions between our observable universe and multiple overlapping inflationary regions (domains). For more information about the IDT model, see the documentation in the IDT directory.
