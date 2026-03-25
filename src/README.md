# IDT CLASS Module

**Inflationary Domain Theory — Minimal Effective Model for CLASS Integration**

## Overview

This module implements the minimal early-time IDT domain parameterization
for integration with the CLASS Boltzmann solver. It provides:

- **Background**: Conserved domain fluid with ρ(z), p(z), w(z)
- **Perturbations**: Fluid equations in synchronous gauge (δ, θ)
- **CLASS integration**: .ini file generation and C source patches
- **Validation**: Standalone test suite (no CLASS dependency)

## Parameterization

The IDT domain is specified by **3 free parameters** (+1 fixed):

| Parameter | Symbol | Description | Typical Range |
|-----------|--------|-------------|---------------|
| Peak fraction | `f_dom` | ρ_dom/ρ_total at peak | 0.02 – 0.20 |
| Critical redshift | `z_c` | Center of domain activity | 1500 – 3000 |
| Width | `Δ_z` | Redshift width | 0.2–0.5 × z_c |
| Sound speed² | `c_s²` | Rest-frame (fixed) | 1.0 (default) |

The energy density profile is log-normal in (1+z):

```
Ω_dom(z) = Ω_peak × exp(-½ [ln((1+z)/(1+z_c)) / σ_ln]²)
```

where `σ_ln = Δ_z / (1 + z_c)` and `Ω_peak = f_dom/(1-f_dom) × E²_ΛCDM(z_c)`.

**Conservation is guaranteed by construction**: w(z) is *derived* from
the ρ(z) profile via the continuity equation, not assumed.

## Quick Start

```python
from idt_domain import IDTDomain, IDTModel

# Create a domain
domain = IDTDomain(f_dom=0.10, z_c=2000, delta_z=600)
domain.summary()

# Build full model
model = IDTModel(domains=[domain])

# Get H(z)
import numpy as np
z = np.linspace(0, 3000, 1000)
H = model.H(z)
```

## File Structure

```
idt_class_module/
├── __init__.py              # Package init
├── idt_domain.py            # Core: IDTDomain, IDTModel classes
├── cosmology_base.py        # ΛCDM baseline functions
├── class_integration.py     # CLASS .ini generation + C patches
├── README.md                # This file
└── tests/
    └── test_idt_standalone.py   # Validation (no CLASS needed)
```

## Usage: Step by Step

### Step 1: Run standalone validation (no CLASS needed)

```bash
cd idt_class_module
python tests/test_idt_standalone.py
```

This verifies conservation, w(z) behavior, sound horizon shifts,
late-time distance constraints, and CMB shift parameters.

### Step 2: Generate CLASS input files

```python
from class_integration import generate_class_ini, generate_class_source_patch
from idt_domain import IDTDomain, IDTModel

domain = IDTDomain(f_dom=0.10, z_c=2000, delta_z=600)
model = IDTModel(domains=[domain])

# Path 1: Use CLASS fluid sector (simpler)
generate_class_ini(model, output_dir="class_runs/")

# Path 2: Generate C patches (more control)
generate_class_source_patch(domain, output_dir="class_patches/")
```

### Step 3: Run CLASS perturbation check

```bash
# If CLASS is installed with Python bindings:
python idt_classy_wrapper.py

# Or with CLASS command line:
cd /path/to/class
./class idt_run.ini
```

### Step 4: Analyze CMB spectra

The classy wrapper automatically compares:
- TT, EE, TE power spectra (IDT vs ΛCDM)
- Lensing power spectrum
- Peak positions and heights
- Sound horizon and shift parameters

## Physics Notes

### Why log-normal profile?

Cosmological evolution is multiplicative in (1+z), making log(1+z) the
natural coordinate. A Gaussian in log(1+z) space:
- Is symmetric in physical time
- Naturally peaks and decays on both sides
- Produces smooth, finite w(z) everywhere
- Has w(z_c) = -1 exactly at the peak (d(ln ρ)/d(ln(1+z)) = 0)

### Why w(z) oscillates around -1

For a peaked ρ(z), conservation requires:
- w > -1 on the rising side (ρ growing → dilutes slower than Λ)
- w = -1 at the peak (instantaneously constant)  
- w < -1 on the falling side (ρ decreasing → dilutes faster than Λ)

This phantom crossing is **not pathological** for an effective fluid.
It does NOT imply ghost instabilities because:
1. The domain is not a fundamental scalar field
2. c_s² > 0 is enforced independently
3. The total energy density remains positive

### Connection to Early Dark Energy

This parameterization is structurally similar to EDE models but with
key differences:
- EDE uses an axion potential → specific w(z) dynamics
- IDT uses a phenomenological ρ(z) profile → more flexible
- IDT doesn't commit to a microscopic mechanism
- IDT can include multiple domains at different epochs

### Perturbation stability

With c_s² = 1 (default), the domain has maximal pressure support and
does not cluster. This is the **most conservative** choice:
- No additional structure growth
- No ISW effect from domain perturbations
- Minimal impact on CMB beyond background geometry

For c_s² < 1, the domain can cluster, potentially affecting σ₈.
This should be explored in Paper 2 (growth/structure focus).

## Paper 1 Scope

The recommended scope for the first paper:

1. Define the effective model (this parameterization)
2. Verify conservation (automated in test suite)
3. Show background observables (r_d shift, distances)
4. Run CLASS perturbation check (CMB spectra)
5. Compare against Planck compressed likelihood
6. Report AIC/BIC vs ΛCDM

**Not in Paper 1**: growth rate predictions, full Planck MCMC,
microscopic derivation, multi-domain models.
