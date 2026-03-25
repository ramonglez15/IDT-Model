"""
IDT Self-Consistent MCMC — G_eff in CLASS
============================================
No hybrid approximation. CLASS computes σ₈ directly with dephasing.
This is the definitive test.
"""

import sys, os, time
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'archive', 'class', 'python'))
from classy import Class

C_KM_S = 299792.458

ZC_EARLY = 2000.0;  SIG_EARLY = 0.18
ZC_LATE = 1.0;      SIG_LATE = 0.5
ETA0 = -0.05

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

def get_lcdm_ref():
    global _LCDM_REF
    if _LCDM_REF is None:
        _LCDM_REF = run_model([67.36, 0.02237, 0.1200, 0, 0])
    return _LCDM_REF


def run_model(theta):
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
        p['eta0_idt'] = ETA0
        p['idt_dephasing_domain'] = 2
    cosmo.set(p)
    try:
        cosmo.compute()
    except Exception:
        cosmo.struct_cleanup(); cosmo.empty()
        return None
    h = H0 / 100.0
    Omega_m = (obh2 + ocdmh2) / h**2
    da = cosmo.angular_distance(1089.92)
    dc = da * (1 + 1089.92)
    bg = cosmo.get_background()
    rs_star = np.interp(1089.92, bg['z'][::-1], bg['comov.snd.hrz.'][::-1])
    R = np.sqrt(Omega_m) * H0 / C_KM_S * dc
    la = np.pi * dc / rs_star
    sigma8 = cosmo.sigma8()
    S8 = sigma8 * np.sqrt(Omega_m / 0.3)
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
        'sigma8': sigma8, 'S8': S8, 'Omega_m': Omega_m,
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
    chi2_bao = sum(((obs['bao_pred'][i] - d) / e)**2
                   for i, (z, d, e) in enumerate(BAO))
    ref = get_lcdm_ref()
    dmu = obs['mu_sn'] - ref['mu_sn']
    dmu_shape = dmu - np.mean(dmu)
    chi2_sn = np.sum((dmu_shape / 0.03) ** 2)
    chi2 = chi2_R + chi2_la + chi2_obh2 + chi2_H0 + chi2_S8 + chi2_bao + chi2_sn
    comp = {'R': chi2_R, 'la': chi2_la, 'obh2': chi2_obh2,
            'H0': chi2_H0, 'S8': chi2_S8, 'BAO': chi2_bao, 'SN': chi2_sn}
    return -0.5 * chi2, comp


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


if __name__ == "__main__":
    print("=" * 70)
    print("IDT SELF-CONSISTENT MCMC — G_eff IN CLASS")
    print(f"  η₀ = {ETA0} (in CLASS perturbations.c)")
    print(f"  No hybrid approximation — fully self-consistent")
    print("=" * 70)

    ref = get_lcdm_ref()
    ll_lcdm, comp_lcdm = log_likelihood([67.36, 0.02237, 0.1200, 0, 0])
    print(f'\n  ΛCDM: logL={ll_lcdm:.1f}  σ₈={ref["sigma8"]:.4f}  S₈={ref["S8"]:.4f}')

    theta_0 = np.array([68.5, 0.02240, 0.1220, 0.05, 0.03])
    lp_0 = log_probability(theta_0)
    obs_0 = run_model(theta_0)
    if obs_0:
        print(f'  Start: logL={lp_0:.1f}  σ₈={obs_0["sigma8"]:.4f}  S₈={obs_0["S8"]:.4f}')

    proposal_sigma = np.array([0.25, 0.00006, 0.001, 0.005, 0.003])
    labels = ['H₀', 'ω_bh²', 'ω_cdmh²', 'f_early', 'f_late']

    n_steps = 1200; burn_in = 300
    chain = np.zeros((n_steps, 5))
    log_probs = np.zeros(n_steps)
    accepted = 0
    theta = theta_0.copy(); lp = lp_0

    print(f'\n  Running {n_steps} steps...')
    t0 = time.time()

    for i in range(n_steps):
        prop = theta + proposal_sigma * np.random.randn(5)
        lp_prop = log_probability(prop)
        if np.log(np.random.rand()) < lp_prop - lp:
            theta = prop; lp = lp_prop; accepted += 1
        chain[i] = theta; log_probs[i] = lp
        if (i + 1) % 200 == 0:
            acc = accepted / (i + 1)
            eta = (n_steps - i - 1) * (time.time() - t0) / (i + 1)
            print(f'    Step {i+1}/{n_steps}  logL={lp:.1f}  '
                  f'H₀={theta[0]:.2f}  f_e={theta[3]:.4f}  f_l={theta[4]:.4f}  '
                  f'acc={acc:.0%}  ETA={eta:.0f}s')

    elapsed = time.time() - t0
    print(f'\n  Done in {elapsed:.0f}s ({elapsed/n_steps:.2f}s/step, acc={accepted/n_steps:.0%})')

    post = chain[burn_in:]; post_lp = log_probs[burn_in:]
    best_idx = np.argmax(post_lp)
    best = post[best_idx]; best_lp = post_lp[best_idx]
    obs_best = run_model(best)
    ll_best, comp_best = log_likelihood(best)

    print(f'\n  {"="*60}')
    print(f'  SELF-CONSISTENT BEST FIT (logL={best_lp:.1f})')
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

        print(f'\n    σ₈ = {obs_best["sigma8"]:.4f}  (self-consistent, no correction)')
        print(f'    S₈ = {obs_best["S8"]:.4f} ({S8_sig:.1f}σ)')
        print(f'    R  = {obs_best["R"]:.4f} ({R_sig:.1f}σ)')
        print(f'    l_a = {obs_best["la"]:.3f} ({la_sig:.1f}σ)')
        print(f'    H₀ tension = {H0_sig:.1f}σ')

    n_extra = 2
    delta_chi2 = -2 * (best_lp - ll_lcdm)
    delta_aic = delta_chi2 + 2 * n_extra

    print(f'\n    Δχ² = {delta_chi2:.1f}')
    print(f'    ΔAIC = {delta_aic:.1f} ({n_extra} extra params)')

    verdict = 'VERY STRONGLY PREFERRED' if delta_aic < -10 else \
              'STRONGLY PREFERRED' if delta_aic < -6 else \
              'PREFERRED' if delta_aic < -2 else \
              'Comparable' if delta_aic < 2 else 'ΛCDM preferred'
    print(f'    → {verdict} over ΛCDM')

    print(f'\n  {"="*60}')
    print(f'  COMPARISON: HYBRID vs SELF-CONSISTENT')
    print(f'  {"="*60}')
    print(f'    {"":>20} {"H₀":>6} {"σ₈":>7} {"S₈":>7} {"ΔAIC":>6}')
    print(f'    {"ΛCDM":>20} {67.36:>6.1f} {0.811:>7.4f} {ref["S8"]:>7.4f} {"0":>6}')
    print(f'    {"Hybrid (prev)":>20} {"68.4":>6} {"0.809":>7} {"0.822":>7} {"-12.5":>6}')
    if obs_best:
        print(f'    {"Self-consistent":>20} {obs_best["H0"]:>6.1f} '
              f'{obs_best["sigma8"]:>7.4f} {obs_best["S8"]:>7.4f} {delta_aic:>6.1f}')
