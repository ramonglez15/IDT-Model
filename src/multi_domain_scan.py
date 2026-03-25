"""
IDT Multi-Domain Parameter Scanner
====================================
Explores multi-epoch domain configurations: the core IDT prediction
that domains at different cosmic epochs create the observed tensions.

Strategy:
    1. Early domain (z ~ 1000-5000): shifts sound horizon r_d → raises H₀
    2. Late domain (z ~ 0.1-10): modifies distance-redshift relation,
       can compensate l_a shift and suppress growth (σ₈)

Reference from old OIDM model (archive/CLASS-IDT):
    H₀ = 73.24, w₀ = -0.92, w_a = -0.14
    z_transition = 0.35, amplitude = 0.05, width = 0.1
    Ω_fld = 0.6863, cs²_fld = 1.0
"""

import numpy as np
import matplotlib.pyplot as plt
from cosmology_base import (E2_LCDM, H_LCDM, sound_horizon,
                            comoving_distance, distance_modulus,
                            CMB_shift_parameters, _H0, _c_km_s)
import cosmology_base
import sys
sys.modules['idt_class_module.cosmology_base'] = cosmology_base
from idt_domain import IDTDomain, IDTModel

# ============================================================
# Observational constraints
# ============================================================
R_PLANCK = 1.7502;  R_ERR = 0.0046
LA_PLANCK = 301.471;  LA_ERR = 0.090
H0_SHOES = 73.04;  H0_SHOES_ERR = 1.04
SN_MAX_DMU = 0.02


def evaluate_model(domains, verbose=False):
    """
    Evaluate a multi-domain IDT model against all constraints.
    """
    try:
        model = IDTModel(domains=domains)
    except Exception:
        return None

    rd_lcdm = sound_horizon(H_LCDM)
    rd_idt = sound_horizon(model.H)
    H0_inferred = _H0 * rd_lcdm / rd_idt

    sp = CMB_shift_parameters(model.H)
    R_idt = sp['R']
    la_idt = sp['l_a']

    # Late-time SN check
    z_sn = np.linspace(0.01, 2.0, 50)
    mu_lcdm = np.array([distance_modulus(z, H_LCDM) for z in z_sn])
    mu_idt = np.array([distance_modulus(z, model.H) for z in z_sn])
    max_dmu = np.max(np.abs(mu_idt - mu_lcdm))

    chi2_R = ((R_idt - R_PLANCK) / R_ERR) ** 2
    chi2_la = ((la_idt - LA_PLANCK) / LA_ERR) ** 2
    chi2_H0 = ((H0_inferred - H0_SHOES) / H0_SHOES_ERR) ** 2
    chi2_sn = (max_dmu / SN_MAX_DMU) ** 2 if max_dmu > SN_MAX_DMU else 0.0

    chi2_total = chi2_R + chi2_la + chi2_H0 + chi2_sn

    result = {
        'domains': [(d.f_dom, d.z_c, d.delta_z) for d in domains],
        'n_domains': len(domains),
        'rd_idt': rd_idt,
        'drd_pct': (rd_idt - rd_lcdm) / rd_lcdm * 100,
        'H0_inferred': H0_inferred,
        'R': R_idt,
        'la': la_idt,
        'max_dmu': max_dmu,
        'chi2_R': chi2_R,
        'chi2_la': chi2_la,
        'chi2_H0': chi2_H0,
        'chi2_sn': chi2_sn,
        'chi2_total': chi2_total,
    }

    if verbose:
        print(f"  Domains: {result['domains']}")
        print(f"    H₀ = {H0_inferred:.2f} "
              f"({abs(H0_inferred-H0_SHOES)/H0_SHOES_ERR:.1f}σ from SH0ES)")
        print(f"    R = {R_idt:.4f} ({abs(R_idt-R_PLANCK)/R_ERR:.1f}σ)")
        print(f"    l_a = {la_idt:.3f} ({abs(la_idt-LA_PLANCK)/LA_ERR:.1f}σ)")
        print(f"    Δr_d/r_d = {result['drd_pct']:+.2f}%")
        print(f"    max|Δμ| = {max_dmu:.4f} mag")
        print(f"    χ² = {chi2_total:.1f} "
              f"(R:{chi2_R:.1f} + l_a:{chi2_la:.1f} + "
              f"H₀:{chi2_H0:.1f} + SN:{chi2_sn:.1f})")

    return result


def print_result(r, rank=None):
    """Pretty-print a result."""
    prefix = f"#{rank}: " if rank else ""
    domains_str = " + ".join(
        f"({f:.3f}, z={z:.0f}, Δ={d:.0f})"
        for f, z, d in r['domains']
    )
    R_sig = abs(r['R'] - R_PLANCK) / R_ERR
    la_sig = abs(r['la'] - LA_PLANCK) / LA_ERR
    H0_sig = abs(r['H0_inferred'] - H0_SHOES) / H0_SHOES_ERR

    print(f"  {prefix}{domains_str}")
    print(f"      H₀={r['H0_inferred']:.2f} ({H0_sig:.1f}σ)  "
          f"R={r['R']:.4f} ({R_sig:.1f}σ)  "
          f"l_a={r['la']:.3f} ({la_sig:.1f}σ)  "
          f"Δμ={r['max_dmu']:.4f}  "
          f"χ²={r['chi2_total']:.1f}")


# ============================================================
# Scan 1: Single late-time domain (like old OIDM model)
# ============================================================

def scan_late_domain():
    """
    Scan late-time domains (z_c < 50) to understand what the old
    OIDM model was doing in the new parameterization.
    """
    print("=" * 70)
    print("SCAN 1: SINGLE LATE-TIME DOMAIN")
    print("=" * 70)
    print("(Analogous to old OIDM hidden region at z=0.35)")
    print()

    results = []
    f_vals = np.linspace(0.001, 0.05, 15)
    zc_vals = np.array([0.2, 0.35, 0.5, 0.75, 1.0, 1.5, 2.0, 3.0, 5.0, 10.0])
    dz_fracs = [0.3, 0.5, 1.0]

    for f in f_vals:
        for zc in zc_vals:
            for frac in dz_fracs:
                dz = max(frac * zc, 0.05)
                try:
                    domain = IDTDomain(f_dom=f, z_c=zc, delta_z=dz)
                    r = evaluate_model([domain])
                    if r is not None:
                        results.append(r)
                except Exception:
                    continue

    print(f"  Evaluated {len(results)} points\n")

    results.sort(key=lambda r: r['chi2_total'])
    print("  Top 5 late-time single domains:")
    for i, r in enumerate(results[:5]):
        print_result(r, i + 1)
    print()

    return results


# ============================================================
# Scan 2: Two-domain (early + late)
# ============================================================

def scan_two_domain():
    """
    The core IDT prediction: domains at different epochs.
    Early domain shifts r_d (raises H₀).
    Late domain compensates l_a and/or modifies distances.
    """
    print("=" * 70)
    print("SCAN 2: TWO-DOMAIN MODEL (EARLY + LATE)")
    print("=" * 70)
    print("Early domain: shifts r_d → raises H₀")
    print("Late domain: compensates l_a, modifies distances")
    print()

    results = []

    # Early domain grid
    early_configs = [
        (0.02, 2000, 600),
        (0.03, 2000, 600),
        (0.05, 1500, 450),
        (0.05, 2000, 600),
        (0.05, 2500, 750),
        (0.05, 3000, 900),
        (0.07, 2000, 600),
        (0.07, 2500, 750),
        (0.10, 2000, 600),
        (0.10, 3000, 900),
        (0.03, 1500, 450),
        (0.03, 2500, 750),
        (0.03, 3000, 300),   # narrow early
        (0.05, 2000, 200),   # very narrow
        (0.05, 3000, 300),   # narrow high-z
    ]

    # Late domain grid
    late_configs = [
        (0.001, 0.35, 0.1),
        (0.002, 0.35, 0.1),
        (0.005, 0.35, 0.15),
        (0.005, 0.5, 0.2),
        (0.005, 1.0, 0.3),
        (0.01, 0.35, 0.1),
        (0.01, 0.5, 0.2),
        (0.01, 1.0, 0.5),
        (0.01, 2.0, 0.6),
        (0.02, 0.5, 0.2),
        (0.02, 1.0, 0.3),
        (0.02, 2.0, 0.6),
        (0.03, 0.5, 0.2),
        (0.03, 1.0, 0.5),
        (0.005, 0.35, 0.05),  # very narrow late
        (0.01, 0.35, 0.05),
        (0.005, 5.0, 1.5),    # intermediate z
        (0.01, 5.0, 1.5),
        (0.01, 10.0, 3.0),
        (0.02, 10.0, 3.0),
    ]

    total = len(early_configs) * len(late_configs)
    print(f"  Testing {len(early_configs)} early × {len(late_configs)} late "
          f"= {total} combinations\n")

    count = 0
    for f_e, zc_e, dz_e in early_configs:
        for f_l, zc_l, dz_l in late_configs:
            try:
                d_early = IDTDomain(f_dom=f_e, z_c=zc_e, delta_z=dz_e)
                d_late = IDTDomain(f_dom=f_l, z_c=zc_l, delta_z=dz_l)
                r = evaluate_model([d_early, d_late])
                if r is not None:
                    results.append(r)
            except Exception:
                continue

            count += 1
            if count % 50 == 0:
                print(f"  {count}/{total}", end='\r')

    print(f"\n  Evaluated {len(results)} valid combinations\n")

    results.sort(key=lambda r: r['chi2_total'])

    print("  Top 15 two-domain models:")
    for i, r in enumerate(results[:15]):
        print_result(r, i + 1)

    return results


# ============================================================
# Scan 3: Width exploration for promising early domains
# ============================================================

def scan_narrow_early():
    """
    Test whether very narrow early domains can shift r_d
    without destroying l_a.
    """
    print("\n" + "=" * 70)
    print("SCAN 3: NARROW EARLY DOMAINS")
    print("=" * 70)
    print("Can a very narrow domain shift r_d with minimal l_a impact?")
    print()

    results = []
    f_vals = np.linspace(0.01, 0.15, 12)
    zc_vals = [1060, 1200, 1500, 2000, 2500, 3000, 4000, 5000]
    width_fracs = [0.02, 0.05, 0.08, 0.1, 0.15, 0.2, 0.3, 0.5]

    total = len(f_vals) * len(zc_vals) * len(width_fracs)

    count = 0
    for f in f_vals:
        for zc in zc_vals:
            for frac in width_fracs:
                dz = frac * zc
                try:
                    domain = IDTDomain(f_dom=f, z_c=zc, delta_z=dz)
                    r = evaluate_model([domain])
                    if r is not None:
                        results.append(r)
                except Exception:
                    continue
                count += 1
                if count % 100 == 0:
                    print(f"  {count}/{total}", end='\r')

    print(f"\n  Evaluated {len(results)} points\n")

    results.sort(key=lambda r: r['chi2_total'])

    print("  Top 10 narrow early domains:")
    for i, r in enumerate(results[:10]):
        print_result(r, i + 1)

    # Also find best H₀ improver that keeps l_a < 5σ
    la_ok = [r for r in results
             if abs(r['la'] - LA_PLANCK) / LA_ERR < 5.0]
    if la_ok:
        la_ok.sort(key=lambda r: abs(r['H0_inferred'] - H0_SHOES))
        print(f"\n  Best H₀ with l_a < 5σ:")
        for i, r in enumerate(la_ok[:5]):
            print_result(r, i + 1)

    return results


# ============================================================
# Scan 4: Three-domain model
# ============================================================

def scan_three_domain():
    """
    Three domains at different epochs:
    - Very early (z ~ 3000-5000): pre-recombination
    - Near recombination (z ~ 1000-1500): around decoupling
    - Late (z ~ 0.3-2): dark energy era
    """
    print("\n" + "=" * 70)
    print("SCAN 4: THREE-DOMAIN MODEL")
    print("=" * 70)
    print()

    results = []

    very_early = [
        (0.02, 4000, 400),
        (0.03, 3000, 300),
        (0.05, 3000, 300),
        (0.03, 5000, 500),
    ]

    near_recomb = [
        (0.02, 1200, 120),
        (0.03, 1100, 110),
        (0.03, 1200, 200),
        (0.05, 1100, 110),
    ]

    late = [
        (0.005, 0.35, 0.1),
        (0.01, 0.5, 0.2),
        (0.01, 1.0, 0.3),
        (0.02, 1.0, 0.5),
    ]

    total = len(very_early) * len(near_recomb) * len(late)
    print(f"  Testing {total} three-domain combinations\n")

    count = 0
    for fe, ze, de in very_early:
        for fm, zm, dm in near_recomb:
            for fl, zl, dl in late:
                try:
                    d1 = IDTDomain(f_dom=fe, z_c=ze, delta_z=de)
                    d2 = IDTDomain(f_dom=fm, z_c=zm, delta_z=dm)
                    d3 = IDTDomain(f_dom=fl, z_c=zl, delta_z=dl)
                    r = evaluate_model([d1, d2, d3])
                    if r is not None:
                        results.append(r)
                except Exception:
                    continue
                count += 1

    print(f"  Evaluated {len(results)} valid combinations\n")

    results.sort(key=lambda r: r['chi2_total'])

    print("  Top 10 three-domain models:")
    for i, r in enumerate(results[:10]):
        print_result(r, i + 1)

    return results


# ============================================================
# Summary and comparison
# ============================================================

def summarize(all_results):
    """Compare best results across all scan types."""
    print("\n" + "=" * 70)
    print("SUMMARY: BEST MODELS COMPARED TO ΛCDM")
    print("=" * 70)

    # ΛCDM baseline
    sp_lcdm = CMB_shift_parameters(H_LCDM)
    chi2_lcdm = ((67.36 - H0_SHOES) / H0_SHOES_ERR) ** 2
    chi2_lcdm += ((sp_lcdm['R'] - R_PLANCK) / R_ERR) ** 2
    chi2_lcdm += ((sp_lcdm['l_a'] - LA_PLANCK) / LA_ERR) ** 2

    print(f"\n  ΛCDM: H₀=67.36, χ²={chi2_lcdm:.1f} (0 extra params)")

    for label, results in all_results.items():
        if not results:
            continue
        best = min(results, key=lambda r: r['chi2_total'])
        n_params = best['n_domains'] * 3
        delta_chi2 = best['chi2_total'] - chi2_lcdm
        # AIC penalty: +2 per extra parameter
        aic_penalty = 2 * n_params
        delta_aic = delta_chi2 + aic_penalty

        print(f"\n  {label}:")
        print_result(best)
        print(f"      Δχ² vs ΛCDM = {delta_chi2:+.1f}, "
              f"ΔAIC = {delta_aic:+.1f} "
              f"({n_params} extra params)")
        if delta_aic < -2:
            print(f"      → PREFERRED over ΛCDM (ΔAIC < -2)")
        elif delta_aic < 2:
            print(f"      → Comparable to ΛCDM")
        else:
            print(f"      → ΛCDM preferred (ΔAIC > 2)")


if __name__ == "__main__":
    print("=" * 70)
    print("IDT MULTI-DOMAIN PARAMETER DISCOVERY")
    print("=" * 70)
    print()

    all_results = {}

    r1 = scan_late_domain()
    all_results['Late-time single domain'] = r1

    r2 = scan_two_domain()
    all_results['Two-domain (early+late)'] = r2

    r3 = scan_narrow_early()
    all_results['Narrow early domain'] = r3

    r4 = scan_three_domain()
    all_results['Three-domain'] = r4

    summarize(all_results)
