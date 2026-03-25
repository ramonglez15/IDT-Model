# Inflationary Domain Theory (IDT)

**Epoch-localized domain interactions as a two-channel approach to cosmological tensions in LCDM**

Jose Ramon Gonzalez | Independent Researcher

---

## Overview

IDT is a minimal effective extension of LCDM in which epoch-localized energy density contributions modify the expansion history and structure growth at specific cosmological epochs. The framework introduces a novel **effective Friedmann-Poisson decoupling**: domain contributions modify the background expansion rate without correspondingly enhancing local gravitational clustering, providing independent channels for addressing the H0 and S8 tensions.

### Key Result

With only **2 extra parameters** beyond LCDM:

| | LCDM | IDT |
|---|------|-----|
| H0 (km/s/Mpc) | 67.4 | 68.7 |
| sigma8 | 0.811 | 0.824 |
| l_a tension | 3.1 sigma | 0.3 sigma |
| Delta AIC | 0 | **-8.1** |

**Strongly preferred over LCDM** (Delta AIC = -8.1).

### Two-Domain Architecture

- **Early domain** (z ~ 2000): Shifts the sound horizon r_d, raising the inferred H0. Does not affect sigma8.
- **Late domain** (z ~ 1): Modifies effective gravitational coupling G_eff via dephasing mechanism, suppressing structure growth. Does not affect r_d.

The two channels operate independently -- a structural feature of the epoch-separation, not a result of parameter tuning.

## Repository Structure

```
IDT-Model/
|-- src/                    Core IDT module and paper
|   |-- IDT_Paper1.tex      Complete paper (PRD format)
|   |-- figures/             Publication figures (PDF + PNG)
|   |-- idt_domain.py        IDTDomain, IDTModel classes
|   |-- cosmology_base.py    LCDM baseline functions
|   |-- class_integration.py CLASS integration paths
|   |-- test_idt_standalone.py  Validation suite (no CLASS needed)
|   +-- generate_figures.py  Paper figure generation
|
|-- analysis/               Working scripts and diagnostics
|   |-- idt_mcmc_*.py        MCMC campaigns (parameter scans, robustness)
|   |-- STEERING_MEMO.md     Research steering document
|   |-- DERIVATION_NOTES.md  G_eff derivation from first principles
|   +-- *.png                Diagnostic plots
|
|-- archive/                Prior implementations (reference)
|   |-- class/               Modified CLASS v3.3.0 with IDT domains
|   |-- CLASS-IDT*/          Earlier C implementations
|   +-- universe/            Theory documents
|
+-- .gitignore
```

## Modified CLASS

The CLASS Boltzmann solver (v3.3.0) has been modified to support:

- **Up to 5 simultaneous localized log-normal domains** in the background
- **Dephasing G_eff modification** in the perturbation equations
- Parameters read from .ini files: `f_dom_idt_N`, `z_c_idt_N`, `sigma_ln_idt_N`, `eta0_idt`

Modified files: `include/background.h`, `source/background.c`, `source/input.c`, `source/perturbations.c`

## Quick Start

```bash
# Run standalone validation (no CLASS needed)
cd src
python test_idt_standalone.py

# Generate paper figures
python generate_figures.py
```

## Requirements

- Python 3.11+
- numpy, scipy, matplotlib
- CLASS v3.3.0 (included in archive/class/, with IDT modifications)
- classy Python bindings (build with `cd archive/class && make && cd python && python setup.py build_ext --inplace`)

## Paper

The paper "Epoch-Localized Domain Interactions: A Two-Channel Approach to Cosmological Tensions in LCDM" is in `src/IDT_Paper1.tex` with figures in `src/figures/`. Compile with pdflatex or upload to Overleaf.

## License

This work is provided for academic and research purposes.
