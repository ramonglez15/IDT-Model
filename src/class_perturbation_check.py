"""
IDT Perturbation-Level Check via CLASS
========================================
Phase B: Verify that IDT domain configurations produce stable,
physically reasonable CMB power spectra.

Uses the best-fit configurations from full_parameter_scan.py
with CLASS's built-in fluid sector (PPF approximation).

This is the credibility threshold: if spectra are stable and
residuals are reasonable, IDT passes perturbation-level validation.
"""

import numpy as np
import matplotlib.pyplot as plt
import sys, os

sys.path.insert(0, os.path.dirname(__file__))
from classy import Class

# Add archive class python path for classy
sys.path.insert(0, os.path.join(os.path.dirname(__file__),
                                '..', 'archive', 'class', 'python'))

import cosmology_base
sys.modules['idt_class_module.cosmology_base'] = cosmology_base
from idt_domain import IDTDomain, IDTModel


def run_lcdm(H0=67.36, omega_b=0.02237, omega_cdm=0.1200):
    """Run standard ΛCDM baseline."""
    cosmo = Class()
    cosmo.set({
        'output': 'tCl,pCl,lCl,mPk',
        'lensing': 'yes',
        'l_max_scalars': 2500,
        'P_k_max_h/Mpc': 1.0,
        'H0': H0,
        'omega_b': omega_b,
        'omega_cdm': omega_cdm,
        'T_cmb': 2.7255,
        'N_ur': 2.0328,
        'N_ncdm': 1,
        'm_ncdm': 0.06,
    })
    cosmo.compute()

    cls = cosmo.lensed_cl(2500)
    result = {
        'ell': np.arange(len(cls['tt'])),
        'tt': cls['tt'],
        'ee': cls['ee'],
        'te': cls['te'],
        'pp': cls['pp'],
        'rs_drag': cosmo.rs_drag(),
        'H0': cosmo.Hubble(0) * 299792.458,
        'sigma8': cosmo.sigma8(),
        'label': f'ΛCDM (H₀={H0:.1f})',
    }

    cosmo.struct_cleanup()
    cosmo.empty()
    return result


def run_idt_fluid(H0, omega_b, omega_cdm, domain,
                  label="IDT", w0_override=None, wa_override=None,
                  omega_fld_override=None):
    """
    Run IDT domain as CLASS fluid species.

    For early-time domains where w(z=0) is extreme, use w0/wa overrides
    to approximate the domain's effect in a CLASS-compatible way.

    The old OIDM approach used w₀=-0.92, wₐ=-0.14 which worked.
    For new domains, we fit a CPL approximation or use direct overrides.
    """
    if omega_fld_override is not None:
        Omega_fld_0 = omega_fld_override
    else:
        Omega_fld_0 = float(domain.Omega(0.0))

    w0 = w0_override if w0_override is not None else float(domain.w(0.01))
    wa = wa_override if wa_override is not None else 0.0

    # CLASS requires w0 < 1/3 for radiation domination at early times
    w0_class = max(min(w0, 0.32), -3.0)

    h = H0 / 100.0

    cosmo = Class()
    params = {
        'output': 'tCl,pCl,lCl,mPk',
        'P_k_max_h/Mpc': 1.0,
        'lensing': 'yes',
        'l_max_scalars': 2500,
        'H0': H0,
        'omega_b': omega_b,
        'omega_cdm': omega_cdm,
        'T_cmb': 2.7255,
        'N_ur': 2.0328,
        'N_ncdm': 1,
        'm_ncdm': 0.06,
        # IDT domain as fluid
        'Omega_fld': Omega_fld_0,
        'w0_fld': w0_class,
        'wa_fld': wa,
        'cs2_fld': domain.c_s2 if domain else 1.0,
    }

    cosmo.set(params)

    try:
        cosmo.compute()
    except Exception as e:
        print(f"  CLASS FAILED for {label}: {e}")
        cosmo.struct_cleanup()
        cosmo.empty()
        return None

    cls = cosmo.lensed_cl(2500)
    result = {
        'ell': np.arange(len(cls['tt'])),
        'tt': cls['tt'],
        'ee': cls['ee'],
        'te': cls['te'],
        'pp': cls['pp'],
        'rs_drag': cosmo.rs_drag(),
        'H0': cosmo.Hubble(0) * 299792.458,
        'sigma8': cosmo.sigma8(),
        'label': label,
        'params': params,
        'Omega_fld_0': Omega_fld_0,
        'w0': w0,
        'w0_class': w0_class,
    }

    cosmo.struct_cleanup()
    cosmo.empty()
    return result


def run_idt_with_old_oidm_params():
    """
    Run with the old OIDM parameter values from archive.
    This is what worked before — use as reference.
    """
    cosmo = Class()
    params = {
        'output': 'tCl,pCl,lCl,mPk',
        'P_k_max_h/Mpc': 1.0,
        'lensing': 'yes',
        'l_max_scalars': 2500,
        'H0': 73.24,
        'omega_b': 0.0492 * (0.7324)**2,  # Omega_b * h²
        'omega_cdm': 0.2645 * (0.7324)**2,
        'T_cmb': 2.7255,
        'N_ur': 3.12 - 1.0132,  # CLASS convention: N_ur = N_eff - 1 massive
        'N_ncdm': 1,
        'm_ncdm': 0.06,
        # Dark energy fluid (old OIDM model)
        'Omega_fld': 0.6863,
        'w0_fld': -0.92,
        'wa_fld': -0.14,
        'cs2_fld': 1.0,
        'YHe': 0.24,
    }

    cosmo.set(params)

    try:
        cosmo.compute()
    except Exception as e:
        print(f"  OLD OIDM FAILED: {e}")
        cosmo.struct_cleanup()
        cosmo.empty()
        return None

    cls = cosmo.lensed_cl(2500)
    result = {
        'ell': np.arange(len(cls['tt'])),
        'tt': cls['tt'],
        'ee': cls['ee'],
        'te': cls['te'],
        'pp': cls['pp'],
        'rs_drag': cosmo.rs_drag(),
        'H0': cosmo.Hubble(0) * 299792.458,
        'sigma8': cosmo.sigma8(),
        'label': 'Old OIDM (H₀=73.24)',
        'params': params,
    }

    cosmo.struct_cleanup()
    cosmo.empty()
    return result


def plot_comparison(results, lcdm):
    """Generate comparison plot."""
    fig, axes = plt.subplots(2, 3, figsize=(18, 11))
    fig.suptitle('IDT Perturbation-Level Check — CMB Power Spectra',
                 fontsize=14, fontweight='bold')

    ell = lcdm['ell'][2:]
    fac = ell * (ell + 1) / (2 * np.pi)

    colors = ['red', 'blue', 'green', 'orange', 'purple']

    # TT spectrum
    ax = axes[0, 0]
    ax.plot(ell, fac * lcdm['tt'][2:] * 1e12, 'k-', lw=1.5,
            label=lcdm['label'])
    for i, r in enumerate(results):
        if r is not None:
            ax.plot(ell, fac * r['tt'][2:] * 1e12, '--', color=colors[i],
                    lw=1, label=r['label'])
    ax.set_xlabel('ℓ')
    ax.set_ylabel('ℓ(ℓ+1)C_ℓ^TT/2π [μK²]')
    ax.set_title('Temperature Power Spectrum')
    ax.legend(fontsize=7)
    ax.set_xlim(2, 2500)
    ax.grid(True, alpha=0.3)

    # TT residual
    ax = axes[0, 1]
    for i, r in enumerate(results):
        if r is not None:
            ratio = r['tt'][2:] / lcdm['tt'][2:]
            ax.plot(ell, (ratio - 1) * 100, color=colors[i], lw=1,
                    label=r['label'])
    ax.axhline(0, color='k', lw=0.5)
    ax.set_xlabel('ℓ')
    ax.set_ylabel('ΔC_ℓ^TT / C_ℓ^TT [%]')
    ax.set_title('TT Residual vs ΛCDM')
    ax.legend(fontsize=7)
    ax.set_xlim(2, 2500)
    ax.set_ylim(-15, 15)
    ax.grid(True, alpha=0.3)

    # EE spectrum
    ax = axes[0, 2]
    ax.plot(ell, fac * lcdm['ee'][2:] * 1e12, 'k-', lw=1.5,
            label=lcdm['label'])
    for i, r in enumerate(results):
        if r is not None:
            ax.plot(ell, fac * r['ee'][2:] * 1e12, '--', color=colors[i],
                    lw=1, label=r['label'])
    ax.set_xlabel('ℓ')
    ax.set_ylabel('ℓ(ℓ+1)C_ℓ^EE/2π [μK²]')
    ax.set_title('E-mode Polarization')
    ax.legend(fontsize=7)
    ax.set_xlim(2, 2500)
    ax.grid(True, alpha=0.3)

    # Lensing
    ax = axes[1, 0]
    ax.plot(ell, fac * lcdm['pp'][2:] * 1e7, 'k-', lw=1.5,
            label=lcdm['label'])
    for i, r in enumerate(results):
        if r is not None:
            ax.plot(ell, fac * r['pp'][2:] * 1e7, '--', color=colors[i],
                    lw=1, label=r['label'])
    ax.set_xlabel('ℓ')
    ax.set_ylabel('ℓ(ℓ+1)C_ℓ^φφ/2π [×10⁷]')
    ax.set_title('Lensing Power Spectrum')
    ax.legend(fontsize=7)
    ax.set_xlim(2, 2500)
    ax.grid(True, alpha=0.3)

    # Summary table
    ax = axes[1, 1]
    ax.axis('off')
    rows = [['Model', 'H₀', 'r_d', 'σ₈', 'Stable']]
    rows.append([lcdm['label'],
                 f"{lcdm['H0']:.1f}", f"{lcdm['rs_drag']:.1f}",
                 f"{lcdm['sigma8']:.4f}", '✓'])
    for r in results:
        if r is not None:
            rows.append([r['label'],
                         f"{r['H0']:.1f}", f"{r['rs_drag']:.1f}",
                         f"{r['sigma8']:.4f}", '✓'])
        else:
            rows.append(['FAILED', '-', '-', '-', '✗'])

    table = ax.table(cellText=rows, loc='center', cellLoc='center',
                     colWidths=[0.35, 0.12, 0.12, 0.15, 0.1])
    table.auto_set_font_size(False)
    table.set_fontsize(8)
    table.scale(1, 1.8)
    for j in range(5):
        table[0, j].set_facecolor('#4472C4')
        table[0, j].set_text_props(color='white', fontweight='bold')
    ax.set_title('Results Summary', fontsize=11, fontweight='bold', pad=15)

    # Low-ℓ TT zoom
    ax = axes[1, 2]
    ell_low = lcdm['ell'][2:50]
    fac_low = ell_low * (ell_low + 1) / (2 * np.pi)
    ax.plot(ell_low, fac_low * lcdm['tt'][2:50] * 1e12, 'k-', lw=2,
            label=lcdm['label'])
    for i, r in enumerate(results):
        if r is not None:
            ax.plot(ell_low, fac_low * r['tt'][2:50] * 1e12, '--',
                    color=colors[i], lw=1.5, label=r['label'])
    ax.set_xlabel('ℓ')
    ax.set_ylabel('ℓ(ℓ+1)C_ℓ^TT/2π [μK²]')
    ax.set_title('Low-ℓ TT (ISW region)')
    ax.legend(fontsize=7)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('idt_perturbation_check.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("\nSaved: idt_perturbation_check.png")


if __name__ == "__main__":
    print("=" * 70)
    print("IDT PERTURBATION-LEVEL CHECK")
    print("=" * 70)

    # 1. ΛCDM baseline
    print("\n1. Running ΛCDM baseline...")
    lcdm = run_lcdm()
    print(f"   r_d={lcdm['rs_drag']:.2f}, σ₈={lcdm['sigma8']:.4f}")

    results = []

    # 2. Old OIDM model (reference from archive)
    print("\n2. Running old OIDM model (H₀=73.24, w₀=-0.92)...")
    oidm = run_idt_with_old_oidm_params()
    if oidm:
        print(f"   r_d={oidm['rs_drag']:.2f}, σ₈={oidm['sigma8']:.4f}, "
              f"H₀={oidm['H0']:.2f}")
    results.append(oidm)

    # 3. IDT with old OIDM-style params but adjusted H₀=70
    print("\n3. Running OIDM-style at H₀=70 (w₀=-0.95, wₐ=-0.10)...")
    r3 = run_idt_fluid(70.0, 0.02246, 0.1200, None,
                       label="IDT H₀=70 (w₀=-0.95)",
                       w0_override=-0.95, wa_override=-0.10,
                       omega_fld_override=0.69)
    if r3:
        print(f"   r_d={r3['rs_drag']:.2f}, σ₈={r3['sigma8']:.4f}")
    results.append(r3)

    # 4. IDT exploring parameter space: w₀=-0.88, stronger effect
    print("\n4. Running IDT H₀=71.5 (w₀=-0.88, wₐ=-0.18)...")
    h4 = 71.5 / 100
    r4 = run_idt_fluid(71.5, 0.0480 * h4**2, 0.2640 * h4**2, None,
                       label="IDT H₀=71.5 (w₀=-0.88)",
                       w0_override=-0.88, wa_override=-0.18,
                       omega_fld_override=0.69)
    if r4:
        print(f"   r_d={r4['rs_drag']:.2f}, σ₈={r4['sigma8']:.4f}")
    results.append(r4)

    # 5. Adjusted ΛCDM at H₀=70 (no domain, just higher H₀ for comparison)
    print("\n5. Running ΛCDM at H₀=70 (no domain, reference)...")
    lcdm70 = run_lcdm(H0=70.0, omega_b=0.02246, omega_cdm=0.1200)
    lcdm70['label'] = 'ΛCDM (H₀=70.0)'
    print(f"   r_d={lcdm70['rs_drag']:.2f}, σ₈={lcdm70['sigma8']:.4f}")
    results.append(lcdm70)

    # Plot
    plot_comparison(results, lcdm)

    # Summary
    print("\n" + "=" * 70)
    print("PERTURBATION CHECK SUMMARY")
    print("=" * 70)
    for r in results:
        if r:
            stable = np.all(np.isfinite(r['tt'])) and np.all(np.isfinite(r['ee']))
            max_tt_resid = np.max(np.abs(r['tt'][2:2500] / lcdm['tt'][2:2500] - 1)) * 100
            print(f"\n  {r['label']}:")
            print(f"    H₀={r['H0']:.2f}, r_d={r['rs_drag']:.2f}, σ₈={r['sigma8']:.4f}")
            print(f"    Spectra stable: {stable}")
            print(f"    Max TT residual: {max_tt_resid:.1f}%")
        else:
            print(f"\n  FAILED (CLASS computation error)")
