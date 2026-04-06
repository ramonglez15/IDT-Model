# Paper 2 Outline: Observational Predictions and Consistency Tests for Epoch-Localized Domain Interactions

**Working title:** *Epoch-Localized Domain Interactions II: High-Redshift Structure Formation, Ly-α Forest Constraints, and Observational Predictions*

**Author:** Jose Ramon Gonzalez

---

## Positioning

Paper 1 introduced the IDT framework and demonstrated statistical preference over ΛCDM (ΔAIC = −8.1) using CMB, BAO, SN, and local H₀ data. Paper 2 does **not** claim new tension resolution. Instead, it asks two questions that any referee of Paper 1 would ask:

1. Does the model make testable predictions beyond the data it was fit to?
2. Does the model violate constraints that were not included in the original fit?

The answer to (1) is yes — IDT predicts enhanced high-z galaxy abundances observable by JWST. The answer to (2) is no — the model is consistent with Ly-α forest, Thomson optical depth, and non-linear structure constraints within current systematic uncertainties. Along the way, we update the statistical analysis with the DES Y3 weak lensing prior and confirm ΔAIC = −8.3.

---

## Abstract (draft)

In a companion paper [Paper 1], we introduced Inflationary Domain Theory (IDT), a two-parameter extension of ΛCDM using epoch-localized energy densities, and showed that it achieves ΔAIC = −8.1 against compressed Planck, BAO, SN, and local H₀ data. Here we examine the observational consequences of the IDT best-fit model beyond the datasets used in the original fit. We compute the linear matter power spectrum P(k) at z = 10–15 using the modified CLASS Boltzmann solver and translate the predicted halo abundances into UV luminosity functions via the Tinker (2008) mass function. We find that the IDT early domain (z_c ≈ 2000, f_dom ≈ 0.035) enhances the predicted number density of UV-bright galaxies by 20–50% relative to ΛCDM at z = 10–15, with the largest enhancement at the bright end — qualitatively consistent with the abundance of massive galaxies reported by JWST surveys. We then perform consistency checks against intermediate-redshift constraints not included in the Paper 1 fit: the Lyman-α forest one-dimensional power spectrum at z = 2–5, the Thomson optical depth to reionization, and the non-linear matter power spectrum. The Ly-α P₁D deviations reach ∼10% at z = 2, which we show is within the systematic uncertainty budget of current flux power spectrum measurements. The Thomson optical depth remains within 0.1σ of the Planck constraint. We update the MCMC analysis with the DES Y3 weak lensing consensus (S₈ = 0.776 ± 0.017) and confirm ΔAIC = −8.3 with four independent chains. The IDT framework thus produces a falsifiable prediction for high-redshift galaxy surveys while remaining consistent with existing intermediate-redshift constraints.

---

## Section 1: Introduction

### 1.1 Context and motivation
- Brief recap of ΛCDM tensions (H₀, S₈, l_a) — cite Paper 1, do not re-derive
- The IDT two-channel architecture: early domain shifts r_d (fixes l_a, raises H₀), late domain modifies G_eff via dephasing (suppresses growth)
- Paper 1 result: ΔAIC = −8.1 with 2 extra parameters, using compressed Planck + BAO + SN + SH0ES + WL

### 1.2 Scope of this paper
- Paper 1 used a specific dataset combination. Natural questions arise:
  - What does the model predict for observations **not** included in the fit?
  - Are there datasets that could **exclude** the model?
- This paper addresses both: predictions (JWST high-z galaxies) and consistency tests (Ly-α, τ, non-linear P(k))
- We also update the statistical analysis with the DES Y3 S₈ prior

### 1.3 Organization
- Section 2: review of IDT framework and CLASS implementation (brief, referencing Paper 1)
- Section 3: high-z structure formation predictions
- Section 4: intermediate-redshift consistency checks
- Section 5: updated MCMC with DES Y3 prior
- Section 6: discussion
- Section 7: conclusions

---

## Section 2: Framework and Implementation (brief)

### 2.1 IDT parameterization
- Reference Paper 1 Sections 2–3 for full derivation
- State the model: two log-normal domains with (f_dom, z_c, σ_ln) each, plus dephasing coupling η₀
- Best-fit from Paper 1: f_early = 0.035, z_c = 2000, σ_ln = 0.18; f_late < 0.006, z_c = 1.0, σ_ln = 0.5; η₀ = −0.05

### 2.2 Modified CLASS solver
- Brief description of modifications to background.c, perturbations.c, input.c
- G_eff = 1 + η₀ Γ(z) applied to Poisson equation source terms
- Code publicly available at [repository]

---

## Section 3: High-Redshift Structure Formation

*This section makes the offensive case: IDT predicts something testable.*

### 3.1 Linear matter power spectrum at z = 10–15
- Run CLASS for both ΛCDM (Planck 2018 best-fit) and IDT (Paper 1 best-fit)
- Output P(k) at z = 10, 12, 15
- Plot P(k) ratio IDT/ΛCDM: broad enhancement of 2–8% at k = 0.01–10 h/Mpc
- Physical mechanism: early domain energy injection near z ∼ 2000 shifts the matter-radiation equality epoch, modifying the P(k) turnover scale
- **Key point: the enhancement is driven entirely by the early domain, which is the same component that resolves the l_a tension. This is not a free parameter tuned to match JWST — it is a consequence of the CMB fit.**

### 3.2 Halo mass function
- Compute σ(R) from CLASS P(k), apply Tinker (2008) multiplicity function
- Compare dn/dlnM and cumulative n(>M) for both models
- IDT predicts 11–28% more halos with M > 10¹⁰ M☉ at z = 10–15, increasing to 24–59% for M > 10¹¹ M☉
- Enhancement grows with mass (exponential tail sensitivity) and redshift

### 3.3 UV luminosity function
- Convert halo masses to stellar masses via constant SFE: M* = ε f_b M_h (ε = 0.10)
- Convert to UV magnitudes via Song et al. (2016) calibration
- Plot UVLF Φ(M_UV) for both models at z = 10 and 12
- Include representative JWST data points from Bouwens et al. (2023), Harikane et al. (2023), Pérez-González et al. (2023)
- IDT enhancement: 12–49% more UV-bright galaxies, with largest effect at bright end (M_UV < −20)

### 3.4 Discussion of SHMR uncertainties
- The absolute UVLF prediction depends on the assumed SFE (ε) and M*–M_UV calibration
- **The IDT/ΛCDM ratio is robust to these assumptions** because it cancels in the ratio
- Table showing ratio is independent of ε
- The prediction is: "whatever SFE makes ΛCDM work, IDT predicts X% more galaxies at the same SFE"
- This is falsifiable: as JWST survey volumes grow and SFE constraints improve, the enhancement is directly testable

---

## Section 4: Intermediate-Redshift Consistency Checks

*This section makes the defensive case: IDT does not violate existing constraints not included in the Paper 1 fit.*

### 4.1 Lyman-α forest one-dimensional power spectrum
- Compute P₁D(k) at z = 2, 3, 4, 5 from the non-linear (Halofit) 3D P(k) via transverse integration
- IDT/ΛCDM ratio: 3–10% enhancement, largest at z = 2
- **Comparison to observational uncertainties:**
  - The matter P₁D is not directly observed; the Ly-α flux power spectrum depends on IGM thermal state, pressure smoothing, temperature-density relation, and mean flux
  - Current eBOSS Ly-α flux P₁D measurements carry 10–20% systematic uncertainties from these modeling choices (cite Chabanier et al. 2019, Palanque-Delabrouille et al. 2020)
  - A 10% deviation in the matter P₁D maps to a smaller deviation in the flux P₁D after convolution with the thermal broadening kernel
  - **Conclusion: the IDT deviation is within current systematic uncertainties and does not constitute a tension**
- Note that future DESI Ly-α measurements with improved thermal modeling will provide a more stringent test

### 4.2 Thomson optical depth
- The enhanced halo abundance at z > 10 produces additional ionizing photons
- Estimate the extra contribution to τ from 20–50% more halos at z = 8–15
- Result: Δτ ≈ 0.0004, giving τ_eff = 0.0547
- Planck constraint: τ = 0.054 ± 0.007 → tension = 0.1σ
- **Conclusion: negligible impact on reionization constraints**

### 4.3 Non-linear regime at high redshift
- Halofit cannot compute non-linear corrections at z > 6 (k_NL too small)
- This is expected: at z > 10, structures are in the linear-to-mildly-nonlinear regime
- The halo mass function calculation uses linear P(k), which is the standard approach
- The IDT P(k) enhancement (2–8%) is a linear-theory prediction and does not depend on non-linear modeling

---

## Section 5: Updated Statistical Analysis

### 5.1 Updated likelihood
- Same likelihood as Paper 1: compressed Planck (R, l_a, ω_b) + BAO (5 pts) + SN (Pantheon+ shape) + SH0ES H₀ + weak lensing S₈
- Update: S₈ = 0.776 ± 0.017 (DES Y3 consensus), replacing 0.770 ± 0.017 used in Paper 1

### 5.2 MCMC configuration
- Same sampler, priors, and floating parameters as Paper 1
- 4 independent chains, 2000 steps each, 500 step burn-in
- Acceptance rates: 11–13%

### 5.3 Results
- **ΔAIC = −8.3** (consistent across all 4 chains: −7.7, −8.3, −8.3, −8.3)
- Best-fit parameters consistent with Paper 1:
  - H₀ = 68.6 km/s/Mpc
  - f_early = 0.029–0.039
  - f_late < 0.005
  - l_a tension: 0.3–0.7σ (resolved)
  - H₀ tension: 4.3–4.5σ (reduced from 5.4σ)
- Table comparing Paper 1 and Paper 2 results side-by-side

### 5.4 Parameter sensitivity
- η₀ sweep results showing ΔAIC as function of dephasing coupling
- The late domain contributes to the fit through two mechanisms: (a) background energy density correcting the angular diameter distance, and (b) dephasing G_eff modifying growth
- Without the late domain, the early domain alone worsens l_a (from 3.1σ to 4.0σ) — the two-channel architecture is not optional
- Reducing η₀ weakens the statistical preference but does not eliminate it (ΔAIC = −7.3 at η₀ = −0.03, −5.5 at η₀ = −0.01)

---

## Section 6: Discussion

### 6.1 Falsifiable predictions
- The IDT model makes a specific, quantitative prediction for the UVLF at z > 10 that is independent of the datasets used to constrain the model
- The prediction depends on the early domain amplitude f_early, which is determined by the CMB acoustic scale — not by galaxy observations
- As JWST survey areas grow (COSMOS-Web, PRIMER, JADES extensions), the predicted 20–50% enhancement will be directly testable

### 6.2 Ly-α as a future discriminant
- Current Ly-α constraints do not exclude the model, but future DESI measurements with reduced systematic uncertainties will provide a sharper test
- If DESI constrains the matter P₁D to better than ∼5% precision at z = 2–3, this would distinguish IDT from ΛCDM
- This constitutes a second independent falsification channel

### 6.3 Comparison with Early Dark Energy
- EDE models face a well-documented tension: raising H₀ generically worsens S₈ (Hill et al. 2020, Ivanov et al. 2020)
- IDT addresses this through the Friedmann-Poisson decoupling: the early domain modifies geometry while the late domain independently modifies growth
- EDE does not predict enhanced high-z galaxy formation in the same way, because the EDE field dilutes before matter-radiation equality affects P(k)
- A direct comparison of UVLF predictions (IDT vs EDE vs ΛCDM) would be a valuable future analysis

### 6.4 Limitations
- The compressed Planck likelihood captures the primary geometric constraints but does not include the full information content of the Planck power spectra; full plik/CamSpec analysis is deferred
- The SHMR used for UVLF predictions assumes constant SFE, which may not hold at z > 10
- The Ly-α comparison uses the matter P₁D rather than a full hydrodynamical flux P₁D forward model
- The MCMC uses a Metropolis-Hastings sampler with moderate chain lengths; nested sampling (e.g., PolyChord) would provide more robust evidence estimates

---

## Section 7: Conclusions

1. The IDT early domain (f_early ≈ 0.035, z_c = 2000), constrained by the CMB acoustic scale, predicts 20–50% more UV-bright galaxies at z = 10–15 relative to ΛCDM — a consequence of the model, not an additional fit
2. The Ly-α forest P₁D deviation (∼10% at z = 2) is within current systematic uncertainties of flux power spectrum measurements and does not constitute a tension with existing data
3. The Thomson optical depth remains within 0.1σ of the Planck constraint
4. With the updated DES Y3 S₈ prior, the model achieves ΔAIC = −8.3, confirming the Paper 1 result
5. Both channels of the two-domain architecture are required: removing the late domain worsens the acoustic scale fit
6. The model makes two falsifiable predictions for near-term observational programs: (a) enhanced UVLF at z > 10 testable by JWST, and (b) ∼10% Ly-α P₁D deviation testable by DESI

---

## Figures (planned)

1. **P(k) ratio IDT/ΛCDM at z = 10, 12, 15** — shows the broadband enhancement from the early domain
2. **UVLF comparison at z = 10 and z = 12** — IDT vs ΛCDM vs JWST data points (two panels)
3. **UVLF all redshifts** — single panel with z = 10, 12, 15 and JWST data
4. **Ly-α P₁D ratio at z = 2, 3, 4, 5** — four panels showing IDT/ΛCDM with 5% and systematic uncertainty bands
5. **Ly-α P₃D ratio** — complementary to P₁D, showing scale dependence
6. **η₀ constraint crossing** — two-axis plot showing S₈ tension and Ly-α deviation as function of η₀
7. **Updated MCMC comparison table** — Paper 1 vs Paper 2 results

---

## Tone guidelines

- **Do not claim** to "solve" the JWST massive galaxy problem — state that the model "predicts enhanced abundances qualitatively consistent with" the observations
- **Do not claim** Ly-α is "safe" — state that the deviations are "within current systematic uncertainties" and cite specific systematic budget numbers
- **Do not claim** the ΔAIC proves the model is correct — state it "indicates statistical preference" and note the limitations of the compressed likelihood
- **Do frame** every prediction as falsifiable: "this prediction will be tested by..."
- **Do acknowledge** every limitation before a reviewer can raise it
- **Do emphasize** that the high-z prediction is a consequence of the CMB fit, not a free parameter — this is the strongest argument against cherry-picking
