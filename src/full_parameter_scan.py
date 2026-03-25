"""
IDT Full Parameter Scan — Floating Base Cosmology
====================================================
The old OIDM model achieved H₀=73.24 by jointly fitting:
    - Base cosmology: H₀, Ω_b, Ω_cdm, (N_ur)
    - Domain parameters: f_dom, z_c, Δ_z

This scan lets the base cosmological parameters float alongside
the domain parameters, matching what an MCMC would do.

Old OIDM reference values:
    H₀ = 73.24, Ω_b = 0.0492, Ω_cdm = 0.2645
    Ω_fld = 0.6863, w₀ = -0.92, w_a = -0.14
    z_transition = 0.35, amplitude = 0.05, width = 0.1
    N_ur = 3.12
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize, differential_evolution
from scipy.integrate import quad
import sys, os

# Import our modules
from cosmology_base import _c_km_s
import cosmology_base
sys.modules['idt_class_module.cosmology_base'] = cosmology_base
from idt_domain import IDTDomain, IDTModel


# ============================================================
# Observational constraints
# ============================================================

# Planck 2018 compressed likelihood
R_PLANCK = 1.7502;  R_ERR = 0.0046
LA_PLANCK = 301.471;  LA_ERR = 0.090
OMEGA_BH2_PLANCK = 0.02237;  OMEGA_BH2_ERR = 0.00015

# SH0ES (Riess et al. 2022)
H0_SHOES = 73.04;  H0_SHOES_ERR = 1.04

# BAO measurements (BOSS DR12, eBOSS)
BAO_DATA = [
    # (z_eff, D_V/r_d, error)  — isotropic BAO
    (0.15, 4.466, 0.168),    # 6dFGS
    (0.38, 10.27, 0.15),     # BOSS DR12
    (0.51, 13.38, 0.18),     # BOSS DR12
    (0.70, 17.86, 0.33),     # eBOSS LRG
    (1.48, 30.69, 0.80),     # eBOSS QSO
    (2.33, 37.6, 1.1),       # eBOSS Lya
]

# Pantheon+ SN binned (approx distance moduli at key redshifts)
# These constrain the shape of d_L(z), not H₀ directly
SN_MAX_DMU = 0.03  # mag tolerance vs best-fit


# ============================================================
# Cosmology functions with variable base parameters
# ============================================================

def E2_base(z, Omega_m, Omega_r, Omega_Lambda):
    """(H/H₀)² for flat ΛCDM with given parameters."""
    z = np.asarray(z, dtype=float)
    return Omega_m * (1+z)**3 + Omega_r * (1+z)**4 + Omega_Lambda


def H_func(z, H0, Omega_m, Omega_r, Omega_Lambda, domains=None):
    """H(z) in km/s/Mpc with variable parameters and optional domains."""
    z = np.asarray(z, dtype=float)
    E2 = E2_base(z, Omega_m, Omega_r, Omega_Lambda)
    if domains:
        for d in domains:
            E2 = E2 + d.Omega(z)
    return H0 * np.sqrt(np.maximum(E2, 0))


def sound_horizon_general(H_func_eval, z_drag=1059.94,
                          Omega_b=0.0493, Omega_gamma=5.38e-5):
    """Comoving sound horizon with general H(z)."""
    def integrand(z):
        R_b = 3.0 * Omega_b / (4.0 * Omega_gamma * (1.0 + z))
        c_s = _c_km_s / np.sqrt(3.0 * (1.0 + R_b))
        return c_s / H_func_eval(z)
    result, _ = quad(integrand, z_drag, 1e5, limit=500)
    return result


def comoving_distance_general(z_val, H_func_eval):
    """Comoving distance d_C(z) in Mpc."""
    if z_val < 1e-6:
        return 0.0
    result, _ = quad(lambda zp: _c_km_s / H_func_eval(zp), 0, z_val,
                     limit=200)
    return result


def DV_over_rd(z_val, H_func_eval, rd):
    """D_V(z)/r_d for BAO comparison."""
    dC = comoving_distance_general(z_val, H_func_eval)
    Hz = H_func_eval(z_val)
    DV = (dC**2 * _c_km_s * z_val / Hz) ** (1.0/3.0)
    return DV / rd


def distance_modulus_general(z_val, H_func_eval):
    """Distance modulus μ(z) in magnitudes."""
    dL = (1 + z_val) * comoving_distance_general(z_val, H_func_eval)
    if dL <= 0:
        return np.nan
    return 5.0 * np.log10(dL) + 25.0


# ============================================================
# Chi-squared evaluation
# ============================================================

def chi2_full(params, domain_configs, include_bao=True, verbose=False):
    """
    Compute total χ² for a full parameter set.

    Parameters
    ----------
    params : array
        [H0, Omega_b, Omega_cdm]
        Base cosmological parameters to float.
    domain_configs : list of tuples
        [(f_dom, z_c, delta_z), ...] for each domain
    """
    H0, Omega_b, Omega_cdm = params

    # Derived
    h = H0 / 100.0
    omega_bh2 = Omega_b * h**2
    Omega_m = Omega_b + Omega_cdm
    Omega_r = 9.1e-5  # radiation (fixed)
    Omega_gamma = 5.38e-5
    Omega_Lambda = 1.0 - Omega_m - Omega_r

    if Omega_Lambda < 0 or Omega_m > 1 or Omega_b < 0 or Omega_cdm < 0:
        return 1e10

    # Build domains
    domains = []
    for f, zc, dz in domain_configs:
        try:
            # Need to build domain with this cosmology's E2
            # The domain uses E2_LCDM internally for normalization
            # We need to account for the different base cosmology
            d = IDTDomain(f_dom=f, z_c=zc, delta_z=dz)
            domains.append(d)
        except Exception:
            return 1e10

    # Build H(z) function
    def H_eval(z):
        return H_func(z, H0, Omega_m, Omega_r, Omega_Lambda, domains)

    # Sound horizon
    rd = sound_horizon_general(H_eval, Omega_b=Omega_b,
                               Omega_gamma=Omega_gamma)

    # CMB shift parameters
    z_star = 1089.92
    dC_star = comoving_distance_general(z_star, H_eval)
    R = np.sqrt(Omega_m) * H0 / _c_km_s * dC_star
    la = np.pi * dC_star / rd

    # Chi² components
    chi2_R = ((R - R_PLANCK) / R_ERR) ** 2
    chi2_la = ((la - LA_PLANCK) / LA_ERR) ** 2
    chi2_obh2 = ((omega_bh2 - OMEGA_BH2_PLANCK) / OMEGA_BH2_ERR) ** 2
    chi2_H0 = ((H0 - H0_SHOES) / H0_SHOES_ERR) ** 2

    # BAO
    chi2_bao = 0.0
    if include_bao:
        for z_eff, DV_rd_obs, DV_rd_err in BAO_DATA:
            DV_rd_pred = DV_over_rd(z_eff, H_eval, rd)
            chi2_bao += ((DV_rd_pred - DV_rd_obs) / DV_rd_err) ** 2

    # SN shape constraint (relative distances)
    z_sn = np.array([0.1, 0.3, 0.5, 0.7, 1.0, 1.5])
    def H_lcdm_ref(z):
        return 67.36 * np.sqrt(E2_base(z, 0.3153, 9.1e-5, 1-0.3153-9.1e-5))

    mu_ref = np.array([distance_modulus_general(z, H_lcdm_ref) for z in z_sn])
    mu_model = np.array([distance_modulus_general(z, H_eval) for z in z_sn])
    # Compare shape (relative differences), not absolute (H₀ shifts all)
    # Remove mean offset (absorbed by M_B calibration)
    dmu = (mu_model - mu_ref)
    dmu_shape = dmu - np.mean(dmu)
    chi2_sn = np.sum((dmu_shape / SN_MAX_DMU) ** 2)

    total = chi2_R + chi2_la + chi2_obh2 + chi2_H0 + chi2_bao + chi2_sn

    if verbose:
        print(f"    H₀={H0:.2f}, Ω_b={Omega_b:.4f}, Ω_cdm={Omega_cdm:.4f}")
        print(f"    ω_bh²={omega_bh2:.5f}, Ω_m={Omega_m:.4f}, Ω_Λ={Omega_Lambda:.4f}")
        print(f"    r_d={rd:.2f} Mpc")
        print(f"    R={R:.4f} ({abs(R-R_PLANCK)/R_ERR:.1f}σ)")
        print(f"    l_a={la:.3f} ({abs(la-LA_PLANCK)/LA_ERR:.1f}σ)")
        print(f"    χ²: R={chi2_R:.1f} l_a={chi2_la:.1f} ωbh²={chi2_obh2:.1f} "
              f"H₀={chi2_H0:.1f} BAO={chi2_bao:.1f} SN={chi2_sn:.1f}")
        print(f"    Total χ² = {total:.1f}")

    return total


# ============================================================
# Optimization
# ============================================================

def optimize_base_for_domains(domain_configs, verbose=True):
    """
    Find the best-fit base cosmology (H₀, Ω_b, Ω_cdm) for a
    given set of domain configurations.
    """
    def objective(params):
        return chi2_full(params, domain_configs)

    # Bounds: H₀ ∈ [60, 80], Ω_b ∈ [0.03, 0.07], Ω_cdm ∈ [0.15, 0.40]
    bounds = [(60, 80), (0.03, 0.07), (0.15, 0.40)]

    # Start near old OIDM values
    x0 = [73.24, 0.0492, 0.2645]

    # Also try Planck start
    x0_planck = [67.36, 0.0493, 0.2660]

    results = []

    # Try multiple starting points
    for x_start in [x0, x0_planck,
                    [70.0, 0.049, 0.25],
                    [72.0, 0.050, 0.27]]:
        try:
            res = minimize(objective, x_start, method='Nelder-Mead',
                           options={'maxiter': 2000, 'xatol': 0.01,
                                    'fatol': 0.1})
            results.append(res)
        except Exception:
            continue

    # Also try differential evolution for global search
    try:
        res_de = differential_evolution(objective, bounds,
                                        maxiter=200, tol=0.1,
                                        seed=42, polish=True)
        results.append(res_de)
    except Exception:
        pass

    # Best result
    best = min(results, key=lambda r: r.fun)

    if verbose:
        domains_str = " + ".join(
            f"({f:.3f}, z={z:.0f}, Δ={d:.0f})"
            for f, z, d in domain_configs
        )
        print(f"\n  Domains: {domains_str}")
        chi2_full(best.x, domain_configs, verbose=True)

    return best


# ============================================================
# Main scan
# ============================================================

def scan_with_floating_cosmology():
    """
    For each domain configuration, optimize the base cosmology.
    """
    print("=" * 70)
    print("IDT FULL PARAMETER SCAN — FLOATING BASE COSMOLOGY")
    print("=" * 70)
    print()

    # First: ΛCDM baseline (no domains)
    print("--- ΛCDM BASELINE (no domains) ---")
    res_lcdm = optimize_base_for_domains([])
    chi2_lcdm = res_lcdm.fun
    print(f"  Best ΛCDM χ² = {chi2_lcdm:.1f}")

    # Domain configurations to test
    configs = {
        # Single late-time (like old OIDM)
        "Late z=0.35 (OIDM-like)": [(0.01, 0.35, 0.1)],
        "Late z=0.5": [(0.01, 0.5, 0.2)],
        "Late z=1.0": [(0.02, 1.0, 0.3)],

        # Single early
        "Early z=1500 narrow": [(0.03, 1500, 150)],
        "Early z=2000 narrow": [(0.05, 2000, 200)],
        "Early z=3000 narrow": [(0.03, 3000, 300)],

        # Two-domain: early + late (core IDT prediction)
        "Early z=2000 + Late z=0.35": [
            (0.05, 2000, 200), (0.01, 0.35, 0.1)],
        "Early z=3000 + Late z=0.35": [
            (0.03, 3000, 300), (0.01, 0.35, 0.1)],
        "Early z=2000 + Late z=1.0": [
            (0.05, 2000, 400), (0.02, 1.0, 0.3)],
        "Early z=1500 + Late z=0.5": [
            (0.05, 1500, 300), (0.01, 0.5, 0.2)],
        "Early z=3000 + Late z=1.0": [
            (0.03, 3000, 300), (0.02, 1.0, 0.5)],

        # Old OIDM-inspired: stronger late domain
        "OIDM-inspired (late z=0.35 strong)": [(0.03, 0.35, 0.1)],
        "OIDM-inspired + early": [
            (0.05, 2000, 400), (0.03, 0.35, 0.1)],

        # Three-domain
        "Three: z=3000 + z=1100 + z=0.5": [
            (0.03, 3000, 300), (0.03, 1100, 110), (0.01, 0.5, 0.2)],
    }

    all_results = []

    for name, domain_config in configs.items():
        print(f"\n{'='*60}")
        print(f"  CONFIG: {name}")
        print(f"{'='*60}")

        res = optimize_base_for_domains(domain_config)
        n_domain_params = len(domain_config) * 3
        n_extra = 3 + n_domain_params  # 3 base + domain params
        # But ΛCDM also has 3 base params, so extra = domain params only
        delta_chi2 = res.fun - chi2_lcdm
        delta_aic = delta_chi2 + 2 * n_domain_params

        H0_best = res.x[0]

        all_results.append({
            'name': name,
            'domains': domain_config,
            'H0': H0_best,
            'Omega_b': res.x[1],
            'Omega_cdm': res.x[2],
            'chi2': res.fun,
            'delta_chi2': delta_chi2,
            'delta_aic': delta_aic,
            'n_domain_params': n_domain_params,
        })

        verdict = ""
        if delta_aic < -5:
            verdict = "STRONGLY PREFERRED"
        elif delta_aic < -2:
            verdict = "PREFERRED"
        elif delta_aic < 2:
            verdict = "COMPARABLE"
        else:
            verdict = "ΛCDM preferred"

        print(f"  → Δχ²={delta_chi2:+.1f}, ΔAIC={delta_aic:+.1f} → {verdict}")

    # Final summary
    print("\n\n" + "=" * 70)
    print("FINAL RANKING (by ΔAIC)")
    print("=" * 70)
    print(f"\n  ΛCDM baseline: χ² = {chi2_lcdm:.1f}\n")

    all_results.sort(key=lambda r: r['delta_aic'])
    for i, r in enumerate(all_results):
        verdict = ""
        if r['delta_aic'] < -5:
            verdict = " ★★★"
        elif r['delta_aic'] < -2:
            verdict = " ★★"
        elif r['delta_aic'] < 2:
            verdict = " ★"

        print(f"  #{i+1}: {r['name']}")
        print(f"      H₀={r['H0']:.2f}  χ²={r['chi2']:.1f}  "
              f"Δχ²={r['delta_chi2']:+.1f}  "
              f"ΔAIC={r['delta_aic']:+.1f}{verdict}")

    return all_results, chi2_lcdm


if __name__ == "__main__":
    results, chi2_lcdm = scan_with_floating_cosmology()
