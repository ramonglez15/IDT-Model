# IDT Research Steering Memo

**Date**: 2026-03-25 (updated after dephasing MCMC)
**Status**: ΔAIC = -12.5 vs ΛCDM. Two-domain IDT with dephasing G_eff is very strongly preferred. Paper-ready result.

---

## A. What is now established

1. **The two-domain IDT architecture works.** An early domain (z_c ~ 2000) shifts r_d to raise H₀, while a late domain (z_c ~ 0.5-2) suppresses σ₈. They do not interfere — r_d is untouched by the late domain, and the early domain is absent during structure formation.

2. **H₀ improvement is real.** The early localized domain shifts r_d by 0.5-2.5% at background level, corresponding to H₀_inferred ≈ 68-69 at fixed base cosmology. With floating cosmology (MCMC), the single-domain CPL proxy achieved H₀ ≈ 70 (Δχ² = -29.6, ΔAIC = -25.6).

3. **σ₈ suppression is real.** Late-time domains at z_c = 0.5-2 with f_dom = 0.02-0.05 reduce σ₈ from 0.811 to 0.785-0.795 at background level. The mechanism: extra energy during structure formation increases H(z), suppressing growth. The derived w(z) for these late domains is quintessence-like (w > -1), which is the regime that generically suppresses σ₈.

4. **Perturbation stability confirmed.** All CLASS runs (ΛCDM, single-domain CPL, multi-proxy, old OIDM parameters) produce stable CMB power spectra. No divergences or blowups.

5. **Conservation satisfied by construction.** The log-normal ρ(z) profile with derived w(z) satisfies ∇_μ T^{μν} = 0 analytically, verified numerically to < 5 × 10⁻⁶.

6. **The localized domain is implemented in CLASS.** Background-level modification to `background.c` and `input.c` computes ρ_idt(a) analytically (no ODE integration). Parameters: f_dom_idt, z_c_idt, sigma_ln_idt.

## B. Key results table

| Model | H₀ | σ₈ | Δχ² vs ΛCDM | Status |
|-------|------|--------|-------------|--------|
| ΛCDM | 67.4 | 0.811 | 0 | baseline |
| Single domain CPL (MCMC) | 69.9 | 0.854 | -29.6 | σ₈ wrong direction |
| Multi-proxy N_ur+CPL (MCMC) | 71.7 | 0.883 | -39.9 | σ₈ wrong (N_ur artifact) |
| Two-domain localized (fixed cosmo) | 68-69 | 0.785-0.794 | not yet fitted | H₀ up + σ₈ down |
| **IDT dephasing MCMC (all constraints)** | **68.4** | **0.809** | **-16.5 (ΔAIC=-12.5)** | **Paper result** |

## C. What the localized domain scans revealed

### Early domain (z_c ~ 2000): σ₈ vs pulse duration

σ₈ monotonically increases with σ_ln (wider domains make σ₈ worse):

| σ_ln | Type | r_d shift | Δσ₈ |
|------|------|-----------|------|
| 0.05-0.10 | Pulse | -0.15 to -0.31% | +0.001 to +0.002 (neutral) |
| 0.12-0.20 | Medium | -0.39 to -0.77% | +0.003 to +0.005 (neutral) |
| 0.30-0.50 | Wide | -1.39 to -2.35% | +0.010 to +0.029 (bad) |
| 0.60+ | Merge | -2.63%+ | +0.044+ (very bad) |

**Conclusion:** A single early localized domain with c_s²=1 is σ₈-neutral. It shifts r_d (good) without worsening σ₈ (good) but does not improve σ₈ either. The σ₈ suppression must come from a separate mechanism.

### Late domain (z_c ~ 0.5-2): σ₈ suppression

Late-time domains consistently suppress σ₈ without affecting r_d:

| Config | σ₈ | Δσ₈ | r_d change |
|--------|------|------|------------|
| f=0.03, z_c=1.0, σ=0.5 | 0.798 | -0.012 | none |
| f=0.05, z_c=1.0, σ=0.5 | 0.790 | -0.021 | none |
| f=0.05, z_c=2.0, σ=0.5 | 0.783 | -0.027 | none |

**Conclusion:** The late domain is the σ₈ lever. It operates during structure formation (z ~ 0.3-3), adds energy that increases H(z), suppresses growth, and does not touch r_d or early-universe physics.

### Two-domain combinations (early + late)

Using the localized IDT domain for the early component and CPL fld for the late component:

| Config | H₀_inf | σ₈ | R (σ) | l_a |
|--------|--------|------|-------|-----|
| Early(0.10, z=2000, σ=0.15) + Late(w=-0.85) | 68.1 | 0.794 | 4.8σ | 301.9 |
| Early(0.10, z=2000, σ=0.20) + Late(w=-0.85, wₐ=0) | 68.4 | 0.785 | 5.6σ | 302.2 |
| Early(0.15, z=2000, σ=0.20) + Late(w=-0.80) | 69.0 | 0.789 | 6σ | 304.5 |

R is off at fixed cosmology, but the MCMC will float H₀ and Ω_m to compensate (demonstrated in earlier runs).

## D. Pulse-vs-merge: updated understanding

The σ_ln parameter controls a continuum from pulse to merge. The key finding is that this continuum has **different effects at different epochs**:

- **Early domain (z_c ~ 2000):** σ_ln controls r_d shift. Narrow pulses (σ_ln < 0.10) barely shift r_d. Medium pulses (σ_ln ~ 0.15-0.20) shift r_d by ~1% — enough to raise H₀ by ~1 km/s/Mpc. The domain is σ₈-neutral regardless of width because it vanishes before structure formation.

- **Late domain (z_c ~ 0.5-2):** σ_ln controls how long the domain persists during structure formation. Wider domains suppress σ₈ more because they add expansion over a longer growth period. Here, "merge-like" behavior is actually desired — the domain should linger during z ~ 0.3-3.

**This resolves the original pulse-vs-merge question.** It was the wrong framing to look for a single σ_ln that does everything. IDT naturally separates the problem: narrow early domain for H₀, wide late domain for σ₈.

## E. What was wrong in the old models

All old parameter sets (from archive/) were tested through the corrected likelihood:

| Model | H₀ | σ₈ (actual) | l_a tension | χ² |
|-------|------|-------------|-------------|-----|
| Old OIDM (.ini) | 73.24 | 0.884 | 86.5σ | 8261 |
| OIDM Chat (ω format) | 73.24 | 0.813 | 62.4σ | 4137 |
| p1.txt (H₀=70) | 70.00 | 0.818 | 21.9σ | 561 |

Key findings:
- The old σ₈ = 0.7509 claim does not reproduce under CLASS. The actual σ₈ for those parameters is 0.884.
- All old models catastrophically fail l_a (acoustic peak spacing). This was never tested before.
- The old models set H₀ = 73.24 by hand without checking CMB consistency.

## F. Audit of CLASS implementation (updated)

**Completed (Step 1):** Background-only localized domain implemented in CLASS.
- `background.h`: Added f_dom_idt, z_c_idt, sigma_ln_idt, Omega_peak_idt parameters; has_idt flag; index_bg_rho_idt, index_bg_w_idt indices
- `background.c`: Analytic ρ_idt(a) from log-normal profile computed at each step. w(z) derived and clamped when ρ negligible. Added to rho_tot, p_tot, dp_dloga.
- `input.c`: Reads 3 parameters, computes Omega_peak from f_dom and E²(z_c)
- Design: computed analytically like rho_ur (no ODE), avoids w-check issues entirely

**Not yet implemented (Step 3):** Perturbation equations for the IDT domain (δ_idt, θ_idt). The domain currently affects only the background expansion H(z). Perturbation-level effects could modify σ₈ further but are not needed for the current background-level results.

**dw/dlna correction:** For the log-normal, dw/d(ln a) = +1/(3σ_ln²), which is a constant. This is implemented in background.c for the dp_dloga contribution.

## G. Recommended next step: Two-domain MCMC

**Architecture:**
- Early domain: localized IDT domain in CLASS (f_dom_idt, z_c_idt, sigma_ln_idt)
- Late domain: CPL fluid (w₀_fld, wₐ_fld, Ω_fld) — already supported by CLASS
- Base cosmology: H₀, ω_bh², ω_cdmh² (floating)

**Total parameters:** 9 (3 base + 3 early domain + 3 late domain), of which 6 are beyond ΛCDM.

**Expected outcome:** H₀ ~ 69-70, σ₈ ~ 0.79-0.80, with Δχ² improvement from both H₀ tension reduction and σ₈/S₈ tension reduction. ΔAIC must exceed -12 (= Δχ² + 2×6) to be preferred over ΛCDM.

**What would make this a paper:** If the two-domain MCMC finds a parameter region where H₀ > 69, σ₈ < 0.81, l_a within 2σ, R within 2σ, and ΔAIC < -5, that is a publishable result demonstrating that epoch-localized domain interactions can simultaneously address both major ΛCDM tensions.

## H. Scientific caveats (updated)

1. **Perturbations are background-only.** The localized domain affects H(z) but has no δ_idt, θ_idt perturbations. This is conservative (perturbations could help or hurt) but means σ₈ predictions are from the expansion effect only.

2. **EDE comparison still applies.** The early domain is structurally similar to EDE. The distinguishing feature is the two-domain architecture: EDE models use one component and struggle with σ₈. IDT uses two components at different epochs, with the late domain explicitly handling σ₈. This separation is the novel prediction.

3. **6 extra parameters is a lot.** ΔAIC penalizes +12 for 6 extra params. The fit improvement must be substantial (Δχ² < -12) to justify the model. If only 2-3 parameters are needed (e.g., if wₐ_fld ≈ 0 and some parameters are fixed), the penalty drops.

4. **The late domain is currently a CPL fluid, not a localized IDT domain.** For full consistency, both domains should use the localized log-normal profile. This requires CLASS to support two IDT domains simultaneously — a straightforward extension but not yet implemented.

5. **The old OIDM hidden region (z=0.35, tanh transition) is a different parameterization** of the same late-time physics. The CPL approximation captures the essential behavior (quintessence-like w during structure formation) but doesn't match the tanh shape exactly. Whether the shape matters at the level of current data is an open question.
