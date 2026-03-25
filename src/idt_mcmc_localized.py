"""
IDT Two Localized Domains MCMC
================================
Both domains are log-normal profiles in CLASS. No CPL proxy.

Early domain: shifts r_d → H₀
Late domain: suppresses growth → σ₈

Parameters (9 total, 6 beyond ΛCDM):
    Base:  H₀, ω_bh², ω_cdmh²
    Early: f_dom_1, z_c_1, σ_ln_1
    Late:  f_dom_2, z_c_2, σ_ln_2
"""

import sys, os, time
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'archive', 'class', 'python'))
from classy import Class

C_KM_S = 299792.458

R_OBS = 1.7502;     R_ERR = 0.0046
LA_OBS = 301.471;   LA_ERR = 0.090
OBH2_OBS = 0.02237; OBH2_ERR = 0.00015
H0_OBS = 73.04;     H0_ERR = 1.04

BAO = [
    (0.106, 3.047, 0.137),
    (0.15,  4.466, 0.168),
    (0.38, 10.23,  0.17),
    (0.51, 13.36,  0.21),
    (0.61, 15.45,  0.20),
]

# Weak lensing S₈ = σ₈ √(Ω_m/0.3)
# DES Y3: S₈ = 0.776 ± 0.017
# KiDS-1000: S₈ = 0.759 ± 0.024
# Combined approx: S₈ = 0.770 ± 0.014
S8_OBS = 0.770;     S8_ERR = 0.017

_LCDM_SN_REF = None

def get_lcdm_sn_ref():
    global _LCDM_SN_REF
    if _LCDM_SN_REF is None:
        r = run_class([67.36, 0.02237, 0.1200, 0, 2000, 0.15, 0, 1, 0.5])
        _LCDM_SN_REF = r['mu_sn']
    return _LCDM_SN_REF


def run_class(theta):
    """theta = [H0, obh2, ocdmh2, f1, zc1, sig1, f2, zc2, sig2]"""
    H0, obh2, ocdmh2, f1, zc1, sig1, f2, zc2, sig2 = theta

    cosmo = Class()
    p = {'output': 'tCl,pCl,lCl,mPk', 'l_max_scalars': 2500,
         'P_k_max_h/Mpc': 1.0,
         'H0': H0, 'omega_b': obh2, 'omega_cdm': ocdmh2,
         'T_cmb': 2.7255, 'N_ur': 2.0328, 'N_ncdm': 1, 'm_ncdm': 0.06}

    if f1 > 0:
        p['f_dom_idt_1'] = f1; p['z_c_idt_1'] = zc1; p['sigma_ln_idt_1'] = sig1
    if f2 > 0:
        p['f_dom_idt_2'] = f2; p['z_c_idt_2'] = zc2; p['sigma_ln_idt_2'] = sig2

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
        'sigma8': cosmo.sigma8(), 'rs_drag': cosmo.rs_drag(),
        'bao_pred': bao_pred, 'mu_sn': np.array(mu_sn),
    }
    cosmo.struct_cleanup(); cosmo.empty()
    return result


def log_likelihood(theta):
    obs = run_class(theta)
    if obs is None:
        return -np.inf

    chi2 = ((obs['R'] - R_OBS) / R_ERR) ** 2
    chi2 += ((obs['la'] - LA_OBS) / LA_ERR) ** 2
    chi2 += ((obs['obh2'] - OBH2_OBS) / OBH2_ERR) ** 2
    chi2 += ((obs['H0'] - H0_OBS) / H0_ERR) ** 2

    for i, (z_eff, DV_rd_obs, DV_rd_err) in enumerate(BAO):
        chi2 += ((obs['bao_pred'][i] - DV_rd_obs) / DV_rd_err) ** 2

    mu_ref = get_lcdm_sn_ref()
    dmu = obs['mu_sn'] - mu_ref
    dmu_shape = dmu - np.mean(dmu)
    chi2 += np.sum((dmu_shape / 0.03) ** 2)

    # Weak lensing S₈
    h = theta[0] / 100.0
    Omega_m = (theta[1] + theta[2]) / h**2
    S8 = obs['sigma8'] * np.sqrt(Omega_m / 0.3)
    chi2 += ((S8 - S8_OBS) / S8_ERR) ** 2

    return -0.5 * chi2


def log_prior(theta):
    H0, obh2, ocdmh2, f1, zc1, sig1, f2, zc2, sig2 = theta

    if not (60 < H0 < 80): return -np.inf
    if not (0.019 < obh2 < 0.025): return -np.inf
    if not (0.08 < ocdmh2 < 0.18): return -np.inf
    # Early domain
    if not (0.0 <= f1 < 0.20): return -np.inf
    if not (1000 < zc1 < 5000): return -np.inf
    if not (0.05 < sig1 < 0.50): return -np.inf
    # Late domain
    if not (0.0 <= f2 < 0.10): return -np.inf
    if not (0.3 < zc2 < 10.0): return -np.inf
    if not (0.1 < sig2 < 2.0): return -np.inf

    return 0.0


def log_probability(theta):
    lp = log_prior(theta)
    if not np.isfinite(lp): return -np.inf
    ll = log_likelihood(theta)
    if not np.isfinite(ll): return -np.inf
    return lp + ll


def run_mcmc(n_steps=800, burn_in=200):
    print("=" * 70)
    print("IDT TWO LOCALIZED DOMAINS MCMC")
    print("  Both domains: log-normal profiles in CLASS")
    print("  No CPL proxy")
    print("=" * 70)

    get_lcdm_sn_ref()

    theta_lcdm = [67.36, 0.02237, 0.1200, 0, 2000, 0.15, 0, 1, 0.5]
    ll_lcdm = log_likelihood(theta_lcdm)
    obs_lcdm = run_class(theta_lcdm)
    print(f'\n  ΛCDM: logL={ll_lcdm:.1f}  σ₈={obs_lcdm["sigma8"]:.4f}')

    # Start from the scan basin: E(0.08,2000,0.18)+L(0.05,1.0,0.5)
    # At fixed cosmo: H₀i=68.1, σ₈=0.797, R=5.1σ, l_a=2.4σ
    # The MCMC should adjust H₀/Ω_m to fix R while keeping the domains active
    theta_0 = np.array([
        69.0,     # H0 — push higher to compensate R
        0.02240,  # obh2
        0.1250,   # ocdmh2 — higher to fix R
        0.08,     # f1 (early)
        2000,     # zc1
        0.18,     # sig1
        0.05,     # f2 (late) — strong σ₈ suppression
        1.0,      # zc2
        0.5,      # sig2
    ])

    lp_0 = log_probability(theta_0)
    obs_0 = run_class(theta_0)
    if obs_0:
        print(f'  Start: logL={lp_0:.1f}  H₀={obs_0["H0"]:.1f}  '
              f'σ₈={obs_0["sigma8"]:.4f}  r_d={obs_0["rs_drag"]:.1f}')

    proposal_sigma = np.array([
        0.3,     # H0
        0.00008, # obh2
        0.0015,  # ocdmh2
        0.006,   # f1
        60,      # zc1
        0.012,   # sig1
        0.004,   # f2
        0.12,    # zc2
        0.06,    # sig2
    ])

    labels = ['H₀', 'ω_bh²', 'ω_cdmh²', 'f₁', 'z_c₁', 'σ_ln₁',
              'f₂', 'z_c₂', 'σ_ln₂']

    chain = np.zeros((n_steps, 9))
    log_probs = np.zeros(n_steps)
    accepted = 0
    theta_current = theta_0.copy()
    lp_current = lp_0

    print(f'\n  Running {n_steps} steps...')
    t0 = time.time()

    for i in range(n_steps):
        theta_proposal = theta_current + proposal_sigma * np.random.randn(9)
        lp_proposal = log_probability(theta_proposal)
        if np.log(np.random.rand()) < lp_proposal - lp_current:
            theta_current = theta_proposal
            lp_current = lp_proposal
            accepted += 1
        chain[i] = theta_current
        log_probs[i] = lp_current

        if (i + 1) % 100 == 0:
            acc = accepted / (i + 1)
            eta = (n_steps - i - 1) * (time.time() - t0) / (i + 1)
            print(f'    Step {i+1}/{n_steps}  logL={lp_current:.1f}  '
                  f'H₀={theta_current[0]:.1f}  '
                  f'f₁={theta_current[3]:.3f}  f₂={theta_current[6]:.3f}  '
                  f'acc={acc:.0%}  ETA={eta:.0f}s')

    elapsed = time.time() - t0
    print(f'\n  Done in {elapsed:.0f}s ({elapsed/n_steps:.1f}s/step, '
          f'acc={accepted/n_steps:.0%})')

    post = chain[burn_in:]
    post_lp = log_probs[burn_in:]
    best_idx = np.argmax(post_lp)
    best = post[best_idx]
    best_lp = post_lp[best_idx]
    obs_best = run_class(best)

    print(f'\n  {"="*60}')
    print(f'  BEST FIT (logL={best_lp:.1f})')
    print(f'  {"="*60}')
    for j, (label, val) in enumerate(zip(labels, best)):
        lo = np.percentile(post[:, j], 16)
        hi = np.percentile(post[:, j], 84)
        print(f'    {label:>8} = {val:.5f}  ({lo:.5f} — {hi:.5f})')

    if obs_best:
        R_sig = abs(obs_best['R'] - R_OBS) / R_ERR
        la_sig = abs(obs_best['la'] - LA_OBS) / LA_ERR
        print(f'\n    σ₈ = {obs_best["sigma8"]:.4f}')
        print(f'    r_d = {obs_best["rs_drag"]:.2f} Mpc')
        print(f'    R = {obs_best["R"]:.4f} ({R_sig:.1f}σ)')
        print(f'    l_a = {obs_best["la"]:.3f} ({la_sig:.1f}σ)')

    n_extra = 6
    delta_chi2 = -2 * (best_lp - ll_lcdm)
    delta_aic = delta_chi2 + 2 * n_extra

    print(f'\n    Δχ² vs ΛCDM = {delta_chi2:.1f}')
    print(f'    ΔAIC = {delta_aic:.1f} ({n_extra} extra params)')

    verdict = 'VERY STRONGLY PREFERRED' if delta_aic < -10 else \
              'PREFERRED' if delta_aic < -2 else \
              'Comparable' if delta_aic < 2 else 'ΛCDM preferred'
    print(f'    → {verdict} over ΛCDM')

    # Key comparison
    print(f'\n  {"="*60}')
    print(f'  COMPARISON')
    print(f'  {"="*60}')
    print(f'    ΛCDM:             H₀=67.4  σ₈=0.811')
    print(f'    CPL single:       H₀=69.9  σ₈=0.854  ΔAIC=-25.6')
    print(f'    N_ur+CPL proxy:   H₀=71.7  σ₈=0.883  ΔAIC=-31.9')
    if obs_best:
        print(f'    Two localized:    H₀={obs_best["H0"]:.1f}  '
              f'σ₈={obs_best["sigma8"]:.3f}  ΔAIC={delta_aic:.1f}')

    return chain, log_probs, best


if __name__ == "__main__":
    chain, log_probs, best = run_mcmc(n_steps=1200, burn_in=300)
