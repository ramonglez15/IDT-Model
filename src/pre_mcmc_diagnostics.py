"""
Pre-MCMC Diagnostics
=====================
Address the review concerns before full MCMC:

1. WHERE are the TT residuals? (ℓ range, peak vs damping tail)
2. σ₈ direction: does IDT increase or decrease σ₈ with H₀?
3. Grid scan over (w₀, wₐ, H₀) to map constraint intersection
4. Document CPL ↔ IDT parameter mapping
"""

import numpy as np
import matplotlib.pyplot as plt
import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__),
                                '..', 'archive', 'class', 'python'))
from classy import Class

C_KM_S = 299792.458


def run_model(H0, obh2, ocdmh2, w0=-1.0, wa=0.0, Omega_fld=0.0,
              label=""):
    """Run CLASS and return full spectra + observables."""
    cosmo = Class()
    params = {
        'output': 'tCl,pCl,lCl,mPk',
        'lensing': 'yes',
        'l_max_scalars': 2500,
        'P_k_max_h/Mpc': 1.0,
        'H0': H0, 'omega_b': obh2, 'omega_cdm': ocdmh2,
        'T_cmb': 2.7255, 'N_ur': 2.0328, 'N_ncdm': 1, 'm_ncdm': 0.06,
    }
    if Omega_fld > 0:
        params['Omega_fld'] = Omega_fld
        params['w0_fld'] = w0
        params['wa_fld'] = wa
        params['cs2_fld'] = 1.0

    cosmo.set(params)
    try:
        cosmo.compute()
    except Exception as e:
        print(f"  FAILED ({label}): {e}")
        cosmo.struct_cleanup()
        cosmo.empty()
        return None

    cls = cosmo.lensed_cl(2500)
    h = H0 / 100
    Omega_m = (obh2 + ocdmh2) / h**2

    da_star = cosmo.angular_distance(1089.92)
    dc_star = da_star * (1 + 1089.92)
    R = np.sqrt(Omega_m) * H0 / C_KM_S * dc_star
    la = np.pi * dc_star / cosmo.rs_drag()

    result = {
        'label': label, 'H0': H0, 'w0': w0, 'wa': wa,
        'Omega_fld': Omega_fld,
        'ell': np.arange(len(cls['tt'])),
        'tt': cls['tt'], 'ee': cls['ee'], 'pp': cls['pp'],
        'rs_drag': cosmo.rs_drag(),
        'sigma8': cosmo.sigma8(),
        'R': R, 'la': la,
        'Omega_m': Omega_m,
    }
    cosmo.struct_cleanup()
    cosmo.empty()
    return result


# ============================================================
# 1. WHERE are the TT residuals?
# ============================================================

def diagnose_residuals():
    """Map residuals by ℓ range to understand which data constrains what."""
    print("=" * 70)
    print("1. TT RESIDUAL ANATOMY")
    print("=" * 70)

    lcdm = run_model(67.36, 0.02237, 0.1200, label="ΛCDM")

    configs = [
        (70.0,  0.02246, 0.1200, -0.95, -0.10, 0.69,  "IDT H₀=70"),
        (71.5,  0.02246, 0.1270, -0.88, -0.18, 0.69,  "IDT H₀=71.5"),
        (73.24, 0.02641, 0.1420, -0.92, -0.14, 0.6863,"Old OIDM"),
    ]

    results = []
    for H0, ob, ocdm, w0, wa, ofld, label in configs:
        r = run_model(H0, ob, ocdm, w0, wa, ofld, label)
        if r:
            results.append(r)

    # Analyze residuals by ℓ range
    ell_ranges = [
        (2, 30, "ISW/Sachs-Wolfe"),
        (30, 100, "Low-ℓ transition"),
        (100, 300, "1st peak region"),
        (300, 600, "2nd-3rd peaks"),
        (600, 1200, "Damping tail onset"),
        (1200, 2500, "Deep damping tail"),
    ]

    print(f"\n  {'Model':<20} ", end="")
    for lo, hi, name in ell_ranges:
        print(f"{'ℓ='+str(lo)+'-'+str(hi):>14}", end="")
    print(f"  {'Max':>6}  {'RMS':>6}")

    for r in results:
        ratio = r['tt'][2:2500] / lcdm['tt'][2:2500]
        resid = (ratio - 1) * 100  # percent

        print(f"  {r['label']:<20} ", end="")
        for lo, hi, _ in ell_ranges:
            seg = resid[lo-2:hi-2]
            rms = np.sqrt(np.mean(seg**2))
            print(f"{rms:>13.1f}%", end="")

        print(f"  {np.max(np.abs(resid)):>5.1f}%  "
              f"{np.sqrt(np.mean(resid**2)):>5.1f}%")

    # Plot
    fig, axes = plt.subplots(2, 2, figsize=(16, 10))
    fig.suptitle('TT Residual Anatomy — Where IDT Deviates from ΛCDM',
                 fontsize=14, fontweight='bold')

    ell = lcdm['ell'][2:2500]
    fac = ell * (ell + 1) / (2 * np.pi)
    colors = ['red', 'blue', 'green']

    # Full residual
    ax = axes[0, 0]
    for i, r in enumerate(results):
        resid = (r['tt'][2:2500] / lcdm['tt'][2:2500] - 1) * 100
        ax.plot(ell, resid, color=colors[i], lw=0.8, label=r['label'])
    ax.axhline(0, color='k', lw=0.5)
    ax.set_xlabel('ℓ')
    ax.set_ylabel('ΔC_ℓ^TT / C_ℓ^TT [%]')
    ax.set_title('Full TT Residual')
    ax.legend(fontsize=8)
    ax.set_xlim(2, 2500)
    ax.grid(True, alpha=0.3)

    # Zoom on peaks
    ax = axes[0, 1]
    for i, r in enumerate(results):
        resid = (r['tt'][2:2500] / lcdm['tt'][2:2500] - 1) * 100
        ax.plot(ell, resid, color=colors[i], lw=1, label=r['label'])
    ax.axhline(0, color='k', lw=0.5)
    ax.set_xlabel('ℓ')
    ax.set_ylabel('ΔC_ℓ^TT [%]')
    ax.set_title('Peak Region (ℓ = 100-800)')
    ax.set_xlim(100, 800)
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)

    # Running RMS
    ax = axes[1, 0]
    window = 50
    for i, r in enumerate(results):
        resid = (r['tt'][2:2500] / lcdm['tt'][2:2500] - 1) * 100
        rms = np.array([np.sqrt(np.mean(resid[max(0,j-window):j+window]**2))
                        for j in range(len(resid))])
        ax.plot(ell, rms, color=colors[i], lw=1, label=r['label'])
    ax.set_xlabel('ℓ')
    ax.set_ylabel('Running RMS [%]')
    ax.set_title(f'Running RMS (window={window})')
    ax.legend(fontsize=8)
    ax.set_xlim(2, 2500)
    ax.grid(True, alpha=0.3)

    # Spectra overlay at peaks
    ax = axes[1, 1]
    ax.plot(ell, fac * lcdm['tt'][2:2500] * 1e12, 'k-', lw=2,
            label='ΛCDM', alpha=0.7)
    for i, r in enumerate(results):
        ax.plot(ell, fac * r['tt'][2:2500] * 1e12, '--', color=colors[i],
                lw=1, label=r['label'])
    ax.set_xlabel('ℓ')
    ax.set_ylabel('ℓ(ℓ+1)C_ℓ^TT/2π [μK²]')
    ax.set_title('TT Spectra (peak region)')
    ax.set_xlim(100, 1200)
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('idt_residual_anatomy.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("\n  Saved: idt_residual_anatomy.png")

    return results


# ============================================================
# 2. σ₈ DIRECTION — does IDT help or hurt S₈ tension?
# ============================================================

def diagnose_sigma8():
    """
    Systematic scan of σ₈ vs w₀, wₐ, H₀ to understand
    whether IDT can lower σ₈ (desired) or only raises it.
    """
    print("\n" + "=" * 70)
    print("2. σ₈ RESPONSE TO IDT PARAMETERS")
    print("=" * 70)

    # Scan w₀ at fixed H₀=70
    print("\n  σ₈ vs w₀ (H₀=70, wₐ=0, Ω_fld=0.69):")
    w0_vals = [-1.3, -1.2, -1.1, -1.0, -0.9, -0.8, -0.7]
    for w0 in w0_vals:
        r = run_model(70.0, 0.02246, 0.1200, w0, 0.0, 0.69, f"w₀={w0}")
        if r:
            print(f"    w₀={w0:+.2f}: σ₈={r['sigma8']:.4f}  "
                  f"r_d={r['rs_drag']:.1f}  R={r['R']:.4f}")

    # Scan wₐ at fixed w₀=-1.0
    print("\n  σ₈ vs wₐ (H₀=70, w₀=-1.0, Ω_fld=0.69):")
    wa_vals = [-0.5, -0.3, -0.1, 0.0, 0.1, 0.3, 0.5]
    for wa in wa_vals:
        r = run_model(70.0, 0.02246, 0.1200, -1.0, wa, 0.69, f"wₐ={wa}")
        if r:
            print(f"    wₐ={wa:+.2f}: σ₈={r['sigma8']:.4f}  "
                  f"r_d={r['rs_drag']:.1f}")

    # Scan H₀ at fixed w₀=-0.92 (old OIDM value)
    print("\n  σ₈ vs H₀ (w₀=-0.92, wₐ=-0.14, Ω_fld=0.69):")
    h0_vals = [67, 68, 69, 70, 71, 72, 73]
    for h0 in h0_vals:
        h = h0 / 100
        r = run_model(h0, 0.02237, 0.1200, -0.92, -0.14, 0.69, f"H₀={h0}")
        if r:
            print(f"    H₀={h0}: σ₈={r['sigma8']:.4f}  "
                  f"r_d={r['rs_drag']:.1f}")

    # The key question: can we get BOTH higher H₀ AND lower σ₈?
    print("\n  Can we get H₀>70 AND σ₈<0.81? Scanning w₀ < -1 (phantom):")
    for w0 in [-1.3, -1.4, -1.5]:
        for wa in [0.0, 0.2, 0.4]:
            r = run_model(71.0, 0.02240, 0.1180, w0, wa, 0.72,
                          f"w₀={w0},wₐ={wa}")
            if r:
                flag = " ★" if r['sigma8'] < 0.81 else ""
                print(f"    w₀={w0:+.1f} wₐ={wa:+.1f}: "
                      f"σ₈={r['sigma8']:.4f}  H₀={r['H0']:.1f}  "
                      f"R={r['R']:.4f}  l_a={r['la']:.1f}{flag}")


# ============================================================
# 3. GRID SCAN over (w₀, wₐ, H₀)
# ============================================================

def grid_scan():
    """
    Quick grid scan to map where constraints intersect
    before committing to MCMC.
    """
    print("\n" + "=" * 70)
    print("3. GRID SCAN — CONSTRAINT INTERSECTION MAP")
    print("=" * 70)

    # Observational targets
    R_OBS = 1.7502;  R_ERR = 0.0046
    LA_OBS = 301.471;  LA_ERR = 0.090
    H0_OBS = 73.04;  H0_ERR = 1.04

    H0_vals = np.linspace(68, 74, 7)
    w0_vals = np.linspace(-1.4, -0.7, 8)

    print(f"\n  Grid: {len(H0_vals)} H₀ × {len(w0_vals)} w₀ = "
          f"{len(H0_vals)*len(w0_vals)} points")
    print(f"  Fixed: wₐ=-0.14, Ω_fld=0.69, ω_bh²=0.02237, ω_cdmh²=0.1200\n")

    results = []
    for h0 in H0_vals:
        for w0 in w0_vals:
            r = run_model(h0, 0.02237, 0.1200, w0, -0.14, 0.69,
                          f"H₀={h0:.0f},w₀={w0:.2f}")
            if r:
                chi2_R = ((r['R'] - R_OBS) / R_ERR)**2
                chi2_la = ((r['la'] - LA_OBS) / LA_ERR)**2
                chi2_H0 = ((r['H0'] - H0_OBS) / H0_ERR)**2
                r['chi2_cmb'] = chi2_R + chi2_la
                r['chi2_H0'] = chi2_H0
                r['chi2_total'] = chi2_R + chi2_la + chi2_H0
                results.append(r)

    # Print best points
    results.sort(key=lambda r: r['chi2_total'])
    print(f"  Top 10 grid points (by combined χ²):\n")
    print(f"  {'H₀':>5} {'w₀':>6} {'σ₈':>6} {'R':>7} {'R(σ)':>5} "
          f"{'l_a':>8} {'l_a(σ)':>6} {'χ²_CMB':>7} {'χ²_H₀':>6} {'χ²_tot':>7}")
    for r in results[:10]:
        R_sig = abs(r['R'] - R_OBS) / R_ERR
        la_sig = abs(r['la'] - LA_OBS) / LA_ERR
        print(f"  {r['H0']:>5.1f} {r['w0']:>6.2f} {r['sigma8']:>6.4f} "
              f"{r['R']:>7.4f} {R_sig:>5.1f} "
              f"{r['la']:>8.3f} {la_sig:>6.1f} "
              f"{r['chi2_cmb']:>7.1f} {r['chi2_H0']:>6.1f} {r['chi2_total']:>7.1f}")

    return results


if __name__ == "__main__":
    print("=" * 70)
    print("IDT PRE-MCMC DIAGNOSTICS")
    print("=" * 70)

    diagnose_residuals()
    diagnose_sigma8()
    grid_scan()
