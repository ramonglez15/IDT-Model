# Paper 2 — Unified Outline (Final)

## Comparison of sources

| Element | Outline 1 | Outline 2 | Outline 3 | My draft | Best version |
|---------|-----------|-----------|-----------|----------|-------------|
| **Title tone** | Slightly forward ("constraints and landscape") | Most conservative | Balanced ("predictions and constraints") | Moderate | Outline 3 |
| **Core framing** | Two objectives (JWST + η₀ landscape) | Parameter-space analysis | Landscape mapping, let data decide | Referee Q&A | Outline 3's landscape + Outline 2's tone |
| **JWST language** | "alignment with CEERS/JADES" (slightly strong) | "consistent with reported trends" (safe) | "partially alleviates... does not fully resolve" (honest) | "qualitatively consistent" | Outline 3 |
| **Ly-α framing** | "within current noise floors" | "indicative deviations, not direct exclusions" | "defines a falsifiable prediction for DESI" (turns weakness into strength) | "within systematic uncertainties" | Outline 3 |
| **l_a cooperation** | Not included | Not included | Full section (Section 3) — key discovery | Not included | Outline 3 (essential finding) |
| **η₀ presentation** | Maps landscape but selects best | Maps regimes without selecting | Maps full landscape, does NOT pick a winner | Picks η₀=-0.05 | Outline 3 |
| **Section structure** | 6 sections | 7 sections | 7 sections + appendices | 7 sections | Outline 3 |
| **Language discipline** | Good but occasional "optimal" | Excellent — explicit tone rules | Best — written rules enforced throughout | Good | Outline 3 |
| **What's missing** | l_a cooperation, limitations section | l_a cooperation, appendices | Nothing major | Landscape approach | — |
| **Unique strengths** | "expanded temporal baseline" physics language | Explicit "what to say / not say" guidance | l_a cooperation discovery; DESI as prediction not apology; "what Paper 2 does NOT do" list | DES Y3 update emphasis | — |

## Verdict

**Outline 3 is the backbone.** It has the strongest structure, the most defensible framing, and the key discovery (l_a cooperation) that the others miss. It also has the best tone discipline and the critical insight of NOT picking a single η₀.

**Outline 2 contributes the tone rules** — the explicit "say this / not that" guidance should be incorporated as an authoring standard.

**Outline 1 contributes the physics language** — "expanded temporal baseline for early halo collapse" is a cleaner physical description than my draft had.

**My draft contributes** the DES Y3 update emphasis and the explicit MCMC chain convergence reporting.

---

# UNIFIED OUTLINE

## Title

**Inflationary Domain Theory II: High-Redshift Structure Formation Predictions and Intermediate-Epoch Parameter Space Constraints**

---

## Language Rules (from Outline 2, enforced throughout)

- "consistent with" not "resolves" or "explains"
- "partially alleviates" not "solves"
- "to our knowledge" before uniqueness claims
- "approximate operational independence" not "complete decoupling"
- Present predictions as predictions, not fits
- No superlatives: no "remarkable," "striking," "powerful"
- Let tables and figures carry the argument, not adjectives

---

## Abstract (~250 words)

Structure: context → what this paper does → core results → interpretation → forward-looking

- In Paper 1 (Gonzalez 2026), we introduced IDT, a two-parameter extension of ΛCDM achieving ΔAIC = −8.1 through epoch-localized energy density contributions.
- The early domain (z_c ∼ 2000, f_dom ∼ 0.035), constrained by CMB + BAO + SN + H₀ data, modifies the matter power spectrum near the matter-radiation equality scale.
- With no additional parameters, this predicts a 20–50% enhancement in the abundance of UV-bright galaxies at z = 10–15, consistent with the elevated abundances reported by JWST surveys.
- This prediction is independent of the late-time dephasing coupling η₀, arising entirely from the early domain.
- We map the full η₀ parameter space against Ly-α forest, Thomson optical depth, and weak lensing constraints, finding: ΔAIC ranges from −5.5 to −8.3 across η₀ ∈ [−0.05, −0.01], with the model preferred over ΛCDM throughout.
- Both domains are structurally necessary for the acoustic scale correction: the early domain alone worsens l_a from 3.1σ to 4.0σ tension with Planck.
- The Ly-α one-dimensional matter power spectrum deviation ranges from 4% to 10%, with the upper range within current systematic uncertainties of flux power spectrum measurements but testable by forthcoming DESI Ly-α analyses.
- We update the statistical analysis with the DES Y3 weak lensing consensus (S₈ = 0.776 ± 0.017) and confirm ΔAIC = −8.3 at η₀ = −0.05 with four independent MCMC chains.

---

## 1. Introduction (2–3 pages)

### 1.1 The high-redshift galaxy abundance anomaly
- JWST spectroscopic confirmations of UV-bright galaxies at z > 10 in numbers exceeding ΛCDM predictions
- Accommodating these within standard structure formation requires star formation efficiencies approaching unity, in tension with feedback models
- This constitutes a third area of tension alongside H₀ and S₈
- Cite: Harikane+23, Finkelstein+23, Castellano+22, Naidu+22, Curtis-Lake+23, Bouwens+23, Pérez-González+23

### 1.2 Early-time modifications and high-z structure
- Models modifying pre-recombination expansion generically alter matter-radiation equality and reshape P(k)
- Demonstrated for EDE (Shen+24, Forconi+24), which enhances high-z galaxies but worsens σ₈
- IDT operates in similar redshift range but within a two-channel framework

### 1.3 Paper 1 summary and Paper 2 scope
- Paper 1: IDT with early domain (z_c = 2000) and late domain (z_c = 1.0), ΔAIC = −8.1
- Paper 2 scope:
  (a) Compute the P(k) enhancement and consequences for high-z halo abundances — a zero-parameter prediction
  (b) Map the full η₀ parameter space against Ly-α, τ, and CMB constraints
  (c) Demonstrate the structural necessity of both domains (l_a cooperation)
  (d) Identify falsifiable predictions for DESI and JWST
- **This paper does not introduce new parameters beyond Paper 1**

---

## 2. The JWST Prediction (3–4 pages)
*[Computed from Paper 1 parameters, not fitted]*

### 2.1 Matter power spectrum enhancement
- CLASS output P(k) at z = 10, 12, 15 for ΛCDM and IDT
- 2–8% broadband enhancement at halo-relevant scales (k ∼ 0.01–10 h/Mpc)
- Physical mechanism: early domain energy injection shifts matter-radiation equality, providing an expanded temporal baseline for early halo collapse
- **Figure 1:** P(k) ratio IDT/ΛCDM at z = 10, 12, 15

### 2.2 Halo mass function
- Tinker (2008) computed from CLASS P(k) (not Eisenstein-Hu approximation)
- Percent-level P(k) enhancements produce significant abundance changes on the exponential tail
- Enhancement table: 11–28% (M > 10¹⁰ M☉), 24–59% (M > 10¹¹ M☉), growing with redshift
- **Figure 2:** Cumulative halo mass function IDT vs ΛCDM

### 2.3 UV luminosity functions and JWST comparison
- Pipeline: M_halo → M_stellar (SHMR, ε = 0.10) → M_UV (Song+16)
- IDT UVLF sits above ΛCDM at the bright end
- Comparison with CEERS/JADES data: "predicts increased abundance consistent with reported trends"
- **IDT partially alleviates the ΛCDM tension with JWST without requiring extreme star formation efficiencies; it does not fully resolve the discrepancy at the brightest end**
- Sensitivity test: IDT/ΛCDM ratio stable across ε = 0.05 to 0.15
- **Figure 3:** UVLF at z = 10, 12, 15 with JWST data

### 2.4 Independence from the dephasing coupling
- JWST prediction identical across η₀ = 0, −0.01, −0.03, −0.05
- Enhancement arises entirely from the early domain
- Verified by running CLASS with late domain disabled
- **Figure 4:** UVLF overlay confirming η₀-independence

---

## 3. The Two-Domain Cooperation (2–3 pages)
*[Key discovery of Paper 2 — neither domain works alone]*

### 3.1 The acoustic scale requires both domains
- l_a analysis table:

  | Configuration | l_a | l_a tension |
  |---|---|---|
  | ΛCDM | 301.75 | 3.1σ |
  | Early only | 301.83 | **4.0σ** (worse) |
  | Early + Late, η₀ = −0.01 | 301.43 | 0.5σ |
  | Early + Late, η₀ = −0.03 | 301.46 | 0.1σ |
  | Early + Late, η₀ = −0.05 | 301.60 | 0.3σ |

- The early domain alone makes l_a worse, not better
- Early domain shifts r_d; without the late domain adjusting d_A(z*) through its effect on intermediate-redshift expansion, the angular ratio r_d/d_A(z*) overshoots
- Both domains are structurally necessary

### 3.2 Implications for parameter count
- The two-parameter extension is minimal — neither parameter is redundant
- This strengthens the ΔAIC interpretation: both parameters do necessary physical work

### 3.3 Refinement of the two-channel description
- Paper 1: early domain for geometry, late domain for growth
- Paper 2 refinement: early domain modifies r_d, late domain adjusts d_A(z*), together they correct l_a; the late domain additionally modifies growth through dephasing
- Channels are complementary on l_a, approximately independent on r_d and σ₈

---

## 4. The η₀ Parameter Space (3–4 pages)
*[Map the landscape — do NOT pick a single point]*

### 4.1 Updated MCMC
- Same likelihood as Paper 1 + updated S₈ = 0.776 ± 0.017 (DES Y3)
- 4 independent chains, 2000 steps each, 500 burn-in
- Acceptance rates: 11–14%

### 4.2 The landscape table (the key table of the paper)

  | | ΛCDM | η₀ = −0.01 | η₀ = −0.03 | η₀ = −0.05 |
  |---|---|---|---|---|
  | H₀ | 67.4 | 68.3 | 68.2 | 68.7 |
  | σ₈ | 0.811 | 0.816 | 0.816 | 0.821 |
  | S₈ | 0.830 | 0.824 | 0.829 | 0.833 |
  | l_a tension | 3.1σ | 0.1σ | 0.1σ | 0.3σ |
  | f_late | — | vestigial | active | active |
  | **ΔAIC** | **0** | **−5.5** | **−7.3** | **−8.3** |
  | Ly-α P₁D | 0% | 4.3% | 7.3% | 10.5% |
  | JWST enhancement | — | 20–50% | 20–50% | 20–50% |

- IDT preferred over ΛCDM at every tested η₀
- ΔAIC improves monotonically with |η₀|
- JWST prediction constant across all η₀
- **Figure 5:** ΔAIC, S₈ tension, Ly-α deviation vs η₀ (three-panel or two-axis)

### 4.3 The Ly-α trade-off
- Ly-α P₁D deviation increases with |η₀| because dephasing modifies the Poisson equation
- **Critical distinction:** the computed quantity is the **matter** P₁D; the observed quantity is the **flux** P₁D. The mapping depends on IGM thermal state, pressure smoothing, and the temperature-density relation, introducing 10–20% systematic uncertainties (cite Chabanier+19, Palanque-Delabrouille+20, Walther+19)
- At η₀ = −0.05, the 10% matter P₁D deviation maps to a smaller deviation in the flux P₁D after convolution with the thermal broadening kernel
- "These values should be interpreted as indicative deviations at the matter level rather than direct exclusions at the flux level"
- **Figure 6:** P₁D ratio at z = 2, 3, 4, 5 for each η₀

### 4.4 Thomson optical depth
- τ_eff ≈ 0.0547 across all η₀ configurations
- Within 0.1σ of Planck — enhanced galaxy abundances do not force premature reionization

### 4.5 What DESI will resolve
- DESI Ly-α measurements with improved thermal modeling will determine whether the matter P₁D enhancement at z = 2–5 is consistent with |η₀| > 0.03
- If confirmed → independent support for dephasing mechanism
- If excluded → favors weak dephasing, primarily single-channel model
- **Either outcome is informative**
- This turns the Ly-α deviation from a liability into a prediction

---

## 5. Discussion (2–3 pages)

### 5.1 IDT as a predictive framework
- Paper 1 constrained the early domain from data with no connection to high-z galaxy counts
- Paper 2 shows the same domain predicts abundance enhancements consistent with JWST
- The prediction preceded the comparison — not a fit

### 5.2 Comparison to EDE
- EDE enhances high-z galaxies through similar P(k) reshaping (Shen+24)
- IDT achieves comparable enhancement but within a framework that separately addresses late-time growth
- IDT's η₀ provides independent control on Ly-α deviation that EDE lacks

### 5.3 The structural necessity of two domains
- l_a cooperation analysis demonstrates the two-parameter model is minimal, not over-parameterized
- Addresses potential reviewer objection about parameter count

### 5.4 The parameter space as the result
- Paper 2 does not select a "best" η₀ — it maps the full landscape
- The data exhibit a clear preference for active dual-domain architecture (ΔAIC ≈ −8), which requires a Ly-α P₁D deviation at the matter level
- Whether this deviation is observationally acceptable is an empirical question that DESI will resolve

### 5.5 Limitations
- Star formation efficiency assumed constant (ε = 0.10); absolute UVLF depends on this, ratio does not
- Ly-α comparison uses matter P₁D, not flux P₁D; full comparison requires IGM thermal modeling
- Compressed Planck likelihood; full plik/CamSpec analysis deferred
- Halofit calibrated for ΛCDM; may not be fully accurate for IDT at high k
- MCMC uses Metropolis-Hastings; nested sampling would provide more robust evidence

---

## 6. Future Directions (1 page)

### 6.1 DESI Ly-α — the most immediate test
### 6.2 JWST deep surveys — testing the 20–50% enhancement
### 6.3 Full Planck likelihood — testing l_a cooperation under full analysis
### 6.4 Microphysical completion — first-principles derivation of η₀

---

## 7. Conclusions (1 page)

1. The early domain, constrained by the CMB acoustic scale, predicts 20–50% enhanced galaxy abundances at z > 10, consistent with JWST, with no new parameters
2. This prediction is independent of the dephasing coupling η₀
3. Both domains are structurally necessary: the early domain alone worsens l_a from 3.1σ to 4.0σ
4. IDT is preferred over ΛCDM (ΔAIC = −5.5 to −8.3) across the full tested η₀ range
5. The Ly-α P₁D deviation (4–10%) defines a falsifiable prediction for DESI
6. With updated DES Y3 S₈ prior, the best-fit ΔAIC = −8.3 confirms Paper 1
7. IDT connects the CMB acoustic scale, high-redshift galaxy formation, and intermediate-epoch constraints through epoch-localized energy contributions without exotic particle content

---

## Appendices

### A. Star formation efficiency sensitivity
### B. Halofit validation at high k
### C. Full η₀ sweep data table

---

## Figures (8 total)

1. P(k) ratio IDT/ΛCDM at z = 10, 12, 15
2. Cumulative halo mass function IDT vs ΛCDM
3. UV luminosity function with JWST data (z = 10, 12, 15)
4. UVLF independence from η₀ (overlay multiple curves)
5. η₀ landscape: ΔAIC, S₈, Ly-α vs η₀
6. P₁D ratio at z = 2–5 for each η₀
7. l_a cooperation table/figure
8. Thomson optical depth comparison

---

## What Paper 2 does NOT do

- Does not change the model or add parameters
- Does not present a different η₀ as "better" than Paper 1
- Does not include JWST data in the MCMC likelihood
- Does not claim to resolve the JWST anomaly (says "consistent with" and "partially alleviates")
- Does not dismiss the Ly-α deviation (maps it honestly and identifies it as a DESI prediction)

---

## Estimated length: 15–20 pages (PRD format)
## Target journal: Physical Review D
