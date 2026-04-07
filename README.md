# Inflationary Domain Theory (IDT)

**Epoch-localized domain interactions as a multi-channel approach to cosmological tensions in LCDM**

Jose Ramon Gonzalez | Independent Researcher

---

## Overview

IDT is a minimal effective extension of LCDM in which epoch-localized energy density contributions modify the expansion history and structure growth at specific cosmological epochs. The framework introduces **gravitational dephasing**: during domain resonance, the effective gravitational coupling is partially cancelled — analogous to the force balance at a Lagrange point — suppressing late-time structure growth while preserving the CMB acoustic scale.

### Paper III Key Results (converged, all R-hat < 1.1)

| | LCDM | Paper I | Paper III |
|---|------|---------|-----------|
| H0 (km/s/Mpc) | 67.4 | 68.7 | 68.1 |
| sigma8 (dephased) | 0.811 | 0.809 | 0.745 |
| S8 tension | 3.1 sigma | ~2.8 sigma | **0.2 sigma** |
| l_a tension | 3.1 sigma | 0.3 sigma | **0.0 sigma** |
| Extra params | 0 | 2 | 6 |
| Delta AIC | 0 | -8.1 | **-24** |

**Statistically preferred over LCDM** (Delta AIC = -24 under compressed Planck + P(k) constraints).

### Three Advances in Paper III

1. **Phase quantum formalism**: Domain widths derived from a single parameter Delta, replacing hand-chosen values
2. **Conserved observable**: g = f_dom x (1 + eta0) = 0.035 +/- 0.016 — the net dephasing impact, analogous to Omega_m h^2 in CMB cosmology
3. **Converged posteriors**: Adaptive Metropolis-Hastings with 4 independent chains, all Gelman-Rubin R-hat < 1.1

## Publications

| Paper | Title | Status | Link |
|-------|-------|--------|------|
| I | Epoch-Localized Domain Interactions | Published | [Zenodo](https://zenodo.org/records/19224546) |
| II | High-Redshift Structure Formation and eta0 Parameter Space | Published | [Zenodo](https://zenodo.org/records/19268803) |
| III | Phase Resonance, Gravitational Dephasing, and the Conserved Net Impact Observable | Published | [Zenodo](https://zenodo.org/records/19446031) |

## Two-Domain Architecture

- **Early domain** (z_c ~ 2250): Modifies expansion history near matter-radiation transition. Drives the JWST high-z galaxy prediction (20-50% enhancement at z = 10-15).
- **Late domain** (z_c ~ 1.8): Modifies effective gravitational coupling G_eff via dephasing, suppressing structure growth. Reduces S8 from 3 sigma to 0.2 sigma tension.

The dephasing parameter eta0 = -0.57 produces behavior analogous to a gravitational Lagrange point: partial cancellation from competing domain influences.

## Repository Structure

```
IDT-Model/
|-- src/                    Core IDT module and papers
|   |-- IDT_Paper1.tex      Paper I (PRD format)
|   |-- IDT_Paper3.tex      Paper III (PRD format)
|   |-- IDT_Paper3_Outline.md  Paper III outline and language rules
|   |-- desi_dr1_bao.py     DESI DR1 BAO data module
|   |-- figures/             Publication figures
|   |-- idt_domain.py        IDTDomain, IDTModel classes
|   |-- cosmology_base.py    LCDM baseline functions
|   +-- class_integration.py CLASS integration paths
|
|-- analysis/               MCMC scripts and diagnostics
|   |-- idt_mh_adaptive.py   Adaptive M-H sampler (Paper III primary)
|   |-- idt_emcee_*.py       emcee ensemble samplers
|   |-- idt_find_map.py      MAP optimizer
|   |-- chain_diagnostics.py Chain analysis and convergence
|   |-- three_domain_test.py Third domain scan (null result)
|   |-- sigma8_cap_scan.py   sigma8_CLASS constraint analysis
|   |-- bao_desi_comparison.py  SDSS vs DESI BAO comparison
|   +-- generate_paper3_figures.py  All 12 Paper III figures
|
|-- archive/                Prior implementations (reference)
|   |-- class/               Modified CLASS v3.3.0 with IDT domains
|   +-- universe/            Theory documents
|
+-- CLAUDE.md               Project configuration
```

## Modified CLASS

CLASS v3.3.0 modified to support:

- **Up to 5 simultaneous localized log-normal domains** in the background
- **Dephasing G_eff modification** in perturbation equations
- Parameters: `f_dom_idt_N`, `z_c_idt_N`, `sigma_ln_idt_N`, `eta0_idt`

## Quick Start

```bash
# Build CLASS with IDT modifications
cd archive/class && make && cd python && python setup.py build_ext --inplace

# Run the adaptive M-H sampler (Paper III)
python analysis/idt_mh_adaptive.py

# Generate Paper III figures
python analysis/generate_paper3_figures.py
```

## Requirements

- Python 3.11+
- numpy, scipy, matplotlib, emcee
- CLASS v3.3.0 (included in archive/class/, with IDT modifications)

## License

This work is provided for academic and research purposes.
