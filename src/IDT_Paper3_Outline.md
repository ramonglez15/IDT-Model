# Paper 3 — Revised Outline

## Title

**Inflationary Domain Theory III: Phase Resonance, Gravitational Dephasing at the Lagrange Point, and the Conserved Net Impact Observable**

---

## Language Rules (carried from Paper 2 + reviewer-proofing)

- "consistent with" not "resolves" or "explains"
- "partially alleviates" / "substantially reduces" not "solves"
- Present derived quantities as derived, not assumed
- Let the progression table carry the argument
- No superlatives
- NEVER "derives from first principles" → "provides a data-supported relation"
- NEVER "the data require X" → "within tested configurations, X is not favored"
- Lagrange point is an ANALOGY, not literal physics → "analogous to" not "is"
- ΔAIC = −24 always anchored: "under the compressed Planck likelihood with P(k) constraints"
- The phase formalism is an EFFECTIVE description, assessed empirically
- IDT claim is: "lower-dimensional structure in parameter space selected by data" not "new fundamental physics"

---

## Key Results (for reference during writing)

Converged adaptive M-H, 4 independent chains, all R-hat < 1.1:
- ΔAIC ≈ −24 (penalty 12, 6 extra params)
- S8 = 0.767 (0.2σ) — resolved
- l_a = 301.47 (0.0σ) — perfect
- R = 1.749 (0.3σ) — excellent
- H0 = 68.12 (consistent with CMB cosmic average; local void accounts for SH0ES discrepancy)
- g_early = f×(1+η₀) = 0.035 (0.021–0.054) — converged conserved observable
- η₀ = −0.573 (−0.704 to −0.398)
- Δ = 0.359 (0.267–0.490)
- σ₈_CLASS = 0.847, σ₈_dephased = 0.745

---

## Abstract (~300 words)

- Papers 1–2 established IDT with hand-chosen domain widths and perturbative dephasing (η₀ = −0.05), achieving ΔAIC = −8.1.
- Paper 3 introduces three advances: (1) the MS phase quantum formalism, which provides a data-supported relation determining domain widths from a single parameter Δ, (2) full parameter liberation with converged posteriors from adaptive Metropolis-Hastings sampling, and (3) the finding that the data constrain the combination g = f_dom × (1 + η₀), which emerges as a conserved observable governing the net dephasing effect, rather than f_dom or η₀ individually.
- With 6 parameters beyond ΛCDM (all free, data-determined), the model achieves ΔAIC = −24 under the compressed Planck likelihood with additional P(k) constraints. The S₈ tension is reduced from ~3σ to 0.2σ. The CMB acoustic scale l_a is reproduced to 0.0σ.
- The dephasing parameter η₀ = −0.57 (−0.70 to −0.40) produces behavior analogous to a gravitational Lagrange point, where competing influences from two domains lead to partial cancellation of the net gravitational coupling.
- The conserved quantity g = 0.035 ± 0.016 explains a previously observed bimodal posterior as a physical degeneracy between neighbor configurations that produce identical net dephasing, not a convergence failure. This behavior is analogous to the emergence of Ωₘh² as the primary CMB-constrained quantity, suggesting that g may play a similar role in organizing domain-induced modifications to structure growth.
- H₀ = 68.1 ± 0.5 is consistent with the CMB-inferred global expansion rate. The discrepancy with local distance-ladder measurements may reflect the local void effect rather than requiring additional new physics.

---

## 1. Introduction (2–3 pages)

### 1.1 The parameter motivation problem
- Papers 1–2: ΔAIC = −8.1 with hand-chosen σ_ln and η₀ = −0.05
- Natural question: what do the data prefer when all parameters are free?
- Can the MS framework predict or constrain these parameters?

### 1.2 The MS phase quantum hypothesis
- Cosmological phase Φ(N) = ∫(1+w) dN tracks background evolution rate
- Hypothesis: each resonance window accumulates equal phase Δ
- This derives σ_ln from (Δ, z_c, cosmology) — one parameter replaces two per domain

### 1.3 From perturbative dephasing to partial gravitational cancellation
- Paper 1: η₀ = −0.05 (5% gravitational leakage, perturbative regime)
- Paper 3: the data select η₀ ≈ −0.50 (50% gravitational cancellation)
- This behavior is analogous to a Lagrange point in gravitational systems, where competing influences lead to partial cancellation
- The perturbative regime explored in Paper 1 is not favored within the tested parameter space

### 1.4 Paper 3 scope
- (a) Phase quantum formalism: derive σ_ln from Δ
- (b) Progressive parameter liberation with converged posteriors
- (c) Discovery of g = f×(1+η₀) as the conserved observable
- (d) Lagrange point interpretation of dephasing
- (e) S₈ resolution, CMB consistency, H₀ discussion
- **All parameters free, all posteriors converged (R-hat < 1.1), nothing hand-picked.**

---

## 2. The MS Phase Quantum Formalism (3–4 pages)

### 2.1 Cosmological phase and phase velocity
- Φ(N) = ∫(1+w_bg) dN; dΦ/dN = 1+w
- Radiation: 4/3 per e-fold; Matter: 1; Λ: 0 (phase frozen)
- **Figure 1:** Phase velocity vs redshift with domain windows overlaid

### 2.2 The constant phase quantum condition
- Δ = ∫(1+w) dN over resonance window
- Given Δ and z_c → σ_ln determined by root-finding
- Earlier resonances (faster phase) → narrower σ_ln
- **Figure 2:** σ_ln vs z_c for different Δ values

### 2.3 Parameter reduction
- Paper 1: 4 hand-chosen + 2 fitted = 6 params
- Paper 3: 6 free params (z_c×2, f_dom×2, Δ, η₀), σ_ln derived
- All free, nothing hand-picked

### 2.4 Computational implementation
- σ_ln recomputed at each MCMC step via bisection
- Self-consistent with changing cosmological parameters

### 2.5 Epistemological status of the phase formalism
- The phase formalism should be understood as an effective description that organizes the parameter space of IDT
- Its validity is assessed empirically, through its ability to reduce parameter freedom, improve fit quality, and produce consistent predictions across independent tests
- Three independent lines of evidence support it: (1) grid improvement over Paper 1, (2) Δ convergence under free-parameter MCMC, (3) robustness under dataset ablation (no-S₈ test)

---

## 3. Grid Validation (2 pages)

### 3.1 Design
- Paper 1 baseline (σ_early=0.18, σ_late=0.50): ΔAIC = −8.1
- Four MS σ pairs from Δ = 0.40, 0.55, 0.75, 1.00
- **Table 1:** Grid results

### 3.2 Results
- All four MS pairs beat Paper 1
- Best: Δ = 0.75, ΔAIC = −12.8 (improvement of 4.7)
- Paper 1's hand-chosen σ_early was suboptimal
- **Figure 3:** ΔAIC vs Δ

---

## 4. Progressive Parameter Liberation (4–5 pages)

### 4.1 Free Δ (k=3): ΔAIC = −9.7
### 4.2 Free Δ + η₀ (k=4): ΔAIC = −19.5, η₀ hits prior wall at −0.15
### 4.3 Full free, 9 params (k=6): ΔAIC = −23.0, η₀ hits wall at −0.20
### 4.4 Wide-wall exploration: η₀ settles at −0.40 to −0.53

### 4.5 The progression table

| Config | H0 | σ₈_deph | S8 | l_a | Δ | η₀ | k | ΔAIC |
|---|---|---|---|---|---|---|---|---|
| ΛCDM | 67.4 | 0.811 | 0.830 | 3.1σ | — | — | 0 | 0 |
| Paper 1 | 68.4 | 0.809 | — | 0.1σ | — | −0.05 | 2 | −8.1 |
| Grid best | 68.0 | 0.803 | — | 0.4σ | 0.75 | −0.05 | 2 | −12.8 |
| Free Δ | 67.6 | 0.802 | 0.822 | 0.1σ | 0.73 | −0.05 | 3 | −9.7 |
| Free Δ+η₀ | 68.3 | 0.775 | 0.792 | 0.4σ | 1.34 | −0.147 | 4 | −19.5 |
| Full free | 68.1 | 0.745 | 0.767 | 0.0σ | 0.36 | −0.57 | 6 | −24 |

- **Figure 4:** ΔAIC progression
- **Figure 5:** S₈ tension progression

---

## 5. Converged Posteriors and the Conserved Observable (3–4 pages)
*[The major new contribution]*

### 5.1 Sampler choice: adaptive M-H vs ensemble methods
- emcee stretch move fails R-hat (1.4–1.8) due to elongated correlations
- Adaptive M-H with learned covariance: 4 independent chains, all R-hat < 1.1
- CosmoMC-style approach validated for IDT parameter space
- **Table 2:** R-hat values for all 9 parameters

### 5.2 The conserved quantity g = f × (1+η₀)
- MCMC reveals bimodal posterior in (f, η₀) space
- Basin 1: η₀ ≈ −0.36, f_early ≈ 0.055, Δ ≈ 0.50
- Basin 2: η₀ ≈ −0.67, f_early ≈ 0.102, Δ ≈ 0.32
- Three parameters scale by the same factor (0.53×): f_early, f_late, η₀
- But g = f×(1+η₀) is identical across basins: 0.031 vs 0.031
- The data constrain the product, not the factors
- Analogous to Ωₘh² being the CMB-constrained quantity, not Ωₘ and h separately
- **Figure 6:** g_early posterior (unimodal) vs f_early posterior (bimodal)
- **Figure 7:** f_early vs η₀ scatter colored by g_early

### 5.3 Physical interpretation: neighbor geometry degeneracy
- Both basins produce identical net gravitational dephasing
- Basin 1: weak coupling to strongly resonating neighbor
- Basin 2: strong coupling to weakly resonating neighbor
- The degeneracy is physical, not a fitting artifact
- Breaking it requires observables sensitive to f and η₀ separately (e.g., scale-dependent P(k) suppression)

### 5.4 Converged posterior summary
- g_early = 0.035 (0.021–0.054): the net dephasing impact
- η₀ = −0.57 (−0.70 to −0.40): coupling strength (degenerate with f)
- Δ = 0.36 (0.27–0.49): universal phase quantum
- z_c_early = 2254 (1433–3517): early resonance epoch
- z_c_late = 1.82 (1.09–2.50): late resonance epoch
- **Figure 8:** Corner plot (key parameters)

---

## 6. The Physics of Dephasing (2–3 pages)

### 6.1 The Lagrange point analogy
- At L1 between two gravitating bodies, net gravitational acceleration is reduced by competing influences
- The effective gravitational coupling during domain resonance exhibits analogous behavior: partial cancellation from competing organizational demands
- η₀ quantifies the cancellation fraction
- η₀ = −0.50 → approximately symmetric cancellation (analogous to equal-mass L1)
- η₀ = 0 → no neighbor influence
- η₀ = −1 → complete cancellation (physical limit: G_eff = 0)
- This analogy is descriptive, not constitutive — the mathematical content is G_eff = 1 + η₀·Γ(z)
- **Figure 9:** G_eff(z) profile at best-fit parameters

### 6.2 The resonance framework
- Domain interactions occur through phase resonance, not spatial overlap
- The MS has distance but no time; resonance occurs when our phase matches the neighbor's
- z_c = resonance redshift; σ_ln = resonance width; f_dom = resonance amplitude
- The Gaussian profile in ln(a) is the resonance response curve
- At peak resonance, domain energy has w = −1 (vacuum-like) — Friedmann–Poisson decoupling

### 6.3 Why S₈ is resolved but H₀ is not
- σ₈ depends on growth rate during z ~ 0.5–2 (where late-domain dephasing operates)
- H₀ depends on the distance ladder anchored by r_d (set at z ~ 1100, before any domain resonance)
- IDT modifies growth at the right epoch for S₈ without affecting the sound horizon
- The Hubble tension is fundamentally an r_d–H₀ constraint that IDT does not address
- H₀ = 68.1 is the cosmic average; the local void may account for SH0ES's 73.0

---

## 7. Robustness Tests (2 pages)

### 7.1 BBN verification
- Domain energy density at z ~ 10⁹: < 10⁻⁷¹ of total
- 20–60σ from nucleosynthesis epoch — zero impact
- This places the model safely outside the regime relevant for nucleosynthesis constraints

### 7.2 Three-domain test
- Scanned third domain at z = 5000, 8000, 15000, 30000, 50000
- No improvement in logL at any redshift
- Within the tested configurations, no additional domains are favored by the data
- The bimodality is a parameter degeneracy, not evidence for missing domains

### 7.3 σ₈_CLASS constraint
- σ₈_CLASS < 0.85 enforced to maintain perturbation theory validity
- Basin 2 MAP has σ₈_CLASS = 0.847 — constraint is not strongly binding
- Relaxing to 0.95 or removing does not change the preferred H₀

### 7.4 Convergence across samplers
- Metropolis-Hastings: ΔAIC = −22.4
- emcee (64 walkers): ΔAIC = −24.9
- Adaptive M-H (4 chains): ΔAIC ≈ −24
- Result is sampler-independent

---

## 8. Predictions and Future Tests (2 pages)

### 8.1 DESI BAO
- Preliminary analysis with DESI DR1 shows IDT naturally accommodates DESI's evolving dark energy signal
- The late domain at z_c ~ 1.8 produces an effective w(z) that mimics w₀wₐCDM
- Full DESI analysis deferred to Paper 4

### 8.2 Ly-alpha P1D at η₀ ≈ −0.57
- Substantially stronger P(k) suppression than Paper 2's η₀ = −0.05
- DESI Ly-alpha becomes a critical discriminant
- Predicted: +17% at z=2, +22% at z=3

### 8.3 CMB lensing
- σ₈_dephased = 0.745 vs σ₈_CLASS = 0.847
- 12% suppression should be visible in CMB lensing power spectrum
- ACT/SPT measurements provide independent test

### 8.4 JWST prediction unchanged
- The JWST 20–50% high-z enhancement from Paper 2 depends on the early domain alone
- Independent of η₀, Δ, and z_c_late — survives Paper 3's parameter revision

### 8.5 The conserved observable as a prediction
- g = f×(1+η₀) = 0.035 ± 0.016 is a specific numerical prediction
- Future data (DESI DR2, Euclid, CMB-S4) will constrain g more precisely
- If g is robust across datasets, it measures a fundamental property of the domain resonance

---

## 9. Discussion (2 pages)

### 9.1 What Paper 3 claims
- IDT with 6 free parameters is statistically preferred over ΛCDM under the adopted likelihood (ΔAIC = −24)
- S₈ tension is resolved through transient gravitational dephasing at a phase-space Lagrange point
- The posterior is unimodal in g = f×(1+η₀); the apparent bimodality in (f, η₀) space is a physical degeneracy
- All posteriors converged (R-hat < 1.1, 4 independent chains)

### 9.2 What Paper 3 does NOT claim
- Does not resolve the Hubble tension (H₀ = 68.1, consistent with CMB average)
- Does not derive Δ from first principles (measured at 0.36 ± 0.11)
- Does not specify the nature of the MS substrate (G_eff modification is testable regardless)
- Does not use full Planck likelihood (compressed R, l_a, ωbh²)

### 9.3 Connection to the broader landscape
- IDT's transient G_eff modification is a new class of modified gravity: epoch-specific, self-terminating
- The Lagrange point analogy connects the phenomenology to familiar gravitational physics
- The conserved quantity g parallels the emergence of Ωₘh² as a fundamental observable
- The overall finding: a lower-dimensional structure in the parameter space, selected by the data, that produces consistent predictions — this is the core claim of Paper 3

---

## 10. Conclusions (1 page)

1. The MS phase quantum Δ provides a data-supported relation that determines domain widths, reducing free parameters.
2. All MS-predicted σ pairs outperform Paper 1's hand-tuned values.
3. With 6 free parameters beyond ΛCDM, the model achieves ΔAIC = −24 under compressed Planck + P(k) constraints, with all R-hat < 1.1.
4. The net dephasing impact g = f×(1+η₀) = 0.035 ± 0.016 is the conserved observable.
5. The bimodal posterior in (f, η₀) space represents a physical degeneracy between neighbor configurations.
6. Dephasing operates as gravitational cancellation at a phase-space Lagrange point (η₀ ≈ −0.57).
7. S₈ reduced from ~3σ to 0.2σ; l_a consistent to 0.0σ; H₀ = 68.1 (cosmic average).
8. The JWST prediction from Paper 2 survives parameter revision.

---

## Appendices

### A. Phase quantum solver implementation
### B. Adaptive M-H sampler details and convergence diagnostics
### C. Full progression data tables (all MCMC runs)
### D. Correlation matrices and corner plots
### E. Three-domain scan results
### F. σ₈_CLASS cap analysis

---

## Figures (10–12 total)

1. Phase velocity dΦ/dN vs redshift with domain windows
2. σ_ln vs z_c for different Δ values
3. Grid test: ΔAIC vs Δ
4. ΔAIC progression as parameters freed
5. S₈ and H₀ tension progression
6. g_early posterior (unimodal) vs f_early posterior (bimodal)
7. f_early vs η₀ scatter colored by g_early (showing the degeneracy)
8. Corner plot (key parameters: H₀, g_early, η₀, Δ, z_c_early)
9. G_eff(z) profile at best-fit parameters
10. R-hat convergence comparison: emcee vs adaptive M-H
11. Chi-squared breakdown: ΛCDM vs IDT
12. Three-domain scan results (null result)

---

## Estimated length: 20–25 pages (PRD format)
## Target journal: Physical Review D
