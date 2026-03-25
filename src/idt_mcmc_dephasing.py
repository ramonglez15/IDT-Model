"""
IDT Dephasing MCMC — The Full Picture
=======================================
Two localized domains with dephasing-driven G_eff.

Uses CLASS for: CMB (R, l_a), BAO distances, background
Uses growth calculator for: σ₈ with G_eff modification

Parameters (5 total, 3 beyond ΛCDM):
    Base:  H₀, ω_bh², ω_cdmh²  (floating)
    IDT:   f_early, f_late       (floating, epochs/widths fixed)
    Fixed: z_c_early=2000, σ_early=0.18, z_c_late=1.0, σ_late=0.5
           η₀ = -0.05 (dephasing coupling, fixed from derivation)
"""

import sys, os, time
import numpy as np
from scipy.integrate import odeint, quad
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'archive', 'class', 'python'))
from classy import Class

C_KM_S = 299792.458

# Fixed domain structure
ZC_EARLY = 2000.0;  SIG_EARLY = 0.18
ZC_LATE = 1.0;      SIG_LATE = 0.5
ETA0 = -0.05  # dephasing coupling

# Observational constraints
R_OBS = 1.7502;     R_ERR = 0.0046
LA_OBS = 301.471;   LA_ERR = 0.090
OBH2_OBS = 0.02237; OBH2_ERR = 0.00015
H0_OBS = 73.04;     H0_ERR = 1.04
S8_OBS = 0.770;     S8_ERR = 0.017

BAO = [
    (0.106, 3.047, 0.137),
    (0.15,  4.466, 0.168),
    (0.38, 10.23,  0.17),
    (0.51, 13.36,  0.21),
    (0.61, 15.45,  0.20),
]

_LCDM_REF = None


def compute_sigma8_with_geff(H0, obh2, ocdmh2, f_early, f_late, sigma8_class):
    """
    Correct CLASS σ₈ for the dephasing G_eff effect.

    CLASS computes σ₈ with standard growth (no G_eff).
    We compute the RATIO of growth factors with/without G_eff
    and apply it as a correction.
    """
    h = H0 / 100.0
    Om0 = (obh2 + ocdmh2) / h**2
    Or0 = 9.1e-5
    OL0 = 1 - Om0 - Or0

    def E2(a, with_domains=True):
        z = 1.0/a - 1.0
        E2_val = Om0/a**3 + Or0/a**4 + OL0
        if with_domains:
            for f_dom, z_c, sigma_ln in [(f_early, ZC_EARLY, SIG_EARLY),
                                          (f_late, ZC_LATE, SIG_LATE)]:
                if f_dom > 0:
                    ln_ratio = np.log((1+z)/(1+z_c))
                    rho_shape = np.exp(-0.5 * ln_ratio**2 / sigma_ln**2)
                    E2_zc = Om0*(1+z_c)**3 + Or0*(1+z_c)**4 + OL0
                    Omega_peak = f_dom / (1-f_dom) * E2_zc
                    E2_val += Omega_peak * rho_shape
        return E2_val

    def Gamma(a):
        if f_late <= 0: return 0
        z = 1.0/a - 1.0
        ln_ratio = np.log((1+z)/(1+ZC_LATE))
        sigma2 = SIG_LATE**2
        rho_shape = np.exp(-0.5 * ln_ratio**2 / sigma2)
        if rho_shape < 1e-12: return 0
        return (ln_ratio / sigma2) * rho_shape

    def growth_ode(y, lna, use_geff):
        D, dD = y
        a = np.exp(lna)
        E2_val = E2(a)
        if E2_val <= 0: return [0, 0]
        da = 1e-5
        E2_p = E2(a * np.exp(da))
        E2_m = E2(a * np.exp(-da))
        dlnH = (np.log(max(E2_p, 1e-30)) - np.log(max(E2_m, 1e-30))) / (4*da)
        Om_a = Om0 / a**3 / E2_val
        G_mod = 1.0 + (ETA0 * Gamma(a) if use_geff else 0)
        return [dD, -(2 + dlnH)*dD + 1.5*Om_a*G_mod*D]

    lna = np.linspace(np.log(1e-3), 0, 2000)
    y0 = [1e-3, 1.0]

    # Growth WITH G_eff (dephasing)
    sol_geff = odeint(growth_ode, y0, lna, args=(True,))
    D_geff = sol_geff[-1, 0]

    # Growth WITHOUT G_eff (standard, what CLASS computes)
    sol_std = odeint(growth_ode, y0, lna, args=(False,))
    D_std = sol_std[-1, 0]

    # Correction ratio
    ratio = D_geff / D_std if D_std > 0 else 1.0

    # Apply correction to CLASS σ₈
    return sigma8_class * ratio


def get_lcdm_ref():
    global _LCDM_REF
    if _LCDM_REF is None:
        _LCDM_REF = run_model([67.36, 0.02237, 0.1200, 0, 0])
    return _LCDM_REF


def run_model(theta):
    """theta = [H0, obh2, ocdmh2, f_early, f_late]"""
    H0, obh2, ocdmh2, f_early, f_late = theta

    cosmo = Class()
    p = {'output': 'tCl,pCl,lCl,mPk', 'l_max_scalars': 2500,
         'P_k_max_h/Mpc': 1.0,
         'H0': H0, 'omega_b': obh2, 'omega_cdm': ocdmh2,
         'T_cmb': 2.7255, 'N_ur': 2.0328, 'N_ncdm': 1, 'm_ncdm': 0.06}

    if f_early > 0:
        p['f_dom_idt_1'] = f_early
        p['z_c_idt_1'] = ZC_EARLY
        p['sigma_ln_idt_1'] = SIG_EARLY
    if f_late > 0:
        p['f_dom_idt_2'] = f_late
        p['z_c_idt_2'] = ZC_LATE
        p['sigma_ln_idt_2'] = SIG_LATE

    cosmo.set(p)
    try:
        cosmo.compute()
    except Exception:
        cosmo.struct_cleanup(); cosmo.empty()
        return None

    h = H0 / 100.0
    Omega_m = (obh2 + ocdmh2) / h**2
    z_star = 1089.92
    da = cosmo.angular_distance(z_star)
    dc = da * (1 + z_star)
    bg = cosmo.get_background()
    rs_star = np.interp(z_star, bg['z'][::-1], bg['comov.snd.hrz.'][::-1])

    R = np.sqrt(Omega_m) * H0 / C_KM_S * dc
    la = np.pi * dc / rs_star

    # CLASS σ₈ (standard growth)
    sigma8_class = cosmo.sigma8()

    # Corrected σ₈ with dephasing G_eff
    sigma8_idt = compute_sigma8_with_geff(
        H0, obh2, ocdmh2, f_early, f_late, sigma8_class)

    S8 = sigma8_idt * np.sqrt(Omega_m / 0.3)

    bao_pred = []
    for z_eff, _, _ in BAO:
        da_z = cosmo.angular_distance(z_eff)
        dc_z = da_z * (1 + z_eff)
        Hz = cosmo.Hubble(z_eff) * C_KM_S
        DV = (dc_z**2 * C_KM_S * z_eff / Hz) ** (1.0/3.0)
        bao_pred.append(DV / cosmo.rs_drag())

    z_sn = [0.1, 0.3, 0.5, 0.7, 1.0, 1.5]
    mu_sn = []
    for z in z_sn:
        da_z = cosmo.angular_distance(z)
        dl = da_z * (1 + z)**2
        mu_sn.append(5.0 * np.log10(dl) + 25.0 if dl > 0 else 999)

    result = {
        'H0': H0, 'R': R, 'la': la, 'obh2': obh2,
        'sigma8': sigma8_idt, 'sigma8_class': sigma8_class,
        'S8': S8, 'Omega_m': Omega_m,
        'rs_drag': cosmo.rs_drag(),
        'bao_pred': bao_pred, 'mu_sn': np.array(mu_sn),
    }
    cosmo.struct_cleanup(); cosmo.empty()
    return result


def log_likelihood(theta):
    obs = run_model(theta)
    if obs is None:
        return -np.inf, None

    chi2_R = ((obs['R'] - R_OBS) / R_ERR) ** 2
    chi2_la = ((obs['la'] - LA_OBS) / LA_ERR) ** 2
    chi2_obh2 = ((obs['obh2'] - OBH2_OBS) / OBH2_ERR) ** 2
    chi2_H0 = ((obs['H0'] - H0_OBS) / H0_ERR) ** 2
    chi2_S8 = ((obs['S8'] - S8_OBS) / S8_ERR) ** 2

    chi2_bao = 0
    for i, (z_eff, DV_rd_obs, DV_rd_err) in enumerate(BAO):
        chi2_bao += ((obs['bao_pred'][i] - DV_rd_obs) / DV_rd_err) ** 2

    ref = get_lcdm_ref()
    dmu = obs['mu_sn'] - ref['mu_sn']
    dmu_shape = dmu - np.mean(dmu)
    chi2_sn = np.sum((dmu_shape / 0.03) ** 2)

    chi2 = chi2_R + chi2_la + chi2_obh2 + chi2_H0 + chi2_S8 + chi2_bao + chi2_sn

    components = {'R': chi2_R, 'la': chi2_la, 'obh2': chi2_obh2,
                  'H0': chi2_H0, 'S8': chi2_S8, 'BAO': chi2_bao, 'SN': chi2_sn}

    return -0.5 * chi2, components


def log_prior(theta):
    H0, obh2, ocdmh2, f_early, f_late = theta
    if not (60 < H0 < 80): return -np.inf
    if not (0.019 < obh2 < 0.025): return -np.inf
    if not (0.08 < ocdmh2 < 0.18): return -np.inf
    if not (0.0 <= f_early < 0.20): return -np.inf
    if not (0.0 <= f_late < 0.10): return -np.inf
    return 0.0


def log_probability(theta):
    lp = log_prior(theta)
    if not np.isfinite(lp): return -np.inf
    ll, _ = log_likelihood(theta)
    if not np.isfinite(ll): return -np.inf
    return lp + ll


def run_mcmc(n_steps=1500, burn_in=400):
    print("=" * 70)
    print("IDT DEPHASING MCMC — FULL PICTURE")
    print(f"  Early domain: z_c={ZC_EARLY}, σ={SIG_EARLY} (fixed)")
    print(f"  Late domain:  z_c={ZC_LATE}, σ={SIG_LATE} (fixed)")
    print(f"  Dephasing:    η₀ = {ETA0} (fixed from derivation)")
    print(f"  Floating: H₀, ω_bh², ω_cdmh², f_early, f_late")
    print(f"  Extra params beyond ΛCDM: 2")
    print("=" * 70)

    # ΛCDM reference
    ref = get_lcdm_ref()
    ll_lcdm, comp_lcdm = log_likelihood([67.36, 0.02237, 0.1200, 0, 0])
    print(f'\n  ΛCDM: logL={ll_lcdm:.1f}  H₀={ref["H0"]:.1f}  '
          f'σ₈={ref["sigma8"]:.4f}  S₈={ref["S8"]:.4f}')
    print(f'    χ² breakdown: R={comp_lcdm["R"]:.1f} la={comp_lcdm["la"]:.1f} '
          f'obh2={comp_lcdm["obh2"]:.1f} H0={comp_lcdm["H0"]:.1f} '
          f'S8={comp_lcdm["S8"]:.1f} BAO={comp_lcdm["BAO"]:.1f}')

    # Start near viable basin
    theta_0 = np.array([68.5, 0.02240, 0.1220, 0.06, 0.03])

    lp_0 = log_probability(theta_0)
    obs_0 = run_model(theta_0)
    if obs_0:
        print(f'\n  Start: logL={lp_0:.1f}  H₀={obs_0["H0"]:.1f}  '
              f'σ₈={obs_0["sigma8"]:.4f}  S₈={obs_0["S8"]:.4f}  '
              f'σ₈_class={obs_0["sigma8_class"]:.4f}')

    proposal_sigma = np.array([0.25, 0.00006, 0.001, 0.005, 0.003])
    labels = ['H₀', 'ω_bh²', 'ω_cdmh²', 'f_early', 'f_late']

    chain = np.zeros((n_steps, 5))
    log_probs = np.zeros(n_steps)
    accepted = 0
    theta_current = theta_0.copy()
    lp_current = lp_0

    print(f'\n  Running {n_steps} steps...')
    t0 = time.time()

    for i in range(n_steps):
        theta_proposal = theta_current + proposal_sigma * np.random.randn(5)
        lp_proposal = log_probability(theta_proposal)
        if np.log(np.random.rand()) < lp_proposal - lp_current:
            theta_current = theta_proposal
            lp_current = lp_proposal
            accepted += 1
        chain[i] = theta_current
        log_probs[i] = lp_current

        if (i + 1) % 200 == 0:
            acc = accepted / (i + 1)
            eta = (n_steps - i - 1) * (time.time() - t0) / (i + 1)
            print(f'    Step {i+1}/{n_steps}  logL={lp_current:.1f}  '
                  f'H₀={theta_current[0]:.2f}  '
                  f'f_e={theta_current[3]:.4f}  f_l={theta_current[4]:.4f}  '
                  f'acc={acc:.0%}  ETA={eta:.0f}s')

    elapsed = time.time() - t0
    print(f'\n  Done in {elapsed:.0f}s ({elapsed/n_steps:.2f}s/step, '
          f'acc={accepted/n_steps:.0%})')

    # Post-processing
    post = chain[burn_in:]
    post_lp = log_probs[burn_in:]
    best_idx = np.argmax(post_lp)
    best = post[best_idx]
    best_lp = post_lp[best_idx]
    obs_best = run_model(best)
    ll_best, comp_best = log_likelihood(best)

    print(f'\n  {"="*60}')
    print(f'  BEST FIT (logL={best_lp:.1f})')
    print(f'  {"="*60}')
    for j, (label, val) in enumerate(zip(labels, best)):
        lo = np.percentile(post[:, j], 16)
        med = np.median(post[:, j])
        hi = np.percentile(post[:, j], 84)
        print(f'    {label:>10} = {med:.5f}  ({lo:.5f} — {hi:.5f})  [best: {val:.5f}]')

    if obs_best:
        R_sig = abs(obs_best['R'] - R_OBS) / R_ERR
        la_sig = abs(obs_best['la'] - LA_OBS) / LA_ERR
        S8_sig = abs(obs_best['S8'] - S8_OBS) / S8_ERR
        H0_sig = abs(obs_best['H0'] - H0_OBS) / H0_ERR

        print(f'\n    Derived:')
        print(f'      σ₈ (CLASS)    = {obs_best["sigma8_class"]:.4f}')
        print(f'      σ₈ (dephased) = {obs_best["sigma8"]:.4f}')
        print(f'      S₈            = {obs_best["S8"]:.4f} ({S8_sig:.1f}σ from lensing)')
        print(f'      Ω_m           = {obs_best["Omega_m"]:.4f}')
        print(f'      r_d           = {obs_best["rs_drag"]:.2f} Mpc')
        print(f'      R             = {obs_best["R"]:.4f} ({R_sig:.1f}σ)')
        print(f'      l_a           = {obs_best["la"]:.3f} ({la_sig:.1f}σ)')
        print(f'      H₀ tension    = {H0_sig:.1f}σ')

    print(f'\n    χ² breakdown:')
    for k, v in comp_best.items():
        print(f'      {k:>5}: {v:.2f}')

    n_extra = 2
    delta_chi2 = -2 * (best_lp - ll_lcdm)
    delta_aic = delta_chi2 + 2 * n_extra

    print(f'\n    Δχ² vs ΛCDM = {delta_chi2:.1f}')
    print(f'    ΔAIC = {delta_aic:.1f} ({n_extra} extra params)')

    verdict = 'VERY STRONGLY PREFERRED' if delta_aic < -10 else \
              'STRONGLY PREFERRED' if delta_aic < -6 else \
              'PREFERRED' if delta_aic < -2 else \
              'Comparable' if delta_aic < 2 else 'ΛCDM preferred'
    print(f'    → {verdict} over ΛCDM')

    print(f'\n  {"="*60}')
    print(f'  FINAL COMPARISON')
    print(f'  {"="*60}')
    print(f'    {"":>25} {"H₀":>6} {"σ₈":>7} {"S₈":>7} {"R(σ)":>5} {"l_a(σ)":>6} {"ΔAIC":>6}')
    print(f'    {"ΛCDM":>25} {67.36:>6.1f} {ref["sigma8"]:>7.4f} '
          f'{ref["S8"]:>7.4f} {"0.9":>5} {"3.1":>6} {"0":>6}')
    if obs_best:
        print(f'    {"IDT dephasing":>25} {obs_best["H0"]:>6.1f} '
              f'{obs_best["sigma8"]:>7.4f} {obs_best["S8"]:>7.4f} '
              f'{R_sig:>5.1f} {la_sig:>6.1f} {delta_aic:>6.1f}')

    return chain, log_probs, best


if __name__ == "__main__":
    chain, log_probs, best = run_mcmc(n_steps=1500, burn_in=400)
