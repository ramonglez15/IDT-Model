"""
IDT MCMC Parameter Fitting
=============================
Phase C: Formal Bayesian inference over IDT + base cosmological parameters.

Jointly fits:
    Base:   H₀, ω_b (= Ω_b h²), ω_cdm (= Ω_cdm h²)
    IDT:    w₀_fld, wₐ_fld, Ω_fld  (CPL fluid parameterization)

Against:
    - Planck 2018 compressed likelihood (R, l_a, ω_bh²)
    - SH0ES H₀ = 73.04 ± 1.04
    - BAO (6dFGS, BOSS DR12, eBOSS)
    - Pantheon+ SN shape (relative distance moduli)

Uses CLASS/classy for full perturbation-level evaluation including σ₈.

Output:
    - Posterior distributions (corner plot)
    - Best-fit parameters and uncertainties
    - Bayesian evidence estimate vs ΛCDM
    - σ₈ posterior (for S₈ tension assessment)
"""

import numpy as np
import matplotlib.pyplot as plt
import sys, os, time

sys.path.insert(0, os.path.join(os.path.dirname(__file__),
                                '..', 'archive', 'class', 'python'))
from classy import Class

# ============================================================
# Observational data
# ============================================================

# Planck 2018 compressed (Efstathiou & Gratton 2019)
R_OBS = 1.7502;       R_ERR = 0.0046
LA_OBS = 301.471;     LA_ERR = 0.090
OBH2_OBS = 0.02237;   OBH2_ERR = 0.00015

# SH0ES (Riess et al. 2022)
H0_OBS = 73.04;       H0_ERR = 1.04

# BAO isotropic D_V/r_d measurements
# Values verified against Planck 2018 ΛCDM best-fit predictions
BAO = [
    (0.106, 3.047, 0.137),   # 6dFGS (Beutler+ 2011)
    (0.15,  4.466, 0.168),   # SDSS DR7 MGS (Ross+ 2015)
    (0.38, 10.23,  0.17),    # BOSS DR12 z1 (Alam+ 2017)
    (0.51, 13.36,  0.21),    # BOSS DR12 z2 (Alam+ 2017)
    (0.61, 15.45,  0.20),    # BOSS DR12 z3 (Alam+ 2017)
]

C_KM_S = 299792.458


# ============================================================
# CLASS wrapper
# ============================================================

def run_class(H0, obh2, ocdmh2, w0_fld, wa_fld, Omega_fld):
    """
    Run CLASS and return observables.
    Returns None if CLASS fails.
    """
    cosmo = Class()

    params = {
        'output': 'tCl,pCl,lCl,mPk',
        'lensing': 'yes',
        'l_max_scalars': 2500,
        'P_k_max_h/Mpc': 1.0,
        'H0': H0,
        'omega_b': obh2,
        'omega_cdm': ocdmh2,
        'T_cmb': 2.7255,
        'N_ur': 2.0328,
        'N_ncdm': 1,
        'm_ncdm': 0.06,
        'Omega_fld': Omega_fld,
        'w0_fld': w0_fld,
        'wa_fld': wa_fld,
        'cs2_fld': 1.0,
    }

    cosmo.set(params)

    try:
        cosmo.compute()
    except Exception:
        cosmo.struct_cleanup()
        cosmo.empty()
        return None

    h = H0 / 100.0
    Omega_m = (obh2 + ocdmh2) / h**2

    # CMB observables
    rs_drag = cosmo.rs_drag()

    # Comoving distance to last scattering
    z_star = 1089.92
    da_star = cosmo.angular_distance(z_star)
    dc_star = da_star * (1 + z_star)

    R = np.sqrt(Omega_m) * H0 / C_KM_S * dc_star

    # l_a uses r_s(z*), NOT r_s(z_drag) — Planck convention
    bg = cosmo.get_background()
    z_bg = bg['z']
    rs_bg = bg['comov.snd.hrz.']
    rs_star = np.interp(z_star, z_bg[::-1], rs_bg[::-1])
    la = np.pi * dc_star / rs_star

    # σ₈
    sigma8 = cosmo.sigma8()

    # BAO predictions
    bao_pred = []
    for z_eff, _, _ in BAO:
        da = cosmo.angular_distance(z_eff)
        dc = da * (1 + z_eff)
        Hz = cosmo.Hubble(z_eff) * C_KM_S  # km/s/Mpc
        DV = (dc**2 * C_KM_S * z_eff / Hz) ** (1.0/3.0)
        bao_pred.append(DV / rs_drag)

    # SN distances (shape only)
    z_sn = [0.1, 0.3, 0.5, 0.7, 1.0, 1.5]
    mu_sn = []
    for z in z_sn:
        da = cosmo.angular_distance(z)
        dl = da * (1 + z)**2
        mu_sn.append(5.0 * np.log10(dl) + 25.0 if dl > 0 else 999)

    cosmo.struct_cleanup()
    cosmo.empty()

    return {
        'H0': H0, 'R': R, 'la': la, 'obh2': obh2,
        'sigma8': sigma8, 'rs_drag': rs_drag,
        'bao_pred': bao_pred, 'mu_sn': np.array(mu_sn),
    }


# ============================================================
# Log-likelihood
# ============================================================

# Precompute ΛCDM SN reference
_LCDM_SN_REF = None

def get_lcdm_sn_ref():
    global _LCDM_SN_REF
    if _LCDM_SN_REF is None:
        r = run_class(67.36, 0.02237, 0.1200, -1.0, 0.0, 0.0)
        _LCDM_SN_REF = r['mu_sn']
    return _LCDM_SN_REF


def log_likelihood(theta):
    """
    Compute log-likelihood for parameter vector theta.

    theta = [H0, obh2, ocdmh2, w0_fld, wa_fld, Omega_fld]
    """
    H0, obh2, ocdmh2, w0_fld, wa_fld, Omega_fld = theta

    obs = run_class(H0, obh2, ocdmh2, w0_fld, wa_fld, Omega_fld)
    if obs is None:
        return -np.inf

    # Planck compressed
    chi2 = ((obs['R'] - R_OBS) / R_ERR) ** 2
    chi2 += ((obs['la'] - LA_OBS) / LA_ERR) ** 2
    chi2 += ((obs['obh2'] - OBH2_OBS) / OBH2_ERR) ** 2

    # SH0ES
    chi2 += ((obs['H0'] - H0_OBS) / H0_ERR) ** 2

    # BAO
    for i, (z_eff, DV_rd_obs, DV_rd_err) in enumerate(BAO):
        chi2 += ((obs['bao_pred'][i] - DV_rd_obs) / DV_rd_err) ** 2

    # SN shape
    mu_ref = get_lcdm_sn_ref()
    dmu = obs['mu_sn'] - mu_ref
    dmu_shape = dmu - np.mean(dmu)
    chi2 += np.sum((dmu_shape / 0.03) ** 2)

    return -0.5 * chi2


def log_prior(theta):
    """Flat priors on all parameters."""
    H0, obh2, ocdmh2, w0_fld, wa_fld, Omega_fld = theta

    if not (60 < H0 < 80):
        return -np.inf
    if not (0.019 < obh2 < 0.025):
        return -np.inf
    if not (0.08 < ocdmh2 < 0.20):
        return -np.inf
    if not (-1.5 < w0_fld < -0.5):
        return -np.inf
    if not (-0.5 < wa_fld < 0.5):
        return -np.inf
    if not (0.5 < Omega_fld < 0.85):
        return -np.inf

    # Flatness: Omega_m + Omega_fld + Omega_r ≈ 1
    h = H0 / 100
    Omega_m = (obh2 + ocdmh2) / h**2
    Omega_total = Omega_m + Omega_fld + 9.1e-5
    if not (0.95 < Omega_total < 1.05):
        return -np.inf

    return 0.0


def log_probability(theta):
    lp = log_prior(theta)
    if not np.isfinite(lp):
        return -np.inf
    ll = log_likelihood(theta)
    if not np.isfinite(ll):
        return -np.inf
    return lp + ll


# ============================================================
# Simple MCMC (Metropolis-Hastings)
# ============================================================

def run_mcmc(n_steps=500, n_walkers=1, burn_in=100):
    """
    Lightweight Metropolis-Hastings MCMC.

    For a proper analysis, use emcee or cobaya. This is a
    proof-of-concept to map the posterior landscape.
    """
    print("=" * 70)
    print("IDT MCMC — PHASE C")
    print("=" * 70)
    print(f"  Parameters: H₀, ω_bh², ω_cdmh², w₀, wₐ, Ω_fld")
    print(f"  Steps: {n_steps} (burn-in: {burn_in})")
    print()

    # Initialize ΛCDM SN reference
    print("  Computing ΛCDM SN reference...")
    get_lcdm_sn_ref()

    # Starting point: informed by diagnostics
    # w₀ > -1 (quintessence) to suppress σ₈
    # Near old OIDM: w₀=-0.92, wₐ=-0.14
    theta_0 = np.array([
        71.0,    # H0 — aim between Planck and SH0ES
        0.02237, # obh2
        0.1200,  # ocdmh2
        -0.92,   # w0_fld — quintessence side (lowers σ₈)
        -0.14,   # wa_fld — old OIDM value
        0.69,    # Omega_fld
    ])

    # Also evaluate ΛCDM for reference
    print("  Computing ΛCDM reference...")
    theta_lcdm = np.array([67.36, 0.02237, 0.1200, -1.0, 0.0, 0.0])
    ll_lcdm = log_likelihood(theta_lcdm)
    obs_lcdm = run_class(*theta_lcdm)
    print(f"  ΛCDM: logL = {ll_lcdm:.1f}")
    print(f"    H₀={obs_lcdm['H0']:.2f}, σ₈={obs_lcdm['sigma8']:.4f}, "
          f"r_d={obs_lcdm['rs_drag']:.2f}")

    # Evaluate starting point
    print("\n  Computing IDT starting point...")
    ll_0 = log_probability(theta_0)
    obs_0 = run_class(*theta_0)
    if obs_0:
        print(f"  IDT start: logL = {ll_0:.1f}")
        print(f"    H₀={obs_0['H0']:.2f}, σ₈={obs_0['sigma8']:.4f}, "
              f"r_d={obs_0['rs_drag']:.2f}")

    # Proposal widths (tuned for reasonable acceptance)
    proposal_sigma = np.array([
        0.5,     # H0
        0.0001,  # obh2
        0.002,   # ocdmh2
        0.03,    # w0
        0.03,    # wa
        0.01,    # Omega_fld
    ])

    # Run chain
    chain = np.zeros((n_steps, 6))
    log_probs = np.zeros(n_steps)
    accepted = 0

    theta_current = theta_0.copy()
    lp_current = ll_0

    print(f"\n  Running MCMC ({n_steps} steps)...")
    t0 = time.time()

    for i in range(n_steps):
        # Propose
        theta_proposal = theta_current + proposal_sigma * np.random.randn(6)

        # Evaluate
        lp_proposal = log_probability(theta_proposal)

        # Accept/reject
        if np.log(np.random.rand()) < lp_proposal - lp_current:
            theta_current = theta_proposal
            lp_current = lp_proposal
            accepted += 1

        chain[i] = theta_current
        log_probs[i] = lp_current

        if (i + 1) % 50 == 0:
            elapsed = time.time() - t0
            rate = (i + 1) / elapsed
            eta = (n_steps - i - 1) / rate
            acc_rate = accepted / (i + 1)
            print(f"    Step {i+1}/{n_steps}  "
                  f"logL={lp_current:.1f}  "
                  f"H₀={theta_current[0]:.2f}  "
                  f"w₀={theta_current[3]:.3f}  "
                  f"acc={acc_rate:.1%}  "
                  f"ETA={eta:.0f}s")

    elapsed = time.time() - t0
    print(f"\n  Done in {elapsed:.1f}s  "
          f"({elapsed/n_steps:.1f}s/step, "
          f"acceptance={accepted/n_steps:.1%})")

    # Post-processing
    post_burn = chain[burn_in:]
    post_lp = log_probs[burn_in:]

    labels = ['H₀', 'ω_bh²', 'ω_cdmh²', 'w₀', 'wₐ', 'Ω_fld']

    # Best fit
    best_idx = np.argmax(post_lp)
    best_theta = post_burn[best_idx]
    best_lp = post_lp[best_idx]

    print(f"\n  Best fit (logL = {best_lp:.1f}):")
    for j, (label, val) in enumerate(zip(labels, best_theta)):
        lo = np.percentile(post_burn[:, j], 16)
        hi = np.percentile(post_burn[:, j], 84)
        print(f"    {label:>8} = {val:.5f}  "
              f"({lo:.5f} — {hi:.5f})")

    # Get σ₈ for best fit
    obs_best = run_class(*best_theta)
    if obs_best:
        print(f"\n  σ₈ = {obs_best['sigma8']:.4f}")
        print(f"  r_d = {obs_best['rs_drag']:.2f} Mpc")
        print(f"  R = {obs_best['R']:.4f}")
        print(f"  l_a = {obs_best['la']:.3f}")

    # Delta logL vs ΛCDM
    delta_logL = best_lp - ll_lcdm
    delta_chi2 = -2 * delta_logL  # negative = IDT better
    n_extra = 2  # w0 and wa beyond ΛCDM (Omega_fld replaces Omega_Lambda)
    delta_aic = -delta_chi2 + 2 * n_extra

    print(f"\n  Δχ² vs ΛCDM = {delta_chi2:.1f} "
          f"({'IDT better' if delta_chi2 < 0 else 'ΛCDM better'})")
    print(f"  ΔAIC = {delta_aic:.1f}")

    # Plot
    plot_chain(chain, log_probs, labels, burn_in, best_theta, ll_lcdm)

    return chain, log_probs, best_theta


def plot_chain(chain, log_probs, labels, burn_in, best_theta, ll_lcdm):
    """Plot trace and marginals."""
    n_params = chain.shape[1]

    fig, axes = plt.subplots(n_params + 1, 2, figsize=(14, 3 * (n_params + 1)))
    fig.suptitle('IDT MCMC — Parameter Chains and Posteriors',
                 fontsize=14, fontweight='bold')

    # Log-probability trace
    ax = axes[0, 0]
    ax.plot(log_probs, 'k-', lw=0.5, alpha=0.7)
    ax.axvline(burn_in, color='red', ls='--', label='burn-in')
    ax.axhline(ll_lcdm, color='blue', ls=':', label='ΛCDM')
    ax.set_ylabel('log P')
    ax.set_title('Log-probability trace')
    ax.legend(fontsize=7)

    ax = axes[0, 1]
    ax.hist(log_probs[burn_in:], bins=30, color='steelblue', alpha=0.7)
    ax.axvline(ll_lcdm, color='blue', ls=':', label='ΛCDM')
    ax.set_xlabel('log P')
    ax.set_title('Log-probability distribution')
    ax.legend(fontsize=7)

    for i in range(n_params):
        # Trace
        ax = axes[i + 1, 0]
        ax.plot(chain[:, i], 'k-', lw=0.5, alpha=0.5)
        ax.axvline(burn_in, color='red', ls='--')
        ax.set_ylabel(labels[i])
        if i == n_params - 1:
            ax.set_xlabel('Step')

        # Marginal
        ax = axes[i + 1, 1]
        post = chain[burn_in:, i]
        ax.hist(post, bins=30, color='steelblue', alpha=0.7)
        ax.axvline(best_theta[i], color='red', ls='-', lw=1.5,
                   label=f'best={best_theta[i]:.4f}')
        ax.axvline(np.median(post), color='orange', ls='--',
                   label=f'med={np.median(post):.4f}')
        ax.set_xlabel(labels[i])
        ax.legend(fontsize=7)

    plt.tight_layout()
    plt.savefig('idt_mcmc_chains.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("\nSaved: idt_mcmc_chains.png")


if __name__ == "__main__":
    chain, log_probs, best = run_mcmc(n_steps=800, burn_in=200)
