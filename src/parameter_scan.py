"""
IDT Parameter Space Scanner
=============================
Systematic exploration of (f_dom, z_c, Δ_z) parameter space
against background-level observational constraints.

This is the parameter discovery tool — it maps which regions of
parameter space are viable before committing to expensive CLASS runs.

Constraints used:
    1. Planck 2018 shift parameter R = 1.7502 ± 0.0046
    2. Planck 2018 acoustic scale l_a = 301.471 ± 0.090
    3. SH0ES H₀ = 73.04 ± 1.04 km/s/Mpc (local measurement)
    4. Planck H₀ = 67.4 ± 0.5 km/s/Mpc (CMB-inferred, ΛCDM)
    5. Late-time distance modulus (max|Δμ| < 0.02 mag vs SN)

The scan computes a combined χ² for each parameter point and
identifies the regions where IDT can improve H₀ while staying
consistent with CMB and SN data.
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

# Planck 2018 compressed likelihood (Efstathiou & Gratton 2019)
R_PLANCK = 1.7502
R_ERR = 0.0046

LA_PLANCK = 301.471
LA_ERR = 0.090

# SH0ES (Riess et al. 2022)
H0_SHOES = 73.04
H0_SHOES_ERR = 1.04

# Planck ΛCDM-inferred H₀
H0_PLANCK = 67.4
H0_PLANCK_ERR = 0.5

# SN distance threshold (conservative)
SN_MAX_DMU = 0.02  # mag


def evaluate_point(f_dom, z_c, delta_z, verbose=False):
    """
    Evaluate a single parameter point against all constraints.

    Returns dict with chi² contributions and derived quantities.
    """
    try:
        domain = IDTDomain(f_dom=f_dom, z_c=z_c, delta_z=delta_z)
        model = IDTModel(domains=[domain])
    except (AssertionError, ValueError):
        return None

    # Sound horizon and inferred H₀
    rd_lcdm = sound_horizon(H_LCDM)
    rd_idt = sound_horizon(model.H)
    H0_inferred = _H0 * rd_lcdm / rd_idt

    # CMB shift parameters
    sp = CMB_shift_parameters(model.H)
    R_idt = sp['R']
    la_idt = sp['l_a']

    # Late-time SN check
    z_sn = np.linspace(0.01, 2.0, 50)
    mu_lcdm = np.array([distance_modulus(z, H_LCDM) for z in z_sn])
    mu_idt = np.array([distance_modulus(z, model.H) for z in z_sn])
    max_dmu = np.max(np.abs(mu_idt - mu_lcdm))

    # Chi² contributions
    chi2_R = ((R_idt - R_PLANCK) / R_ERR) ** 2
    chi2_la = ((la_idt - LA_PLANCK) / LA_ERR) ** 2
    chi2_H0_shoes = ((H0_inferred - H0_SHOES) / H0_SHOES_ERR) ** 2
    chi2_sn = (max_dmu / SN_MAX_DMU) ** 2 if max_dmu > SN_MAX_DMU else 0.0

    # Combined: R + l_a + SH0ES (primary targets)
    chi2_cmb_h0 = chi2_R + chi2_la + chi2_H0_shoes

    # Δr_d / r_d
    drd_pct = (rd_idt - rd_lcdm) / rd_lcdm * 100

    result = {
        'f_dom': f_dom,
        'z_c': z_c,
        'delta_z': delta_z,
        'rd_idt': rd_idt,
        'drd_pct': drd_pct,
        'H0_inferred': H0_inferred,
        'R': R_idt,
        'la': la_idt,
        'max_dmu': max_dmu,
        'chi2_R': chi2_R,
        'chi2_la': chi2_la,
        'chi2_H0': chi2_H0_shoes,
        'chi2_sn': chi2_sn,
        'chi2_total': chi2_cmb_h0 + chi2_sn,
    }

    if verbose:
        print(f"  f_dom={f_dom:.3f}, z_c={z_c:.0f}, Δz={delta_z:.0f}")
        print(f"    Δr_d/r_d = {drd_pct:+.2f}%")
        print(f"    H₀ = {H0_inferred:.2f} km/s/Mpc")
        print(f"    R = {R_idt:.4f} ({(R_idt-R_PLANCK)/R_ERR:+.1f}σ)")
        print(f"    l_a = {la_idt:.3f} ({(la_idt-LA_PLANCK)/LA_ERR:+.1f}σ)")
        print(f"    max|Δμ| = {max_dmu:.4f} mag")
        print(f"    χ²(R+l_a+H₀) = {chi2_cmb_h0:.1f}")

    return result


def run_scan(f_range=(0.01, 0.25, 15),
             zc_range=(500, 5000, 20),
             delta_z_frac=0.3):
    """
    Run a 2D parameter scan over (f_dom, z_c) with fixed Δ_z = frac × z_c.

    Parameters
    ----------
    f_range : tuple
        (min, max, n_points) for f_dom
    zc_range : tuple
        (min, max, n_points) for z_c
    delta_z_frac : float
        Δ_z = delta_z_frac × z_c (fixed ratio)
    """
    f_vals = np.linspace(f_range[0], f_range[1], f_range[2])
    zc_vals = np.linspace(zc_range[0], zc_range[1], zc_range[2])

    print(f"Scanning {len(f_vals)} × {len(zc_vals)} = "
          f"{len(f_vals)*len(zc_vals)} points...")
    print(f"  f_dom: {f_range[0]:.2f} — {f_range[1]:.2f}")
    print(f"  z_c:   {zc_range[0]:.0f} — {zc_range[1]:.0f}")
    print(f"  Δ_z = {delta_z_frac} × z_c")
    print()

    results = []
    total = len(f_vals) * len(zc_vals)

    for i, f in enumerate(f_vals):
        for j, zc in enumerate(zc_vals):
            dz = delta_z_frac * zc
            r = evaluate_point(f, zc, dz)
            if r is not None:
                results.append(r)

            done = i * len(zc_vals) + j + 1
            if done % 50 == 0 or done == total:
                print(f"  {done}/{total} complete", end='\r')

    print(f"\n  {len(results)} valid points evaluated\n")
    return results, f_vals, zc_vals


def plot_scan(results, f_vals, zc_vals, delta_z_frac=0.3):
    """Generate visualization of parameter scan results."""

    # Convert to 2D grids
    nf, nz = len(f_vals), len(zc_vals)

    H0_grid = np.full((nf, nz), np.nan)
    chi2_grid = np.full((nf, nz), np.nan)
    la_sigma_grid = np.full((nf, nz), np.nan)
    R_sigma_grid = np.full((nf, nz), np.nan)
    drd_grid = np.full((nf, nz), np.nan)

    for r in results:
        i = np.argmin(np.abs(f_vals - r['f_dom']))
        j = np.argmin(np.abs(zc_vals - r['z_c']))
        H0_grid[i, j] = r['H0_inferred']
        chi2_grid[i, j] = r['chi2_total']
        la_sigma_grid[i, j] = abs(r['la'] - LA_PLANCK) / LA_ERR
        R_sigma_grid[i, j] = abs(r['R'] - R_PLANCK) / R_ERR
        drd_grid[i, j] = r['drd_pct']

    fig, axes = plt.subplots(2, 3, figsize=(18, 11))
    fig.suptitle(f'IDT Parameter Space Scan (Δ_z = {delta_z_frac}·z_c)',
                 fontsize=14, fontweight='bold')

    ZC, F = np.meshgrid(zc_vals, f_vals)

    # Panel 1: Inferred H₀
    ax = axes[0, 0]
    c = ax.contourf(ZC, F * 100, H0_grid,
                    levels=np.linspace(67, 76, 19), cmap='RdYlBu_r')
    plt.colorbar(c, ax=ax, label='km/s/Mpc')
    ax.contour(ZC, F * 100, H0_grid, levels=[73.04], colors='red',
               linewidths=2, linestyles='--')
    ax.contour(ZC, F * 100, H0_grid, levels=[67.4], colors='blue',
               linewidths=2, linestyles='--')
    ax.set_xlabel('z_c')
    ax.set_ylabel('f_dom [%]')
    ax.set_title('Inferred H₀ (red=SH0ES, blue=Planck)')

    # Panel 2: l_a tension (σ)
    ax = axes[0, 1]
    c = ax.contourf(ZC, F * 100, la_sigma_grid,
                    levels=[0, 1, 2, 3, 5, 10, 20, 50, 100, 200],
                    cmap='YlOrRd')
    plt.colorbar(c, ax=ax, label='σ from Planck')
    ax.contour(ZC, F * 100, la_sigma_grid, levels=[2, 5],
               colors=['green', 'black'], linewidths=2)
    ax.set_xlabel('z_c')
    ax.set_ylabel('f_dom [%]')
    ax.set_title('l_a Tension (green=2σ, black=5σ)')

    # Panel 3: R tension (σ)
    ax = axes[0, 2]
    c = ax.contourf(ZC, F * 100, R_sigma_grid,
                    levels=[0, 0.5, 1, 2, 3, 5, 10], cmap='YlOrRd')
    plt.colorbar(c, ax=ax, label='σ from Planck')
    ax.contour(ZC, F * 100, R_sigma_grid, levels=[2],
               colors='green', linewidths=2)
    ax.set_xlabel('z_c')
    ax.set_ylabel('f_dom [%]')
    ax.set_title('R Tension')

    # Panel 4: Δr_d/r_d
    ax = axes[1, 0]
    c = ax.contourf(ZC, F * 100, drd_grid,
                    levels=np.linspace(-10, 0, 21), cmap='Blues_r')
    plt.colorbar(c, ax=ax, label='%')
    ax.set_xlabel('z_c')
    ax.set_ylabel('f_dom [%]')
    ax.set_title('Sound Horizon Shift Δr_d/r_d')

    # Panel 5: Total χ² (log scale)
    ax = axes[1, 1]
    log_chi2 = np.log10(np.clip(chi2_grid, 1e-1, None))
    c = ax.contourf(ZC, F * 100, log_chi2,
                    levels=np.linspace(-1, 5, 25), cmap='viridis_r')
    plt.colorbar(c, ax=ax, label='log₁₀(χ²)')
    ax.contour(ZC, F * 100, log_chi2, levels=[np.log10(11.3)],
               colors='red', linewidths=2, linestyles='--')
    ax.set_xlabel('z_c')
    ax.set_ylabel('f_dom [%]')
    ax.set_title('Total χ² (red = 3σ for 3 dof)')

    # Panel 6: Best points table
    ax = axes[1, 2]
    ax.axis('off')

    # Find best points by total χ²
    sorted_results = sorted(results, key=lambda r: r['chi2_total'])
    best = sorted_results[:8]

    rows = [['f_dom', 'z_c', 'H₀', 'R(σ)', 'l_a(σ)', 'χ²']]
    for b in best:
        R_sig = abs(b['R'] - R_PLANCK) / R_ERR
        la_sig = abs(b['la'] - LA_PLANCK) / LA_ERR
        rows.append([
            f"{b['f_dom']:.3f}",
            f"{b['z_c']:.0f}",
            f"{b['H0_inferred']:.1f}",
            f"{R_sig:.1f}",
            f"{la_sig:.1f}",
            f"{b['chi2_total']:.1f}",
        ])

    table = ax.table(cellText=rows, loc='center', cellLoc='center',
                     colWidths=[0.14, 0.12, 0.12, 0.12, 0.12, 0.12])
    table.auto_set_font_size(False)
    table.set_fontsize(8)
    table.scale(1, 1.6)
    for j in range(6):
        table[0, j].set_facecolor('#4472C4')
        table[0, j].set_text_props(color='white', fontweight='bold')
    ax.set_title('Best Parameter Points (by χ²)', fontsize=11,
                 fontweight='bold', pad=15)

    plt.tight_layout()
    plt.savefig('idt_parameter_scan.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Saved: idt_parameter_scan.png")


def run_width_scan(f_dom=0.05, z_c=2000,
                   frac_range=(0.05, 0.8, 20)):
    """
    Scan over Δ_z width for a fixed (f_dom, z_c) to understand
    how width affects constraints.
    """
    fracs = np.linspace(frac_range[0], frac_range[1], frac_range[2])

    print(f"Width scan: f_dom={f_dom}, z_c={z_c}")
    print(f"  Δ_z/z_c from {frac_range[0]} to {frac_range[1]}")
    print()

    for frac in fracs:
        dz = frac * z_c
        r = evaluate_point(f_dom, z_c, dz, verbose=True)


if __name__ == "__main__":
    print("=" * 70)
    print("IDT PARAMETER SPACE SCAN")
    print("=" * 70)
    print()

    # Main 2D scan
    results, f_vals, zc_vals = run_scan(
        f_range=(0.005, 0.20, 20),
        zc_range=(500, 6000, 25),
        delta_z_frac=0.3,
    )

    plot_scan(results, f_vals, zc_vals, delta_z_frac=0.3)

    # Print top 10 best points
    print("\n" + "=" * 70)
    print("TOP 10 PARAMETER POINTS (by total χ²)")
    print("=" * 70)

    sorted_results = sorted(results, key=lambda r: r['chi2_total'])
    for i, r in enumerate(sorted_results[:10]):
        R_sig = abs(r['R'] - R_PLANCK) / R_ERR
        la_sig = abs(r['la'] - LA_PLANCK) / LA_ERR
        H0_sig_shoes = abs(r['H0_inferred'] - H0_SHOES) / H0_SHOES_ERR
        print(f"\n  #{i+1}: f_dom={r['f_dom']:.4f}, z_c={r['z_c']:.0f}, "
              f"Δ_z={r['delta_z']:.0f}")
        print(f"      H₀ = {r['H0_inferred']:.2f} ({H0_sig_shoes:.1f}σ from SH0ES)")
        print(f"      R = {r['R']:.4f} ({R_sig:.1f}σ)")
        print(f"      l_a = {r['la']:.3f} ({la_sig:.1f}σ)")
        print(f"      Δr_d/r_d = {r['drd_pct']:+.2f}%")
        print(f"      χ² = {r['chi2_total']:.1f}")

    # Wisdom: what does the scan tell us?
    print("\n" + "=" * 70)
    print("PARAMETER SPACE INSIGHTS")
    print("=" * 70)

    best = sorted_results[0]
    print(f"\n  Best point: f_dom={best['f_dom']:.4f}, z_c={best['z_c']:.0f}")
    print(f"  This achieves χ² = {best['chi2_total']:.1f}")

    # Find best H₀ match
    h0_sorted = sorted(results,
                       key=lambda r: abs(r['H0_inferred'] - H0_SHOES))
    h0_best = h0_sorted[0]
    print(f"\n  Best H₀ match: f_dom={h0_best['f_dom']:.4f}, "
          f"z_c={h0_best['z_c']:.0f}")
    print(f"  H₀ = {h0_best['H0_inferred']:.2f}, but χ² = "
          f"{h0_best['chi2_total']:.1f}")

    # ΛCDM reference
    sp_lcdm = CMB_shift_parameters(H_LCDM)
    chi2_lcdm_h0 = ((67.36 - H0_SHOES) / H0_SHOES_ERR) ** 2
    print(f"\n  ΛCDM reference:")
    print(f"    H₀ = 67.36 ({abs(67.36-H0_SHOES)/H0_SHOES_ERR:.1f}σ from SH0ES)")
    print(f"    R = {sp_lcdm['R']:.4f} "
          f"({abs(sp_lcdm['R']-R_PLANCK)/R_ERR:.1f}σ)")
    print(f"    l_a = {sp_lcdm['l_a']:.3f} "
          f"({abs(sp_lcdm['l_a']-LA_PLANCK)/LA_ERR:.1f}σ)")
    print(f"    χ²(H₀ only) = {chi2_lcdm_h0:.1f}")
