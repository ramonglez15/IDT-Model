# IDT Research Steering Memo — Post-Proxy Assessment

**Date**: 2026-03-24
**Status**: Multi-domain proxy results complete. Next step: localized domain implementation.

---

## A. What the current multi-domain result really establishes

**Established with confidence:**

1. An early-time energy injection that shrinks r_d can raise H₀ from 67.4 toward 72 while keeping l_a within 1σ of Planck. This is a background-geometry result independent of the specific microphysics.

2. A late-time CPL fluid (w₀, wₐ) combined with the early component produces Δχ² = -39.9 (ΔAIC = -31.9) against ΛCDM using Planck compressed + BAO + SN + SH0ES. The improvement is real and comes primarily from reducing the H₀ tension (from 5.5σ to ~1.2σ).

3. The data prefers w₀ ≈ -1.03 for the late-time fluid, remarkably close to a cosmological constant. The late domain's role in the proxy model is modest — most of the work is done by the early radiation component.

4. The single-domain CPL-only fit (no early component) converges on w₀ ≈ -1.19 (phantom), achieves H₀ ≈ 70, and is also preferred over ΛCDM (ΔAIC = -25.6). The quintessence side (w₀ > -1) is ruled out by the CMB when only one fluid is available.

5. Conservation is satisfied by construction in the IDTDomain parameterization. All CLASS runs produce perturbation-stable CMB spectra. The model does not break physics at the level CLASS can test.

**Not established — proxy-dependent only:**

1. σ₈ = 0.883 in the multi-domain fit is a consequence of using ΔN_ur as the early-domain proxy. N_ur is permanent radiation, not a localized domain. A truly localized domain that vanishes before z ~ 100 would not contribute extra expansion during matter domination and would produce a different σ₈.

2. The specific value ΔN_ur = 0.88 has no direct physical interpretation as a "domain strength." It absorbs both the real early-domain effect on r_d and compensatory adjustments to other parameters. It should be treated as an effective fit parameter, not a measurement of domain properties.

3. The claim that the early and late domains "operate independently" is partially true for r_d (set at z ~ 1060) vs late-time distances (z < 2), but N_ur is present at all epochs, so the two proxy components are not cleanly separated.

## B. What is still only proxy-dependent

| Result | Proxy status | What changes with localized domain |
|--------|-------------|-------------------------------------|
| H₀ ≈ 71.7 | Partly proxy | r_d shift is real; exact H₀ depends on how much energy the localized domain injects near z ~ 2000 |
| σ₈ = 0.883 | Fully proxy | Localized domain that vanishes by z ~ 100 would not increase expansion during structure formation. σ₈ could go either way. |
| ΔN_ur = 0.88 | Proxy artifact | Localized domain has 3 physical parameters (f_dom, z_c, σ_ln), not one N_ur number |
| l_a = 301.4 | Mostly real | The geometric argument (d_C/r_s) is robust. A localized domain may shift l_a slightly differently depending on when it decays. |
| w₀ ≈ -1.03 | Partly real | If the late domain is truly needed, w₀ near -1 is preferred. But with a proper early domain, the late component may become unnecessary. |

## C. Why a localized domain is the right next test

The core issue: N_ur is the wrong physics for an epoch-localized domain. It contributes energy density proportional to (1+z)⁴ at *all* redshifts. The IDT domain should peak at z_c and decay rapidly on both sides.

**Quantitative comparison:**

At z = 10 (during structure formation):
- N_ur retains 9.1 × 10⁻¹⁰ of its z=2000 density
- Log-normal domain with σ_ln = 0.10 retains **exactly zero** (< 10⁻¹⁹⁴)
- Log-normal domain with σ_ln = 0.30 retains 4.7 × 10⁻⁶⁶

A narrow domain (σ_ln ≤ 0.15) is effectively absent during structure formation. This means:
1. It shifts r_d (active at z ~ 1000-3000) — addresses H₀
2. It does not add extra expansion during matter domination — does not worsen σ₈
3. It does not alter late-time distances — preserves SN constraints
4. It may actually *lower* σ₈ by changing the matter-radiation equality epoch, since it adds energy only near recombination and then disappears

This is the key scientific prediction to test: **a localized pulse-like domain can decouple the H₀ effect from the σ₈ effect, which the N_ur proxy cannot.**

If this prediction holds under CLASS perturbation calculation, it is a genuinely distinguishing feature of IDT compared to ΔN_eff models.

## D. Pulse-vs-merge interpretation in cosmology language

The "pulse vs merge" intuition maps onto a precise physical parameter: **the domain width σ_ln relative to the Hubble time at the domain epoch.**

**In cosmological language:**

The domain is an effective energy density contribution Ω_dom(z) with a characteristic timescale Δτ_dom in conformal time. The relevant comparison is Δτ_dom vs H⁻¹(z_c), the Hubble time at the domain epoch.

- **Pulse (Δτ_dom ≪ H⁻¹):** The domain appears and disappears within a fraction of a Hubble time. It perturbs the expansion rate briefly, shifts r_d if active near recombination, and then vanishes. σ_ln ≲ 0.10.

- **Sustained interaction (Δτ_dom ~ H⁻¹):** The domain persists for roughly one Hubble time. It has time to affect both the sound horizon and the matter-radiation equality transition. σ_ln ~ 0.15-0.30.

- **Merge (Δτ_dom ≫ H⁻¹):** The domain is present across multiple cosmological eras. It behaves like a new permanent component (effectively modifying Ω_r or Ω_m). N_ur is the extreme limit of this case. σ_ln > 0.5.

**The σ₈ lever is σ_ln.** Narrower domains (smaller σ_ln) shift r_d without lingering during structure formation. The parameter σ_ln directly controls whether the domain is a pulse or a merge. This is the single most important parameter for resolving the σ₈ issue.

**Translating to conformal time widths:**

For a log-normal domain at z_c = 2000:
- σ_ln = 0.05: domain active from z ≈ 1800 to 2200 (Δz/z_c ≈ 10%)
- σ_ln = 0.10: domain active from z ≈ 1600 to 2400 (Δz/z_c ≈ 20%)
- σ_ln = 0.15: domain active from z ≈ 1400 to 2700 (Δz/z_c ≈ 35%)
- σ_ln = 0.30: domain active from z ≈ 900 to 4000 (Δz/z_c ≈ 100%)

For H₀ tension: the domain must be active at z_drag ≈ 1060 to shift r_d. At z_c = 2000 with σ_ln = 0.15, the domain still has 0.013% of its peak density at z = 1060 — probably enough. At σ_ln = 0.10, it has 1.8 × 10⁻⁹ — likely too small.

**Critical constraint on σ_ln:** The domain must be wide enough to reach z ≈ 1060 (to shift r_d) but narrow enough to vanish by z ≈ 100 (to not affect structure formation). With z_c = 2000, this suggests σ_ln ≈ 0.12-0.20 as the sweet spot. With z_c = 1500, the domain is closer to recombination and can be narrower.

## E. Recommended minimal localized ρ_domain model

**Primitive object:** ρ_dom(z) as a log-normal profile in ln(1+z) space, exactly as currently implemented in `idt_domain.py`.

**Parameter set (3 free + 1 fixed):**

| Parameter | Symbol | Controls | Range |
|-----------|--------|----------|-------|
| Peak fraction | f_dom | Amplitude of domain contribution | 0.01 - 0.15 |
| Center redshift | z_c | Epoch of domain activity | 1200 - 3000 |
| Log-width | σ_ln | **Pulse vs merge** — duration of interaction | 0.05 - 0.40 |
| Sound speed² | c_s² | Perturbation clustering (fixed) | 1.0 |

**Why σ_ln and not Δ_z:** The current code uses Δ_z = σ_ln × (1+z_c), which mixes the width with the center. For CLASS implementation, σ_ln is the natural parameter because it directly measures the width in the natural log(1+z) coordinate.

**Why not add asymmetry:** An asymmetric pulse (fast rise, slow decay or vice versa) adds a 5th parameter without clear observational leverage. The log-normal is already symmetric in ln(1+z), which is the physically motivated coordinate. Asymmetry should only be added if the symmetric version fails to find viable parameter space.

**Conservation:** Guaranteed by construction. w(z) is derived from ρ(z) via the continuity equation: w(z) = -1 + (1/3) d(ln ρ)/d(ln(1+z)).

## F. Comparison of candidate localized shapes

### 1. Log-normal in ln(1+z) — RECOMMENDED

```
ρ_dom(z) = ρ_peak × exp(-½ [ln((1+z)/(1+z_c)) / σ_ln]²)
```

- **Physical story:** Domain interaction has a characteristic epoch and duration, symmetric in cosmological time
- **Pulse vs merge:** Controlled entirely by σ_ln. σ_ln = 0.1 is a pulse, σ_ln = 0.5 is a merge
- **w(z) behavior:** Analytically tractable. w(z_c) = -1 exactly. Phantom crossing on falling side — expected, not pathological
- **H₀ without σ₈:** Yes, if σ_ln ≲ 0.15 with z_c ~ 1500-2000
- **Implementation in CLASS:** Already coded in `class_integration.py` as C patches. Background patch is straightforward (4 lines of C). Perturbation patch exists but has a placeholder for dw/dlna
- **Risk:** w(z) becomes extreme far from z_c (w → ±∞), but ρ → 0 there so the product p = wρ remains well-behaved. CLASS may still flag extreme w values in internal checks
- **Recommendation:** Start here. Most theoretically motivated, simplest implementation, best-characterized behavior

### 2. Tanh window (smoothed step on, step off)

```
ρ_dom(z) = ρ_peak × ½[tanh((z-z_low)/w_low) - tanh((z-z_high)/w_high)]
```

- **Physical story:** Domain "arrives" at z_high and "departs" at z_low, with smooth transitions
- **Pulse vs merge:** Controlled by (z_high - z_low). Can model either
- **w(z) behavior:** More complex, needs numerical differentiation. w has features at both transitions
- **H₀ without σ₈:** Possible if z_low > 100
- **Implementation in CLASS:** Moderate. More parameters (z_low, z_high, w_low, w_high = 4-5 params). Conservation requires computing w from the profile
- **Risk:** Not symmetric in any natural coordinate. 4+ parameters is too many for Paper 1
- **Recommendation:** Consider for Paper 2 if asymmetry is needed

### 3. Compact polynomial bump (raised cosine)

```
ρ_dom(z) = ρ_peak × cos²(π/2 × min(|ln((1+z)/(1+z_c))|/σ_ln, 1))
```

- **Physical story:** Domain has compact support — exactly zero outside a finite range
- **Pulse vs merge:** Strict cutoff at σ_ln from center
- **w(z) behavior:** w(z) has a discontinuity in derivative at the edges. May cause numerical issues
- **H₀ without σ₈:** Yes, by construction (exactly zero at z < z_c × exp(-σ_ln))
- **Implementation:** Easy background, but derivative discontinuity may cause perturbation instabilities
- **Risk:** Less smooth than log-normal, may trigger CLASS numerical warnings
- **Recommendation:** Only if log-normal lingering is too large

**Clear recommendation: start with the log-normal (option 1).** It's already implemented in Python, the C patches exist, and it has analytically tractable derivatives. The key test is whether σ_ln ≈ 0.12-0.18 can simultaneously shift r_d and avoid structure-formation-era lingering.

## G. Audit of current CLASS integration path

### What exists (class_integration.py, Path 2):

**Background patch (lines 206-241):**
- Computes ρ_idt and w_idt from the log-normal profile directly in C
- Adds to Friedmann equation as `rho_tot += rho_idt`
- Uses hardcoded parameter values (generated from Python IDTDomain)
- **Status: Functionally correct. Needs integration into CLASS's background structure, not just pasted in.**

**Perturbation patch (lines 246-304):**
- Implements standard fluid δ̇ and θ̇ equations in synchronous gauge
- Uses c_s² = const (parameter) and computes c_a² from w and dw/dlna
- **Critical issue: `dw_dlna_idt = 0.0` is a placeholder.** This must be computed from the background table or analytically. For the log-normal, dw/dlna = +(1/3) × ln((1+z)/(1+z_c)) / σ_ln². This is NOT filled in.
- **Status: Incomplete. The dw/dlna placeholder makes the perturbation equations wrong.**

**Initial conditions patch (lines 309-338):**
- Adiabatic ICs: δ_idt = (3/4)(1+w_ini) × δ_γ
- **Issue: At early times (z ≫ z_c), w → +large. (1+w) is very large, making δ_idt huge.** This will likely cause instabilities. For a domain that is effectively absent at the initial time (ρ_idt ≈ 0 at z_ini ~ 10⁴), the perturbations should be initialized to zero, not to (1+w) × δ_γ.
- **Status: Likely wrong. Should set δ_idt = θ_idt = 0 when ρ_idt/ρ_tot < some threshold.**

### What needs to change:

1. **Background integration:** The domain must be added as a proper CLASS species with its own index in `pvecback`. CLASS tracks ρ and p for each species — we need `index_bg_rho_idt` and `index_bg_p_idt` registered in the background structure. The current patch just pastes code into `background_functions()` without registering indices.

2. **dw/dlna must be computed analytically:** For the log-normal:
   ```
   dw/d(ln a) = -(1+z) × dw/dz = (1/3) × [1/σ_ln² + ln²((1+z)/(1+z_c))/σ_ln⁴] / (something)
   ```
   Actually simpler: w = -1 + (1/3) × [-ln((1+z)/(1+z_c))/σ_ln²], so dw/d(ln(1+z)) = -(1/3σ_ln²), which is constant. Therefore dw/d(ln a) = +(1/3σ_ln²). This is trivial.

3. **Initial conditions must handle negligible-ρ regime:** When ρ_idt ≈ 0 at the initial time, set δ_idt = 0, θ_idt = 0. The domain perturbations should only be seeded when the domain is actually present.

4. **CLASS internal w-checks:** CLASS rejects w > 1/3 at early times (`background_checks`). The log-normal domain has w → +∞ far from z_c (where ρ → 0). Either: (a) clamp w to a maximum value when ρ is negligible, or (b) register the domain in a way that CLASS doesn't check its w independently.

### Hidden assumptions that could make the domain behave like EDE:

1. **If σ_ln is too large (> 0.3):** The domain persists through matter-radiation equality and into matter domination. This is functionally equivalent to EDE. The localization advantage only exists for σ_ln ≲ 0.20.

2. **If c_s² = 1 (stiff fluid):** The domain doesn't cluster, which is conservative. But if c_s² < 1, the domain would cluster and affect structure growth directly — potentially suppressing σ₈ further. This is a Paper 2 lever.

3. **If perturbation ICs are adiabatic:** The domain starts correlated with photons. For a domain that doesn't exist at early times, isocurvature (zero) ICs are more physical. Adiabatic ICs with large (1+w) could seed instabilities.

## H. Exact next coding plan

### Freeze now (commit as proxy milestone):
- Multi-domain proxy results (N_ur + CPL): H₀ = 71.7, Δχ² = -39.9
- All scanning code (parameter_scan.py, multi_domain_scan.py, full_parameter_scan.py)
- MCMC infrastructure (idt_mcmc.py, idt_mcmc_multidomain.py)
- Pre-MCMC diagnostics (σ₈ response, residual anatomy)
- This steering memo

### Implement next (CLASS source modification):

**Step 1: Background-only localized domain (no perturbations yet)**

Modify `archive/class/source/background.c`:
- Add 3 input parameters: `f_dom_idt`, `z_c_idt`, `sigma_ln_idt`
- Register `index_bg_rho_idt`, `index_bg_p_idt`, `index_bg_w_idt` in background structure
- Compute ρ_idt, p_idt, w_idt at each background integration step
- Add ρ_idt to total energy density
- Clamp w_idt to [-1, 1/3] when ρ_idt/ρ_tot < 10⁻¹⁰ to avoid CLASS checks failing

Modify `archive/class/source/input.c`:
- Read the 3 new parameters from .ini file

**Step 2: Background diagnostic outputs**

Before touching perturbations:
- Generate H(z), r_d, R, l_a for a grid of (f_dom, z_c, σ_ln) using the modified CLASS
- Compare against our Python standalone predictions to verify agreement
- Check that the domain properly vanishes at late times (z < 100)
- Verify flatness is maintained

**Step 3: Perturbation integration**

Only after background is verified:
- Add δ_idt, θ_idt to perturbation vector
- Use the equations from the existing patch BUT with correct dw/dlna = 1/(3σ_ln²)
- Set ICs: δ_idt = 0, θ_idt = 0 (isocurvature — domain absent at early times)
- Run CMB spectra and check stability across σ_ln = 0.08 to 0.30

**Step 4: σ₈ diagnostic**

- Compare σ₈ from localized domain vs N_ur proxy at matched r_d
- If σ₈ drops for narrow domains: the pulse hypothesis is confirmed
- If σ₈ stays high: the domain may need c_s² < 1 or late-time adjustment

### Diagnostic outputs before any MCMC:
1. Background comparison: Python standalone vs CLASS modified (must agree to < 0.1%)
2. H(z) plot: modified CLASS vs ΛCDM at the best-fit f_dom, z_c, σ_ln
3. TT/EE spectra: localized domain vs ΛCDM (stability check)
4. σ₈ vs σ_ln: the critical test. Plot σ₈ as a function of σ_ln at fixed f_dom, z_c

## I. Most important scientific caveats

1. **The N_ur proxy result (H₀=71.7) overstates the H₀ improvement.** N_ur adds energy at all redshifts including near z_drag, maximizing the r_d shift. A localized domain with σ_ln ~ 0.15 has much less energy at z_drag and will produce a smaller r_d shift. Expect H₀ ≈ 69-70 from the localized domain, not 72.

2. **The σ₈ prediction from the localized domain is currently unknown.** The N_ur proxy gives σ₈ = 0.88 (wrong direction). The localized domain should give something different, but we cannot predict what without running CLASS perturbations. The sign of the σ₈ effect is the key open question.

3. **The Δχ² improvement is partially from the H₀ term.** Of the -39.9 total, roughly -25 to -30 comes from reducing H₀ tension. The remaining -10 to -15 is from BAO and l_a adjustments. A localized domain that achieves less H₀ shift will have a correspondingly smaller Δχ².

4. **The perturbation equations have not been tested with the localized profile.** The dw/dlna placeholder in the existing C patches means perturbations have never been correctly computed for the log-normal domain. There is a real possibility of numerical instabilities, particularly near z_c where w = -1 and c_a² diverges.

5. **This model is structurally similar to EDE.** A reviewer will ask: "How is this different from Poulin et al. (2019)?" The honest answer: at the level of CLASS implementation, it is a new EDE-like component with a log-normal rather than axion profile. The IDT interpretation (domain interactions) is distinct from the EDE interpretation (axion field), but the computational signature may be similar. The distinguishing feature would be if IDT can access parameter space (particularly narrow σ_ln with lower σ₈) that EDE cannot.

6. **"Pulse vs merge" is a spectrum, not a binary.** The σ_ln parameter controls a continuum. Very narrow pulses may not shift r_d enough; very broad merges behave like extra radiation. The viable window, if it exists, is likely narrow: σ_ln ∈ [0.12, 0.20]. Whether this window produces both r_d shift AND σ₈ improvement is the central question for the next implementation step.
