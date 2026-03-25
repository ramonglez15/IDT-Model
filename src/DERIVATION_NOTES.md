# IDT Growth Equation Derivation — Where Standard GR Ends and IDT Begins

**Purpose**: Derive exactly what a smooth external domain does to structure growth within standard GR, identify where the effect is insufficient, and define precisely what additional physics IDT would need to predict.

---

## 1. The standard growth equation, step by step

The linear growth of matter perturbations δ = δρ_m/ρ_m in an expanding universe follows from three equations:

- **Continuity**: δ' + θ = 0
- **Euler**: θ' + Hθ + k²Φ = 0
- **Poisson**: k²Φ = -4πGa² ρ_m δ

Combining these (in conformal time, converting to d/d ln a):

```
d²δ/d(ln a)² + A(z) dδ/d(ln a) - B(z) δ = 0
```

where:
- **A(z) = 2 + d ln H / d ln a** — the friction coefficient
- **B(z) = (3/2) ρ_m / ρ_total** — the source coefficient

Both A and B depend on the total energy content. The external domain enters through both.

## 2. How the external domain enters each term

### Friction coefficient A(z)

```
d ln H / d ln a = -(1/2)(1 + 3 p_total/ρ_total)
               = -(1/2)(1 + 3 w_eff)
```

where w_eff = Σ(w_i × Ω_i) is the density-weighted equation of state.

Adding a domain with density ρ_ext and pressure p_ext = w_ext × ρ_ext:

```
w_eff = (w_m Ω_m + w_r Ω_r + w_Λ Ω_Λ + w_ext Ω_ext)
```

For the log-normal domain:
```
w_ext(z) = -1 + (1/3) × [-ln((1+z)/(1+z_c)) / σ_ln²]
```

At z = z_c: w_ext = -1 (like Λ → no change to friction)
At z ≠ z_c: w_ext ≠ -1, but ρ_ext is exponentially small

**Key observation**: the product ρ_ext × (w_ext + 1) determines the domain's deviation from Λ-like behavior in the friction term. For the log-normal:

```
ρ_ext × (1 + w_ext) = ρ_ext × (1/3) × [-ln((1+z)/(1+z_c)) / σ_ln²]
```

This product is maximized not at z_c (where ρ is max but w+1=0) nor far from z_c (where w+1 is large but ρ→0). It peaks at z where |ln((1+z)/(1+z_c))| ≈ σ_ln — i.e., about one width away from center.

**Magnitude**: For f_dom = 0.03 at z_c = 1.0, the peak of ρ_ext × (1+w_ext) contributes at most a few percent correction to w_eff at z ~ 0.5 or z ~ 1.5. This gives a small correction to friction.

### Source coefficient B(z)

```
B(z) = (3/2) ρ_m / ρ_total = (3/2) Ω_m(z)
```

Adding ρ_ext to ρ_total REDUCES Ω_m(z), weakening the gravitational source:

```
Ω_m(z) = ρ_m / (ρ_m + ρ_r + ρ_Λ + ρ_ext)
```

For late-time domains with f_dom ~ 0.03-0.05, ρ_ext/ρ_total ~ 3-5% near the peak. So the source term is reduced by 3-5% during the overlap epoch.

### Combined effect

Both modifications suppress growth:
- More friction (if w_ext > -1 near peak, which happens on the rising side)
- Weaker source (always, when ρ_ext > 0)

But both effects are proportional to f_dom, which is a few percent. The total σ₈ suppression is:

```
Δσ₈/σ₈ ≈ -O(f_dom) × (duration of overlap in e-folds)
```

For f_dom = 0.03, duration ~ 1 e-fold: Δσ₈ ≈ -0.01 to -0.02. **This matches exactly what we computed in CLASS.**

## 3. What this means: the ceiling of standard GR

Within standard GR with a smooth external domain, the σ₈ suppression is:

```
|Δσ₈| ≲ f_dom × (σ_ln of late domain) × (geometric factor ~ 1)
```

To get |Δσ₈| ~ 0.03 (from 0.81 to 0.78), we need f_dom × σ_ln ~ 0.03. For σ_ln = 0.5, that means f_dom ~ 0.06. But f_dom = 0.06 at z_c = 1.0 shifts BAO distances by ~5%, which violates constraints.

**This is why the MCMC pushes the late domain to zero.** The σ₈ effect is proportional to f_dom, and the BAO violation is also proportional to f_dom, with similar coefficients. There is no window where one is large enough and the other is small enough.

**This is not a CLASS limitation. This is a GR result.** Any background-level modification that adds energy at z ~ 0.3-2 will face this constraint.

## 4. Where IDT-specific physics could change the picture

For IDT to do better than Candidate 1, the domain must modify growth through a channel that ISN'T proportional to its energy density contribution to H(z).

Three possibilities, in order of increasing departure from standard GR:

### 4a. Domain perturbations (still within GR, but non-trivial)

If the domain has its own perturbations δ_ext ≠ 0, the Poisson equation becomes:

```
k²Φ = -4πGa²(ρ_m δ_m + ρ_ext δ_ext)
```

If δ_ext is **anticorrelated** with δ_m (the domain's structure opposes our structure), the effective source is weakened:

```
k²Φ = -4πGa² ρ_m δ_m (1 - |ρ_ext δ_ext / ρ_m δ_m|)
```

This gives G_eff < G. The suppression is proportional to ρ_ext/ρ_m × δ_ext/δ_m, which could be larger than the pure background effect if δ_ext is substantial.

**Physical motivation from IDT**: An external domain expanding faster than ours could have its structure "stretched" relative to ours. Regions that are dense in the external domain might correspond to voids in ours (because the external domain's expansion has moved its mass differently). This would produce anticorrelation.

**But**: this requires a specific model of how domain structures map onto each other, which is beyond what we've derived.

### 4b. Time-varying gravitational coupling (departure from minimal GR)

If the overlap geometry modifies the effective gravitational constant:

```
k²Φ = -4πG_eff(z) a² ρ_m δ_m
```

The growth equation becomes:

```
d²δ/d(ln a)² + A(z) dδ/d(ln a) - (3/2)(G_eff/G) Ω_m(z) δ = 0
```

Now the source term has an extra factor G_eff/G that can be either larger or smaller than 1, independent of ρ_ext's contribution to H(z).

**This decouples σ₈ from BAO.** The BAO distances depend on H(z), which depends on ρ_ext. But G_eff depends on the OVERLAP GEOMETRY, which could be a different function. So you could have:
- Small ρ_ext (preserves BAO)
- Significant G_eff modification (suppresses growth)

**This is the key insight: if the overlap modifies G_eff through a channel other than ρ_ext, the BAO-σ₈ tension breaks.**

**Physical motivation**: In scalar-tensor gravity, G_eff differs from G because of an additional scalar field. In IDT, the analogous quantity is the overlap function g(z) — how much of the external domain's gravity is "felt" in our universe. If g(z) affects the Poisson equation differently from how ρ_ext affects the Friedmann equation, the two effects decouple.

### 4c. Relative expansion coupling

The most IDT-specific version. The growth modification depends on the relative expansion rate:

```
G_eff(z)/G = 1 + α × Φ_dot_ext / (H × Φ_ext)
```

where Φ_dot_ext/Φ_ext measures how fast the external potential is changing relative to the Hubble rate.

For a fading domain (Φ_dot_ext < 0):
- The ratio is negative
- If α > 0: G_eff < G → growth suppressed

The magnitude depends on how fast the domain fades compared to the expansion rate. For a log-normal:

```
Φ_dot_ext / (H × Φ_ext) ≈ d ln ρ_ext / d ln a / 2 = (3/2)(1 + w_ext)
```

So:
```
G_eff/G ≈ 1 + (3α/2)(1 + w_ext)
```

On the falling side of a late domain (w_ext < -1): G_eff < G if α > 0.
On the rising side (w_ext > -1): G_eff > G.

**Net effect over the domain's lifetime**: depends on the asymmetry of the profile in physical time. For a log-normal (symmetric in ln(1+z)), the rising and falling contributions partially cancel, but the falling side occurs LATER when structures are more developed, so its effect on σ₈ is weighted more heavily.

## 5. What needs to be derived vs what can be parameterized

**Derivable from GR + domain overlap geometry:**
- Whether g(z) (overlap function) enters the Poisson equation, the Friedmann equation, or both
- Whether the coupling is proportional to ρ_ext, to dρ_ext/dt, or to a geometric quantity
- The sign of the effect given a faster-expanding external domain

**Must be parameterized (until a full theory of overlap geometry exists):**
- The magnitude of α or η (the coupling constant)
- Whether the coupling is scale-dependent (k-dependent G_eff)
- Whether there are higher-order effects

## 6. The minimal testable IDT growth hypothesis

Combining the above, the simplest extension beyond Candidate 1 that is:
- Physically motivated by time-varying overlap
- Distinguishable from standard smooth-density addition
- Parameterizable with one new constant

is:

```
Growth equation:

d²δ/d(ln a)² + A(z) dδ/d(ln a) - (3/2) Ω_m(z) [1 + η × f_overlap(z)] δ = 0
```

where:
```
f_overlap(z) = (1/3) × d ln ρ_ext / d ln a
             = -(1 + w_ext(z)) × ρ_ext(z)/ρ_total(z)
```

This is:
- Zero when ρ_ext = 0 (no domain → standard growth)
- Zero when w_ext = -1 (domain acts like Λ → no modification beyond background)
- Negative when the domain is fading (w_ext < -1 on falling side) → G_eff < G if η > 0
- Positive when the domain is building (w_ext > -1 on rising side) → G_eff > G if η > 0

The parameter η encodes "how strongly does the time variation of overlap affect gravitational coupling." Its sign and magnitude should ultimately come from the overlap geometry theory.

**If η > 0**: late fading domains suppress σ₈ beyond the background effect. This is the prediction to test.

**If η < 0**: late fading domains enhance σ₈. This is also a valid prediction and we would have to live with it.

**If η = 0**: we recover Candidate 1 (background only). This is the null hypothesis.

## 7. What this derivation establishes

1. **Standard GR with smooth external density gives Δσ₈ ~ -0.01 to -0.02** for late domains with f_dom ~ 0.03-0.05. This is too small, and is killed by BAO constraints. We computed this in CLASS and it's correct.

2. **The BAO-σ₈ deadlock is a feature of Candidate 1**, where both effects are proportional to ρ_ext in H(z). Breaking the deadlock requires a growth modification that ISN'T tied to the domain's energy density contribution.

3. **Candidate 2/4 (G_eff modification) could break the deadlock** because G_eff would depend on the OVERLAP DYNAMICS (how fast the domain is fading), not on ρ_ext directly. A domain with small ρ_ext (preserving BAO) could still have significant G_eff modification (suppressing σ₈) if the overlap coupling η is large enough.

4. **The sign of the effect (enhancement vs suppression) depends on physics, not fitting.** A fading domain gives G_eff < G (suppression) if η > 0. The sign of η must come from the theory.

5. **η is the single new parameter** beyond the domain profile parameters. Paper 2 would either derive η from first principles or constrain it empirically.

## 8. Implications for Paper 1 vs Paper 2

**Paper 1** (current result): Candidate 1 only. Background-level localized domain. ΔAIC = -5.2 from acoustic scale improvement. σ₈ unchanged. Honest, clean, η = 0 by construction.

**Paper 2**: Implement the growth equation with η ≠ 0. Test whether η > 0 (σ₈ suppression from fading overlap) produces a two-domain fit where:
- Early domain at z ~ 2000 shifts r_d → H₀ ↑
- Late domain at z ~ 1 with η > 0 suppresses growth → σ₈ ↓
- BAO preserved because the σ₈ effect comes from η, not from ρ_ext in H(z)
- ΔAIC significantly negative

**This is the result that would distinguish IDT from all existing models.** No other framework predicts that the RATE OF CHANGE of an external gravitational influence modifies growth independently of its contribution to the expansion rate.
