"""
Generate all figures for IDT Paper 1.
=====================================
Figures referenced in IDT_Paper1_Outline_v2.md:
  1. Domain energy density profiles (early + late) vs redshift
  2. w(z) for both domains showing conservation + phantom crossing
  3. H(z) fractional deviation from ΛCDM
  4. Channel decomposition: background vs dephasing
  5. η₀ robustness: ΔAIC vs η₀
  6. f_early robustness: ΔAIC vs f_early (with H₀ and σ₈ tracks)
  7. Model comparison table (rendered as figure)
  8. Channel independence: domain ON/OFF combinations
"""

import sys, os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'archive', 'class', 'python'))

# IDT domain functions (standalone, no CLASS needed for profile plots)
sys.path.insert(0, os.path.dirname(__file__))
import cosmology_base
sys.modules['idt_class_module.cosmology_base'] = cosmology_base
from idt_domain import IDTDomain

OUTDIR = os.path.join(os.path.dirname(__file__), 'figures')
os.makedirs(OUTDIR, exist_ok=True)

# Common style
plt.rcParams.update({
    'font.size': 10,
    'axes.labelsize': 11,
    'legend.fontsize': 8,
    'figure.dpi': 150,
    'savefig.bbox': 'tight',
    'savefig.dpi': 300,
})


def fig1_domain_profiles():
    """Domain energy density profiles vs redshift."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))

    z = np.logspace(-2, 4, 2000)

    # Early domain
    d_early = IDTDomain(f_dom=0.035, z_c=2000, delta_z=0.18*(1+2000))
    omega_early = d_early.Omega(z)
    E2 = cosmology_base.E2_LCDM(z)
    frac_early = np.where(E2 > 0, omega_early / (E2 + omega_early) * 100, 0)

    ax1.plot(z, frac_early, 'b-', lw=2)
    ax1.axvline(1060, color='gray', ls='--', alpha=0.5, label='$z_{\\rm drag}$')
    ax1.set_xscale('log')
    ax1.set_xlabel('$z$')
    ax1.set_ylabel('$\\rho_{\\rm dom}/\\rho_{\\rm tot}$ [\\%]')
    ax1.set_title('Early domain ($z_c = 2000$, $\\sigma_{\\ln} = 0.18$)')
    ax1.set_xlim(100, 10000)
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # Late domain
    d_late = IDTDomain(f_dom=0.03, z_c=1.0, delta_z=0.5*(1+1.0))
    omega_late = d_late.Omega(z)
    frac_late = np.where(E2 > 0, omega_late / (E2 + omega_late) * 100, 0)

    ax2.plot(z, frac_late, 'r-', lw=2)
    ax2.set_xscale('log')
    ax2.set_xlabel('$z$')
    ax2.set_ylabel('$\\rho_{\\rm dom}/\\rho_{\\rm tot}$ [\\%]')
    ax2.set_title('Late domain ($z_c = 1.0$, $\\sigma_{\\ln} = 0.5$)')
    ax2.set_xlim(0.01, 100)
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(os.path.join(OUTDIR, 'fig1_domain_profiles.pdf'))
    plt.savefig(os.path.join(OUTDIR, 'fig1_domain_profiles.png'))
    plt.close()
    print('  Fig 1: domain profiles')


def fig2_equation_of_state():
    """w(z) for both domains."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))

    # Early domain w(z)
    d_early = IDTDomain(f_dom=0.035, z_c=2000, delta_z=0.18*(1+2000))
    z_e = np.linspace(1000, 3500, 500)
    w_e = d_early.w(z_e)
    ax1.plot(z_e, w_e, 'b-', lw=2)
    ax1.axhline(-1, color='k', ls=':', lw=0.8, label='$w = -1$')
    ax1.axvline(2000, color='gray', ls='--', alpha=0.5, label='$z_c$')
    ax1.set_xlabel('$z$')
    ax1.set_ylabel('$w(z)$')
    ax1.set_title('Early domain')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    ax1.set_ylim(-2.5, 0.5)

    # Late domain w(z)
    d_late = IDTDomain(f_dom=0.03, z_c=1.0, delta_z=0.5*(1+1.0))
    z_l = np.linspace(0.05, 5, 500)
    w_l = d_late.w(z_l)
    ax2.plot(z_l, w_l, 'r-', lw=2)
    ax2.axhline(-1, color='k', ls=':', lw=0.8, label='$w = -1$')
    ax2.axvline(1.0, color='gray', ls='--', alpha=0.5, label='$z_c$')
    ax2.fill_between(z_l, -1, w_l, where=(w_l > -1), alpha=0.15, color='blue',
                     label='Quintessence ($w > -1$)')
    ax2.fill_between(z_l, -1, w_l, where=(w_l < -1), alpha=0.15, color='red',
                     label='Phantom ($w < -1$)')
    ax2.set_xlabel('$z$')
    ax2.set_ylabel('$w(z)$')
    ax2.set_title('Late domain')
    ax2.legend(fontsize=7)
    ax2.grid(True, alpha=0.3)
    ax2.set_ylim(-3, 1)

    plt.tight_layout()
    plt.savefig(os.path.join(OUTDIR, 'fig2_equation_of_state.pdf'))
    plt.savefig(os.path.join(OUTDIR, 'fig2_equation_of_state.png'))
    plt.close()
    print('  Fig 2: equation of state')


def fig3_Hz_deviation():
    """H(z) fractional deviation from ΛCDM."""
    fig, ax = plt.subplots(figsize=(7, 4.5))

    z = np.logspace(-2, 4, 2000)

    H_lcdm = cosmology_base.H_LCDM(z)

    # Early domain only
    d_early = IDTDomain(f_dom=0.035, z_c=2000, delta_z=0.18*(1+2000))
    from idt_domain import IDTModel
    m_early = IDTModel(domains=[d_early])
    H_early = m_early.H(z)
    dH_early = (H_early - H_lcdm) / H_lcdm * 100

    # Late domain only
    d_late = IDTDomain(f_dom=0.03, z_c=1.0, delta_z=0.5*(1+1.0))
    m_late = IDTModel(domains=[d_late])
    H_late = m_late.H(z)
    dH_late = (H_late - H_lcdm) / H_lcdm * 100

    # Both
    m_both = IDTModel(domains=[d_early, d_late])
    H_both = m_both.H(z)
    dH_both = (H_both - H_lcdm) / H_lcdm * 100

    ax.plot(z, dH_early, 'b-', lw=1.5, label='Early domain only')
    ax.plot(z, dH_late, 'r-', lw=1.5, label='Late domain only')
    ax.plot(z, dH_both, 'k--', lw=1.5, label='Both domains')
    ax.axhline(0, color='gray', lw=0.5)
    ax.axvline(1060, color='gray', ls=':', alpha=0.4, label='$z_{\\rm drag}$')

    ax.set_xscale('log')
    ax.set_xlabel('$z$')
    ax.set_ylabel('$\\Delta H / H_{\\Lambda{\\rm CDM}}$ [\\%]')
    ax.set_title('Fractional deviation of $H(z)$ from $\\Lambda$CDM')
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.set_xlim(0.01, 10000)

    plt.tight_layout()
    plt.savefig(os.path.join(OUTDIR, 'fig3_Hz_deviation.pdf'))
    plt.savefig(os.path.join(OUTDIR, 'fig3_Hz_deviation.png'))
    plt.close()
    print('  Fig 3: H(z) deviation')


def fig4_channel_decomposition():
    """Channel decomposition: background vs dephasing."""
    fig, ax = plt.subplots(figsize=(7, 5))

    # Data from the two_domain_growth.py results
    labels = ['Background\n(H(z) effect)', 'Dephasing\n(G$_{\\rm eff}$ effect)', 'Combined']
    values = [-1.61, -2.15, -3.76]  # Δσ₈/σ₈ in percent
    colors = ['#4472C4', '#ED7D31', '#2E7D32']

    bars = ax.bar(labels, [-v for v in values], color=colors, width=0.5, edgecolor='black', lw=0.5)

    ax.set_ylabel('$|\\Delta\\sigma_8 / \\sigma_8|$ [\\%]')
    ax.set_title('Late domain growth suppression: channel decomposition')

    # Add percentage labels
    for bar, val in zip(bars, values):
        frac = val / values[2] * 100
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05,
                f'{abs(val):.2f}\\%\n({frac:.0f}\\%)', ha='center', va='bottom', fontsize=9)

    ax.set_ylim(0, 5)
    ax.grid(True, alpha=0.3, axis='y')

    plt.tight_layout()
    plt.savefig(os.path.join(OUTDIR, 'fig4_channel_decomposition.pdf'))
    plt.savefig(os.path.join(OUTDIR, 'fig4_channel_decomposition.png'))
    plt.close()
    print('  Fig 4: channel decomposition')


def fig5_eta_robustness():
    """ΔAIC vs η₀."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))

    eta_vals = [-0.01, -0.02, -0.03, -0.04, -0.05, -0.06, -0.08, -0.10]
    daic_vals = [-6.3, -8.0, -9.5, -11.0, -12.4, -13.6, -15.9, -17.8]
    sig8_vals = [0.824, 0.820, 0.816, 0.813, 0.809, 0.806, 0.798, 0.791]

    ax1.plot([-e for e in eta_vals], daic_vals, 'ko-', lw=2, markersize=6)
    ax1.axhline(0, color='gray', lw=0.5)
    ax1.axhline(-2, color='green', ls='--', alpha=0.5, label='$\\Delta$AIC = $-2$')
    ax1.axhline(-6, color='blue', ls='--', alpha=0.5, label='$\\Delta$AIC = $-6$')
    ax1.fill_between([0, 0.12], 0, 5, alpha=0.08, color='red', label='$\\Lambda$CDM preferred')
    ax1.fill_between([0, 0.12], -25, 0, alpha=0.08, color='green', label='IDT preferred')
    ax1.set_xlabel('$|\\eta_0|$')
    ax1.set_ylabel('$\\Delta$AIC')
    ax1.set_title('Model preference vs dephasing coupling')
    ax1.legend(fontsize=7)
    ax1.set_xlim(0, 0.11)
    ax1.set_ylim(-20, 5)
    ax1.grid(True, alpha=0.3)

    ax2.plot([-e for e in eta_vals], sig8_vals, 'rs-', lw=2, markersize=6)
    ax2.axhline(0.811, color='gray', ls=':', label='$\\Lambda$CDM $\\sigma_8$')
    ax2.axhline(0.770/np.sqrt(0.315/0.3), color='orange', ls=':', alpha=0.7,
                label='DES/KiDS target')
    ax2.set_xlabel('$|\\eta_0|$')
    ax2.set_ylabel('$\\sigma_8$')
    ax2.set_title('$\\sigma_8$ vs dephasing coupling')
    ax2.legend(fontsize=7)
    ax2.set_xlim(0, 0.11)
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(os.path.join(OUTDIR, 'fig5_eta_robustness.pdf'))
    plt.savefig(os.path.join(OUTDIR, 'fig5_eta_robustness.png'))
    plt.close()
    print('  Fig 5: η₀ robustness')


def fig6_fearly_robustness():
    """ΔAIC vs f_early with H₀ and σ₈ tracks."""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(7, 7), sharex=True)

    f_vals = [0.00, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.08, 0.10]
    H0_vals = [66.8, 67.3, 67.7, 68.2, 68.7, 69.1, 69.6, 70.6, 71.6]
    sig8_vals = [0.802, 0.804, 0.806, 0.808, 0.810, 0.812, 0.814, 0.818, 0.822]
    daic_vals = [-4.3, -8.3, -11.0, -12.3, -12.3, -10.7, -7.7, 2.9, 19.9]

    # ΔAIC
    ax1.plot([f*100 for f in f_vals], daic_vals, 'ko-', lw=2, markersize=6)
    ax1.axhline(0, color='gray', lw=0.5)
    ax1.axhline(-2, color='green', ls='--', alpha=0.5)
    ax1.fill_between([0, 12], 0, 25, alpha=0.08, color='red')
    ax1.fill_between([0, 12], -15, 0, alpha=0.08, color='green')
    ax1.set_ylabel('$\\Delta$AIC')
    ax1.set_title('Model preference and observables vs early domain amplitude')
    ax1.set_ylim(-15, 25)
    ax1.grid(True, alpha=0.3)

    # H₀ and σ₈
    color_h0 = '#4472C4'
    color_s8 = '#ED7D31'
    ax2.plot([f*100 for f in f_vals], H0_vals, 'o-', color=color_h0, lw=2,
             markersize=6, label='$H_0$')
    ax2.set_ylabel('$H_0$ [km/s/Mpc]', color=color_h0)
    ax2.tick_params(axis='y', labelcolor=color_h0)
    ax2.set_xlabel('$f_{\\rm dom}^{\\rm early}$ [\\%]')
    ax2.axhline(67.36, color=color_h0, ls=':', alpha=0.5)
    ax2.grid(True, alpha=0.3)

    ax3 = ax2.twinx()
    ax3.plot([f*100 for f in f_vals], sig8_vals, 's-', color=color_s8, lw=2,
             markersize=6, label='$\\sigma_8$')
    ax3.set_ylabel('$\\sigma_8$', color=color_s8)
    ax3.tick_params(axis='y', labelcolor=color_s8)
    ax3.axhline(0.811, color=color_s8, ls=':', alpha=0.5)

    ax2.set_xlim(-0.5, 10.5)

    plt.tight_layout()
    plt.savefig(os.path.join(OUTDIR, 'fig6_fearly_robustness.pdf'))
    plt.savefig(os.path.join(OUTDIR, 'fig6_fearly_robustness.png'))
    plt.close()
    print('  Fig 6: f_early robustness')


def fig7_channel_independence():
    """Channel independence: domain ON/OFF combinations."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.5))

    # Data from channel independence tests
    configs = ['$\\Lambda$CDM', 'Early\nonly', 'Late\nonly', 'Both']

    # r_d values
    rd_vals = [147.10, 145.55, 147.10, 145.55]
    colors_rd = ['gray', '#4472C4', '#ED7D31', '#2E7D32']
    bars1 = ax1.bar(configs, rd_vals, color=colors_rd, width=0.5, edgecolor='black', lw=0.5)
    ax1.set_ylabel('$r_d$ [Mpc]')
    ax1.set_title('Sound horizon $r_d$')
    ax1.set_ylim(144, 148)
    ax1.axhline(147.10, color='gray', ls=':', alpha=0.5)
    for bar, val in zip(bars1, rd_vals):
        ax1.text(bar.get_x() + bar.get_width()/2, val + 0.05,
                 f'{val:.1f}', ha='center', va='bottom', fontsize=8)
    ax1.grid(True, alpha=0.3, axis='y')

    # σ₈ values (with dephasing for late domain)
    s8_vals = [0.811, 0.812, 0.793, 0.797]
    bars2 = ax2.bar(configs, s8_vals, color=colors_rd, width=0.5, edgecolor='black', lw=0.5)
    ax2.set_ylabel('$\\sigma_8$')
    ax2.set_title('Structure growth $\\sigma_8$ (with dephasing)')
    ax2.set_ylim(0.78, 0.82)
    ax2.axhline(0.811, color='gray', ls=':', alpha=0.5, label='$\\Lambda$CDM')
    for bar, val in zip(bars2, s8_vals):
        ax2.text(bar.get_x() + bar.get_width()/2, val + 0.0005,
                 f'{val:.3f}', ha='center', va='bottom', fontsize=8)
    ax2.legend(fontsize=8)
    ax2.grid(True, alpha=0.3, axis='y')

    plt.tight_layout()
    plt.savefig(os.path.join(OUTDIR, 'fig7_channel_independence.pdf'))
    plt.savefig(os.path.join(OUTDIR, 'fig7_channel_independence.png'))
    plt.close()
    print('  Fig 7: channel independence')


def fig8_dephasing_gamma():
    """The dephasing coupling function Γ(z) and G_eff(z)."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))

    z = np.linspace(0.01, 5, 500)
    sigma_ln = 0.5
    z_c = 1.0

    ln_ratio = np.log((1+z)/(1+z_c))
    sigma2 = sigma_ln**2
    rho_shape = np.exp(-0.5 * ln_ratio**2 / sigma2)
    Gamma = (ln_ratio / sigma2) * rho_shape

    eta0 = -0.05
    G_eff = 1 + eta0 * Gamma

    ax1.plot(z, Gamma, 'r-', lw=2)
    ax1.axhline(0, color='k', lw=0.5)
    ax1.axvline(1.0, color='gray', ls='--', alpha=0.5, label='$z_c = 1.0$')
    ax1.fill_between(z, 0, Gamma, where=(Gamma > 0), alpha=0.15, color='blue',
                     label='Rising side ($\\Gamma > 0$)')
    ax1.fill_between(z, 0, Gamma, where=(Gamma < 0), alpha=0.15, color='red',
                     label='Falling side ($\\Gamma < 0$)')
    ax1.set_xlabel('$z$')
    ax1.set_ylabel('$\\Gamma(z)$')
    ax1.set_title('Dephasing coupling function')
    ax1.legend(fontsize=7)
    ax1.grid(True, alpha=0.3)

    ax2.plot(z, G_eff, 'k-', lw=2)
    ax2.axhline(1.0, color='gray', ls=':', label='$G_{\\rm eff} = G$')
    ax2.axvline(1.0, color='gray', ls='--', alpha=0.5)
    ax2.fill_between(z, 1.0, G_eff, where=(G_eff < 1), alpha=0.2, color='blue',
                     label='Growth suppressed')
    ax2.fill_between(z, 1.0, G_eff, where=(G_eff > 1), alpha=0.2, color='red',
                     label='Growth enhanced')
    ax2.set_xlabel('$z$')
    ax2.set_ylabel('$G_{\\rm eff}(z) / G$')
    ax2.set_title(f'Effective gravitational coupling ($\\eta_0 = {eta0}$)')
    ax2.legend(fontsize=7)
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(os.path.join(OUTDIR, 'fig8_dephasing_gamma.pdf'))
    plt.savefig(os.path.join(OUTDIR, 'fig8_dephasing_gamma.png'))
    plt.close()
    print('  Fig 8: dephasing Γ(z) and G_eff(z)')


if __name__ == "__main__":
    print("Generating Paper 1 figures...")
    print()
    fig1_domain_profiles()
    fig2_equation_of_state()
    fig3_Hz_deviation()
    fig4_channel_decomposition()
    fig5_eta_robustness()
    fig6_fearly_robustness()
    fig7_channel_independence()
    fig8_dephasing_gamma()
    print()
    print(f"All figures saved to {OUTDIR}/")
