"""
IDT Two-Domain Growth Calculator
==================================
Tests the full IDT picture:
  Early domain (z_c ~ 2000): shifts r_d → H₀
  Late domain (z_c ~ 1): dephasing-driven G_eff → σ₈

Separates three effects:
  1. Background-only (Candidate 1): domain modifies H(z)
  2. Dephasing G_eff (Candidate 2): domain modifies growth coupling
  3. Combined: both channels active

This is the first test of the coherent IDT mechanism for both tensions.
"""

import numpy as np
from scipy.integrate import odeint, quad
import sys, os

# LCDM parameters
H0 = 67.36
Om0 = 0.3153
Or0 = 9.1e-5
OL0 = 1 - Om0 - Or0
C_KM_S = 299792.458


def E2_func(a, domains=None):
    """(H/H0)^2 with optional domain contributions."""
    z = 1.0/a - 1.0
    E2 = Om0/a**3 + Or0/a**4 + OL0
    if domains:
        for f_dom, z_c, sigma_ln in domains:
            if f_dom > 0:
                ln_ratio = np.log((1+z)/(1+z_c))
                sigma2 = sigma_ln**2
                rho_shape = np.exp(-0.5 * ln_ratio**2 / sigma2)
                E2_zc = Om0*(1+z_c)**3 + Or0*(1+z_c)**4 + OL0
                Omega_peak = f_dom / (1-f_dom) * E2_zc
                E2 += Omega_peak * rho_shape
    return E2


def Gamma_dephasing(a, f_dom, z_c, sigma_ln):
    """Dephasing coupling: (d ln rho / d ln a) × rho_shape."""
    if f_dom <= 0:
        return 0
    z = 1.0/a - 1.0
    ln_ratio = np.log((1+z)/(1+z_c))
    sigma2 = sigma_ln**2
    rho_shape = np.exp(-0.5 * ln_ratio**2 / sigma2)
    if rho_shape < 1e-12:
        return 0
    return (ln_ratio / sigma2) * rho_shape


def growth_ode(y, lna, domains, eta0, late_domain_idx):
    """
    Growth equation with optional G_eff modification.

    domains: list of (f_dom, z_c, sigma_ln) for background H(z)
    eta0: dephasing coupling strength
    late_domain_idx: which domain gets the G_eff modification (or -1 for none)
    """
    D, dD = y
    a = np.exp(lna)

    E2_val = E2_func(a, domains)
    if E2_val <= 0:
        return [0, 0]

    # d ln H / d ln a (numerical)
    da = 1e-5
    E2_p = E2_func(a * np.exp(da), domains)
    E2_m = E2_func(a * np.exp(-da), domains)
    dlnH = (np.log(max(E2_p, 1e-30)) - np.log(max(E2_m, 1e-30))) / (4 * da)

    # Omega_m(a)
    Om_a = Om0 / a**3 / E2_val

    # G_eff modification from dephasing
    G_mod = 1.0
    if late_domain_idx >= 0 and eta0 != 0 and domains:
        f, zc, sig = domains[late_domain_idx]
        G_mod = 1.0 + eta0 * Gamma_dephasing(a, f, zc, sig)

    friction = 2 + dlnH
    source = 1.5 * Om_a * G_mod

    return [dD, -friction * dD + source * D]


def compute_growth(domains=None, eta0=0, late_domain_idx=-1):
    """Compute growth factor D(a=1) relative to LCDM."""
    lna = np.linspace(np.log(1e-3), 0, 3000)
    y0 = [1e-3, 1.0]

    sol = odeint(growth_ode, y0, lna,
                 args=(domains, eta0, late_domain_idx))
    return sol[-1, 0]


def compute_rd(domains=None):
    """Sound horizon r_d in Mpc."""
    Omega_b = 0.0493
    Omega_gamma = 5.38e-5
    z_drag = 1059.94

    def H_func(z):
        a = 1.0 / (1+z)
        return H0 * np.sqrt(E2_func(a, domains))

    def integrand(z):
        R_b = 3.0 * Omega_b / (4.0 * Omega_gamma * (1.0 + z))
        c_s = C_KM_S / np.sqrt(3.0 * (1.0 + R_b))
        return c_s / H_func(z)

    result, _ = quad(integrand, z_drag, 1e5, limit=500)
    return result


def main():
    print("=" * 70)
    print("IDT TWO-DOMAIN GROWTH ANALYSIS")
    print("  Separating background vs dephasing contributions")
    print("=" * 70)

    # LCDM reference
    D_lcdm = compute_growth()
    rd_lcdm = compute_rd()
    sig8_lcdm = 0.811
    print(f"\n  ΛCDM: D={D_lcdm:.4f}, r_d={rd_lcdm:.2f} Mpc, σ₈={sig8_lcdm}")

    # Define domains
    early = (0.05, 2000, 0.18)    # r_d shifter
    late = (0.03, 1.0, 0.5)       # σ₈ suppressor
    eta0 = -0.05                   # dephasing coupling

    print(f"\n  Early domain: f={early[0]}, z_c={early[1]}, σ_ln={early[2]}")
    print(f"  Late domain:  f={late[0]}, z_c={late[1]}, σ_ln={late[2]}")
    print(f"  Dephasing η₀ = {eta0}")

    # ============================================================
    # Channel separation
    # ============================================================

    print(f"\n{'='*70}")
    print(f"  CHANNEL SEPARATION")
    print(f"{'='*70}")
    print(f"\n  {'Configuration':<45} {'D/D_ΛCDM':>10} {'σ₈':>8} {'r_d':>8} {'H₀_inf':>8}")

    configs = [
        ("ΛCDM (no domains)",
         None, 0, -1),

        ("Early domain only (background)",
         [early], 0, -1),

        ("Late domain only — background channel",
         [late], 0, -1),

        ("Late domain only — dephasing channel",
         None, eta0, 0),  # No bg contribution, only G_eff
         # NOTE: this doesn't work because G_eff needs the domain defined
         # We need a special case

        ("Late domain — background + dephasing",
         [late], eta0, 0),

        ("Both domains — background only",
         [early, late], 0, -1),

        ("Both domains — early bg + late dephasing only",
         [early], eta0, -1),  # early in bg, late only through G_eff
         # This also needs special handling

        ("FULL IDT: both bg + late dephasing",
         [early, late], eta0, 1),  # late domain is index 1
    ]

    # Compute each configuration
    for name, domains, eta, late_idx in configs:
        try:
            D = compute_growth(domains, eta, late_idx)
            ratio = D / D_lcdm
            sig8 = sig8_lcdm * ratio
            rd = compute_rd(domains)
            H0_inf = H0 * rd_lcdm / rd
            print(f"  {name:<45} {ratio:>10.6f} {sig8:>8.4f} {rd:>8.2f} {H0_inf:>8.2f}")
        except Exception as e:
            print(f"  {name:<45} ERROR: {e}")

    # ============================================================
    # Now do the proper channel separation for late domain
    # ============================================================

    print(f"\n{'='*70}")
    print(f"  LATE DOMAIN: DECOMPOSING BACKGROUND vs DEPHASING")
    print(f"{'='*70}")

    # For the late domain alone:
    D_no_domain = compute_growth(None, 0, -1)
    D_bg_only = compute_growth([late], 0, -1)
    D_bg_plus_dephasing = compute_growth([late], eta0, 0)

    bg_effect = (D_bg_only / D_no_domain - 1)
    total_effect = (D_bg_plus_dephasing / D_no_domain - 1)
    dephasing_effect = total_effect - bg_effect

    print(f"\n  Background-only effect:  Δσ₈/σ₈ = {bg_effect:+.4f}  "
          f"(σ₈ = {sig8_lcdm*(1+bg_effect):.4f})")
    print(f"  Dephasing-only effect:   Δσ₈/σ₈ = {dephasing_effect:+.4f}  "
          f"(additional from G_eff)")
    print(f"  Combined effect:         Δσ₈/σ₈ = {total_effect:+.4f}  "
          f"(σ₈ = {sig8_lcdm*(1+total_effect):.4f})")
    print(f"\n  Fraction from background: {bg_effect/total_effect*100:.1f}%")
    print(f"  Fraction from dephasing:  {dephasing_effect/total_effect*100:.1f}%")

    # ============================================================
    # Full two-domain: early (bg) + late (bg + dephasing)
    # ============================================================

    print(f"\n{'='*70}")
    print(f"  FULL TWO-DOMAIN IDT PICTURE")
    print(f"{'='*70}")

    D_full = compute_growth([early, late], eta0, 1)
    rd_full = compute_rd([early, late])
    sig8_full = sig8_lcdm * D_full / D_lcdm
    H0_inf_full = H0 * rd_lcdm / rd_full

    print(f"\n  Early domain: f={early[0]}, z_c={early[1]}, σ={early[2]}")
    print(f"  Late domain:  f={late[0]}, z_c={late[1]}, σ={late[2]}")
    print(f"  Dephasing:    η₀ = {eta0}")
    print(f"\n  Results:")
    print(f"    H₀ inferred = {H0_inf_full:.2f} km/s/Mpc (ΛCDM: {H0:.2f})")
    print(f"    σ₈          = {sig8_full:.4f} (ΛCDM: {sig8_lcdm})")
    print(f"    r_d          = {rd_full:.2f} Mpc (ΛCDM: {rd_lcdm:.2f})")
    print(f"    ΔH₀          = {H0_inf_full - H0:+.2f} km/s/Mpc")
    print(f"    Δσ₈          = {sig8_full - sig8_lcdm:+.4f}")

    # ============================================================
    # Scan over η₀ for the full two-domain picture
    # ============================================================

    print(f"\n{'='*70}")
    print(f"  η₀ SCAN: FULL TWO-DOMAIN")
    print(f"{'='*70}")
    print(f"\n  Early: {early}, Late: {late}")
    print(f"\n  {'η₀':>8} {'σ₈':>8} {'H₀_inf':>8} {'Δσ₈':>8} {'ΔH₀':>8}")

    for eta in [0, -0.01, -0.02, -0.03, -0.05, -0.07, -0.10,
                -0.12, -0.15, -0.20]:
        D = compute_growth([early, late], eta, 1)
        rd = compute_rd([early, late])
        sig8 = sig8_lcdm * D / D_lcdm
        H0_inf = H0 * rd_lcdm / rd
        flag = ' ★' if (sig8 < 0.80 and H0_inf > 67.8) else ''
        print(f"  {eta:>+8.3f} {sig8:>8.4f} {H0_inf:>8.2f} "
              f"{sig8-sig8_lcdm:>+8.4f} {H0_inf-H0:>+8.2f}{flag}")

    # ============================================================
    # Scan late domain strength at fixed η₀
    # ============================================================

    print(f"\n{'='*70}")
    print(f"  LATE DOMAIN STRENGTH SCAN (η₀ = {eta0})")
    print(f"{'='*70}")
    print(f"\n  {'f_late':>8} {'σ₈':>8} {'H₀_inf':>8} {'Δσ₈':>8}")

    for f_late in [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08]:
        late_var = (f_late, 1.0, 0.5)
        D = compute_growth([early, late_var], eta0, 1)
        rd = compute_rd([early, late_var])
        sig8 = sig8_lcdm * D / D_lcdm
        H0_inf = H0 * rd_lcdm / rd
        flag = ' ★' if sig8 < 0.80 else ''
        print(f"  {f_late:>8.3f} {sig8:>8.4f} {H0_inf:>8.2f} "
              f"{sig8-sig8_lcdm:>+8.4f}{flag}")


if __name__ == "__main__":
    main()
