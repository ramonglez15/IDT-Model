"""
IDT Multi-Domain MCMC
=======================
Two domains at different epochs — the core IDT prediction.

Domain 1 (early): Extra radiation-like component (ΔN_ur)
    - Active pre-recombination (z > 1000)
    - Shrinks sound horizon r_d → raises inferred H₀
    - Suppresses σ₈ via altered matter-radiation equality

Domain 2 (late): Dark energy fluid (w₀, wₐ)
    - Active post-recombination (z < few)
    - Modifies distance-redshift relation
    - Adjusts CMB shift parameters (R, l_a)

Parameters:
    Base:  H₀, ω_bh², ω_cdmh²
    Early: ΔN_ur (extra radiation = early domain strength)
    Late:  w₀, wₐ, Ω_fld
    Total: 7 params (4 beyond ΛCDM)
"""

import numpy as np
import matplotlib.pyplot as plt
import sys, os, time

sys.path.insert(0, os.path.join(os.path.dirname(__file__),
                                '..', 'archive', 'class', 'python'))
from classy import Class

C_KM_S = 299792.458

# Observational constraints
R_OBS = 1.7502;       R_ERR = 0.0046
LA_OBS = 301.471;     LA_ERR = 0.090
OBH2_OBS = 0.02237;   OBH2_ERR = 0.00015
H0_OBS = 73.04;       H0_ERR = 1.04

BAO = [
    (0.106, 3.047, 0.137),
    (0.15,  4.466, 0.168),
    (0.38, 10.23,  0.17),
    (0.51, 13.36,  0.21),
    (0.61, 15.45,  0.20),
]

_LCDM_SN_REF = None

def get_lcdm_sn_ref():
    global _LCDM_SN_REF
    if _LCDM_SN_REF is None:
        r = run_class_multi(67.36, 0.02237, 0.1200, 0.0, -1.0, 0.0, 0.0)
        _LCDM_SN_REF = r['mu_sn']
    return _LCDM_SN_REF


def run_class_multi(H0, obh2, ocdmh2, delta_nur, w0_fld, wa_fld, Omega_fld):
    """
    Run CLASS with two domain components:
    - Early domain: ΔN_ur extra radiation
    - Late domain: fld with w₀, wₐ
    """
    cosmo = Class()

    N_ur_base = 2.0328  # standard (3.044 - 1 massive)
    N_ur_total = N_ur_base + delta_nur

    params = {
        'output': 'tCl,pCl,lCl,mPk',
        'lensing': 'yes',
        'l_max_scalars': 2500,
        'P_k_max_h/Mpc': 1.0,
        'H0': H0,
        'omega_b': obh2,
        'omega_cdm': ocdmh2,
        'T_cmb': 2.7255,
        'N_ur': N_ur_total,
        'N_ncdm': 1,
        'm_ncdm': 0.06,
    }

    if Omega_fld > 0.001:
        params['Omega_fld'] = Omega_fld
        params['w0_fld'] = w0_fld
        params['wa_fld'] = wa_fld
        params['cs2_fld'] = 1.0

    cosmo.set(params)
    try:
        cosmo.compute()
    except Exception:
        cosmo.struct_cleanup()
        cosmo.empty()
        return None

    h = H0 / 100.0
    Omega_m = (obh2 + ocdmh2) / h**2

    z_star = 1089.92
    da_star = cosmo.angular_distance(z_star)
    dc_star = da_star * (1 + z_star)

    bg = cosmo.get_background()
    rs_star = np.interp(z_star, bg['z'][::-1], bg['comov.snd.hrz.'][::-1])

    R = np.sqrt(Omega_m) * H0 / C_KM_S * dc_star
    la = np.pi * dc_star / rs_star

    bao_pred = []
    for z_eff, _, _ in BAO:
        da = cosmo.angular_distance(z_eff)
        dc = da * (1 + z_eff)
        Hz = cosmo.Hubble(z_eff) * C_KM_S
        DV = (dc**2 * C_KM_S * z_eff / Hz) ** (1.0/3.0)
        bao_pred.append(DV / cosmo.rs_drag())

    z_sn = [0.1, 0.3, 0.5, 0.7, 1.0, 1.5]
    mu_sn = []
    for z in z_sn:
        da = cosmo.angular_distance(z)
        dl = da * (1 + z)**2
        mu_sn.append(5.0 * np.log10(dl) + 25.0 if dl > 0 else 999)

    result = {
        'H0': H0, 'R': R, 'la': la, 'obh2': obh2,
        'sigma8': cosmo.sigma8(), 'rs_drag': cosmo.rs_drag(),
        'bao_pred': bao_pred, 'mu_sn': np.array(mu_sn),
        'delta_nur': delta_nur,
    }

    cosmo.struct_cleanup()
    cosmo.empty()
    return result


def log_likelihood(theta):
    H0, obh2, ocdmh2, delta_nur, w0_fld, wa_fld, Omega_fld = theta

    obs = run_class_multi(H0, obh2, ocdmh2, delta_nur, w0_fld, wa_fld, Omega_fld)
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

    return -0.5 * chi2


def log_prior(theta):
    H0, obh2, ocdmh2, delta_nur, w0_fld, wa_fld, Omega_fld = theta

    if not (60 < H0 < 80): return -np.inf
    if not (0.019 < obh2 < 0.025): return -np.inf
    if not (0.08 < ocdmh2 < 0.20): return -np.inf
    if not (0.0 <= delta_nur < 2.0): return -np.inf
    if not (-1.5 < w0_fld < -0.5): return -np.inf
    if not (-0.8 < wa_fld < 0.8): return -np.inf
    if not (0.4 < Omega_fld < 0.85): return -np.inf

    h = H0 / 100
    Omega_m = (obh2 + ocdmh2) / h**2
    Omega_total = Omega_m + Omega_fld + 9.1e-5
    if not (0.90 < Omega_total < 1.10): return -np.inf

    return 0.0


def log_probability(theta):
    lp = log_prior(theta)
    if not np.isfinite(lp): return -np.inf
    ll = log_likelihood(theta)
    if not np.isfinite(ll): return -np.inf
    return lp + ll


def run_mcmc(n_steps=600, burn_in=150):
    print("=" * 70)
    print("IDT MULTI-DOMAIN MCMC")
    print("  Early domain: ΔN_ur (extra radiation)")
    print("  Late domain:  w₀, wₐ, Ω_fld (dark energy fluid)")
    print("=" * 70)

    get_lcdm_sn_ref()

    # ΛCDM reference
    theta_lcdm = np.array([67.36, 0.02237, 0.1200, 0.0, -1.0, 0.0, 0.0])
    ll_lcdm = log_likelihood(theta_lcdm)
    print(f'\n  ΛCDM: logL = {ll_lcdm:.1f}')

    # Starting point: combine early (ΔN_ur~0.4) + late (w₀=-0.92)
    theta_0 = np.array([
        70.0,    # H0
        0.02240, # obh2
        0.1200,  # ocdmh2
        0.4,     # delta_nur (early domain)
        -0.92,   # w0_fld (late domain — old OIDM value)
        -0.14,   # wa_fld
        0.69,    # Omega_fld
    ])

    lp_0 = log_probability(theta_0)
    obs_0 = run_class_multi(*theta_0)
    if obs_0:
        print(f'  Start: logL={lp_0:.1f}, H₀={obs_0["H0"]:.1f}, '
              f'σ₈={obs_0["sigma8"]:.4f}, r_d={obs_0["rs_drag"]:.1f}')

    proposal_sigma = np.array([
        0.5,     # H0
        0.0001,  # obh2
        0.002,   # ocdmh2
        0.05,    # delta_nur
        0.03,    # w0
        0.03,    # wa
        0.01,    # Omega_fld
    ])

    labels = ['H₀', 'ω_bh²', 'ω_cdmh²', 'ΔN_ur', 'w₀', 'wₐ', 'Ω_fld']

    chain = np.zeros((n_steps, 7))
    log_probs = np.zeros(n_steps)
    accepted = 0
    theta_current = theta_0.copy()
    lp_current = lp_0

    print(f'\n  Running {n_steps} steps...')
    t0 = time.time()

    for i in range(n_steps):
        theta_proposal = theta_current + proposal_sigma * np.random.randn(7)
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
                  f'H₀={theta_current[0]:.1f}  ΔN_ur={theta_current[3]:.2f}  '
                  f'w₀={theta_current[4]:.3f}  acc={acc:.0%}  ETA={eta:.0f}s')

    elapsed = time.time() - t0
    print(f'\n  Done in {elapsed:.0f}s ({elapsed/n_steps:.1f}s/step, '
          f'acc={accepted/n_steps:.0%})')

    # Best fit
    post = chain[burn_in:]
    post_lp = log_probs[burn_in:]
    best_idx = np.argmax(post_lp)
    best = post[best_idx]
    best_lp = post_lp[best_idx]

    obs_best = run_class_multi(*best)

    print(f'\n  {"="*60}')
    print(f'  MULTI-DOMAIN BEST FIT (logL={best_lp:.1f})')
    print(f'  {"="*60}')
    for j, (label, val) in enumerate(zip(labels, best)):
        lo = np.percentile(post[:, j], 16)
        hi = np.percentile(post[:, j], 84)
        print(f'    {label:>8} = {val:.5f}  ({lo:.5f} — {hi:.5f})')

    if obs_best:
        print(f'\n    σ₈ = {obs_best["sigma8"]:.4f}')
        print(f'    r_d = {obs_best["rs_drag"]:.2f} Mpc')
        print(f'    R = {obs_best["R"]:.4f} ({abs(obs_best["R"]-R_OBS)/R_ERR:.1f}σ)')
        print(f'    l_a = {obs_best["la"]:.3f} ({abs(obs_best["la"]-LA_OBS)/LA_ERR:.1f}σ)')

    delta_chi2 = -2 * (best_lp - ll_lcdm)
    n_extra = 4  # ΔN_ur, w₀, wₐ, Ω_fld
    delta_aic = delta_chi2 + 2 * n_extra

    print(f'\n    Δχ² vs ΛCDM = {delta_chi2:.1f}')
    print(f'    ΔAIC = {delta_aic:.1f} ({n_extra} extra params)')

    if delta_aic < -10:
        print(f'    → VERY STRONGLY PREFERRED over ΛCDM')
    elif delta_aic < -2:
        print(f'    → PREFERRED over ΛCDM')
    elif delta_aic < 2:
        print(f'    → Comparable to ΛCDM')
    else:
        print(f'    → ΛCDM preferred')

    # Compare single vs multi domain
    print(f'\n  Single-domain best: H₀=69.9, σ₈=0.854, Δχ²=-29.6')
    print(f'  Multi-domain best:  H₀={best[0]:.1f}, σ₈={obs_best["sigma8"]:.4f}, '
          f'Δχ²={delta_chi2:.1f}')

    # Plot
    fig, axes = plt.subplots(4, 2, figsize=(14, 16))
    fig.suptitle('IDT Multi-Domain MCMC — Two Epochs',
                 fontsize=14, fontweight='bold')

    ax = axes[0, 0]
    ax.plot(log_probs, 'k-', lw=0.5, alpha=0.7)
    ax.axvline(burn_in, color='red', ls='--')
    ax.axhline(ll_lcdm, color='blue', ls=':', label='ΛCDM')
    ax.set_ylabel('log P')
    ax.set_title('Log-probability')
    ax.legend(fontsize=7)

    ax = axes[0, 1]
    ax.hist(post_lp, bins=30, color='steelblue', alpha=0.7)
    ax.axvline(ll_lcdm, color='blue', ls=':')
    ax.set_xlabel('log P')

    for i, label in enumerate(labels):
        row = (i + 2) // 2
        col = (i + 2) % 2
        if row < 4:
            ax = axes[row, col]
            ax.hist(post[:, i], bins=30, color='steelblue', alpha=0.7)
            ax.axvline(best[i], color='red', lw=1.5)
            ax.axvline(np.median(post[:, i]), color='orange', ls='--')
            ax.set_xlabel(label)

    plt.tight_layout()
    plt.savefig('idt_mcmc_multidomain.png', dpi=150, bbox_inches='tight')
    plt.close()
    print('\n  Saved: idt_mcmc_multidomain.png')

    return chain, log_probs, best


if __name__ == "__main__":
    chain, log_probs, best = run_mcmc(n_steps=600, burn_in=150)
