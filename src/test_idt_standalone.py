"""
IDT Module Validation Tests
============================
Run these BEFORE attempting CLASS integration to verify:
1. Conservation equation is satisfied
2. w(z) behaves as expected
3. Background observables are physically reasonable
4. Sound horizon shift matches analytical expectations
5. Late-time distances remain acceptable

No CLASS dependency required — runs with numpy/scipy/matplotlib only.

Usage:
    cd idt_class_module
    python tests/test_idt_standalone.py
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import numpy as np
import matplotlib.pyplot as plt
from cosmology_base import (E2_LCDM, H_LCDM, sound_horizon, 
                            comoving_distance, distance_modulus,
                            CMB_shift_parameters)

# We need to handle the relative import in idt_domain
# Temporarily patch cosmology_base into the expected location
import cosmology_base
sys.modules['idt_class_module.cosmology_base'] = cosmology_base
from idt_domain import IDTDomain, IDTModel


def test_conservation(domain, name=""):
    """Test 1: Verify continuity equation."""
    print(f"\n--- Test 1: Conservation [{name}] ---")
    passed, max_err = domain.check_conservation()
    print(f"  Max relative error: {max_err:.2e}")
    print(f"  Result: {'PASS ✓' if passed else 'FAIL ✗'}")
    return passed


def test_w_behavior(domain, name=""):
    """Test 2: Check w(z) is finite and well-behaved."""
    print(f"\n--- Test 2: w(z) behavior [{name}] ---")
    
    z_test = np.logspace(-2, 4, 10000)
    w_vals = domain.w(z_test)
    
    all_finite = np.all(np.isfinite(w_vals))
    w_at_peak = float(domain.w(domain.z_c))
    w_at_zero = float(domain.w(0.01))
    w_min = np.min(w_vals)
    w_max = np.max(w_vals)
    
    print(f"  w(z=0)  = {w_at_zero:.4f}")
    print(f"  w(z_c)  = {w_at_peak:.4f}")
    print(f"  w range = [{w_min:.4f}, {w_max:.4f}]")
    print(f"  All finite: {all_finite}")
    
    # w at the peak should be -1 (since d(ln ρ)/d(ln(1+z)) = 0 there)
    w_peak_check = abs(w_at_peak - (-1.0)) < 0.01
    print(f"  w(z_c) ≈ -1: {'PASS ✓' if w_peak_check else 'FAIL ✗'}")
    
    passed = all_finite and w_peak_check
    print(f"  Result: {'PASS ✓' if passed else 'FAIL ✗'}")
    return passed


def test_sound_horizon(domain, name=""):
    """Test 3: Sound horizon shift."""
    print(f"\n--- Test 3: Sound horizon [{name}] ---")
    
    model = IDTModel(domains=[domain])
    
    rd_lcdm = sound_horizon(H_LCDM)
    rd_idt = sound_horizon(model.H)
    delta_rd = (rd_idt - rd_lcdm) / rd_lcdm * 100
    H0_inferred = 67.36 * rd_lcdm / rd_idt
    
    print(f"  r_d(ΛCDM) = {rd_lcdm:.2f} Mpc")
    print(f"  r_d(IDT)  = {rd_idt:.2f} Mpc")
    print(f"  Δr_d/r_d  = {delta_rd:+.2f}%")
    print(f"  H₀ inferred = {H0_inferred:.2f} km/s/Mpc")
    
    # Sanity: r_d should decrease (domain adds energy → faster expansion 
    # → less time for sound to travel → smaller r_d)
    rd_decreased = rd_idt <= rd_lcdm
    print(f"  r_d decreased: {'PASS ✓' if rd_decreased else 'UNEXPECTED'}")
    
    return rd_decreased, delta_rd, H0_inferred


def test_late_time_distances(domain, name=""):
    """Test 4: Late-time distances aren't wrecked."""
    print(f"\n--- Test 4: Late-time distances [{name}] ---")
    
    model = IDTModel(domains=[domain])
    
    z_test = np.linspace(0.01, 2.0, 50)
    mu_lcdm = np.array([distance_modulus(z, H_LCDM) for z in z_test])
    mu_idt = np.array([distance_modulus(z, model.H) for z in z_test])
    
    max_dmu = np.max(np.abs(mu_idt - mu_lcdm))
    
    print(f"  max|Δμ| = {max_dmu:.6f} mag")
    print(f"  Pantheon+ binned precision: ~0.02 mag")
    
    passed = max_dmu < 0.05  # conservative threshold
    print(f"  Within SN constraints: {'PASS ✓' if passed else 'FAIL ✗'}")
    return passed


def test_cmb_shift_params(domain, name=""):
    """Test 5: CMB shift parameters."""
    print(f"\n--- Test 5: CMB shift parameters [{name}] ---")
    
    model = IDTModel(domains=[domain])
    
    sp_lcdm = CMB_shift_parameters(H_LCDM)
    sp_idt = CMB_shift_parameters(model.H)
    
    print(f"  {'':>10} {'ΛCDM':>10} {'IDT':>10} {'Δ/ΛCDM':>10}")
    for key in ['R', 'l_a', 'r_s']:
        v_l = sp_lcdm[key]
        v_i = sp_idt[key]
        delta = (v_i - v_l) / v_l * 100
        print(f"  {key:>10} {v_l:>10.4f} {v_i:>10.4f} {delta:>+9.2f}%")
    
    # Planck 2018 compressed constraints:
    # R = 1.7502 ± 0.0046
    # l_a = 301.471 ± 0.090
    R_planck = 1.7502
    R_err = 0.0046
    R_idt = sp_idt['R']
    R_tension = abs(R_idt - R_planck) / R_err
    
    la_planck = 301.471
    la_err = 0.090
    la_idt = sp_idt['l_a']
    la_tension = abs(la_idt - la_planck) / la_err
    
    print(f"\n  Planck shift parameter constraints:")
    print(f"  R:   IDT={R_idt:.4f} vs Planck={R_planck}±{R_err} ({R_tension:.1f}σ)")
    print(f"  l_a: IDT={la_idt:.3f} vs Planck={la_planck}±{la_err} ({la_tension:.1f}σ)")
    
    return R_tension, la_tension


def run_all_tests():
    """Run complete test suite."""
    print("=" * 70)
    print("IDT MODULE VALIDATION — STANDALONE TESTS")
    print("=" * 70)
    
    # Define test configurations
    configs = [
        ("Conservative (f=5%, z_c=1500)", 
         IDTDomain(f_dom=0.05, z_c=1500, delta_z=450)),
        ("Medium (f=10%, z_c=2000)", 
         IDTDomain(f_dom=0.10, z_c=2000, delta_z=600)),
        ("Aggressive (f=15%, z_c=2000)", 
         IDTDomain(f_dom=0.15, z_c=2000, delta_z=600)),
        ("Maximum (f=20%, z_c=3000)", 
         IDTDomain(f_dom=0.20, z_c=3000, delta_z=900)),
    ]
    
    all_results = []
    
    for name, domain in configs:
        print(f"\n{'='*70}")
        print(f"CONFIGURATION: {name}")
        print(f"{'='*70}")
        
        domain.summary()
        
        t1 = test_conservation(domain, name)
        t2 = test_w_behavior(domain, name)
        t3_pass, t3_drd, t3_H0 = test_sound_horizon(domain, name)
        t4 = test_late_time_distances(domain, name)
        t5_R, t5_la = test_cmb_shift_params(domain, name)
        
        all_results.append({
            'name': name, 'domain': domain,
            'conservation': t1, 'w_ok': t2,
            'rd_shift': t3_drd, 'H0_inferred': t3_H0,
            'sn_ok': t4, 'R_sigma': t5_R, 'la_sigma': t5_la,
        })
    
    # ============================================================
    # Summary plot
    # ============================================================
    fig, axes = plt.subplots(2, 3, figsize=(16, 10))
    fig.suptitle('IDT Module Validation Suite', fontsize=14, fontweight='bold')
    
    z_bg = np.logspace(-2, 4, 2000)
    z_late = np.linspace(0.01, 2.0, 100)
    mu_lcdm = np.array([distance_modulus(z, H_LCDM) for z in z_late])
    
    for res in all_results:
        domain = res['domain']
        model = IDTModel(domains=[domain])
        label = res['name'].split("(")[0].strip()
        
        # Panel 1: Ω_domain(z)
        ax = axes[0, 0]
        omega = domain.Omega(z_bg)
        E2_tot = model.E2(z_bg)
        frac = np.where(E2_tot > 0, omega / E2_tot * 100, 0)
        ax.plot(z_bg, frac, lw=1.5, label=label)
    
    ax = axes[0, 0]
    ax.axvline(1060, color='gray', ls='--', alpha=0.5, label='z_drag')
    ax.set_xscale('log')
    ax.set_xlabel('z')
    ax.set_ylabel('ρ_dom/ρ_tot [%]')
    ax.set_title('Domain Fraction')
    ax.legend(fontsize=7)
    ax.grid(True, alpha=0.3)
    
    for res in all_results:
        domain = res['domain']
        label = res['name'].split("(")[0].strip()
        
        # Panel 2: w(z) near peak
        ax = axes[0, 1]
        z_w = np.linspace(max(domain.z_c - 3*domain.delta_z, 1), 
                          domain.z_c + 3*domain.delta_z, 500)
        ax.plot(z_w, domain.w(z_w), lw=1.5, label=label)
    
    ax = axes[0, 1]
    ax.axhline(-1, color='k', ls=':', lw=0.5)
    ax.set_xlabel('z')
    ax.set_ylabel('w(z)')
    ax.set_title('Equation of State (near peak)')
    ax.legend(fontsize=7)
    ax.grid(True, alpha=0.3)
    
    for res in all_results:
        domain = res['domain']
        model = IDTModel(domains=[domain])
        label = res['name'].split("(")[0].strip()
        
        # Panel 3: ΔH/H
        ax = axes[0, 2]
        z_H = np.logspace(2, 4, 500)
        H_l = np.array([H_LCDM(z) for z in z_H])
        H_i = np.array([model.H(z) for z in z_H])
        ax.plot(z_H, (H_i - H_l)/H_l * 100, lw=1.5, label=label)
    
    ax = axes[0, 2]
    ax.axvline(1060, color='gray', ls='--', alpha=0.5)
    ax.axhline(0, color='k', lw=0.5)
    ax.set_xscale('log')
    ax.set_xlabel('z')
    ax.set_ylabel('ΔH/H [%]')
    ax.set_title('H(z) Deviation')
    ax.legend(fontsize=7)
    ax.grid(True, alpha=0.3)
    
    for res in all_results:
        domain = res['domain']
        model = IDTModel(domains=[domain])
        label = res['name'].split("(")[0].strip()
        
        # Panel 4: Distance modulus
        ax = axes[1, 0]
        mu_i = np.array([distance_modulus(z, model.H) for z in z_late])
        ax.plot(z_late, mu_i - mu_lcdm, lw=1.5, label=label)
    
    ax = axes[1, 0]
    ax.axhline(0, color='k', lw=0.5)
    ax.fill_between(z_late, -0.02, 0.02, alpha=0.12, color='green')
    ax.set_xlabel('z')
    ax.set_ylabel('Δμ [mag]')
    ax.set_title('SN Distance Residual')
    ax.legend(fontsize=7)
    ax.grid(True, alpha=0.3)
    
    # Panel 5: c_a² (adiabatic sound speed)
    ax = axes[1, 1]
    for res in all_results:
        domain = res['domain']
        label = res['name'].split("(")[0].strip()
        z_ca = np.linspace(max(domain.z_c - 3*domain.delta_z, 1),
                           domain.z_c + 3*domain.delta_z, 500)
        ca2 = domain.ca2(z_ca)
        ax.plot(z_ca, ca2, lw=1.5, label=label)
    ax.axhline(0, color='k', ls=':', lw=0.5, label='c_a²=0')
    ax.set_xlabel('z')
    ax.set_ylabel('c_a²')
    ax.set_title('Adiabatic Sound Speed²')
    ax.legend(fontsize=7)
    ax.grid(True, alpha=0.3)
    
    # Panel 6: Summary scorecard
    ax = axes[1, 2]
    ax.axis('off')
    
    rows = [['Config', 'Δr_d/r_d', 'H₀_inf', 'max|Δμ|', 'R(σ)', 'l_a(σ)']]
    for res in all_results:
        label = res['name'].split("(")[0].strip()
        rows.append([
            label,
            f"{res['rd_shift']:+.1f}%",
            f"{res['H0_inferred']:.1f}",
            'OK' if res['sn_ok'] else 'FAIL',
            f"{res['R_sigma']:.1f}",
            f"{res['la_sigma']:.1f}",
        ])
    
    table = ax.table(cellText=rows, loc='center', cellLoc='center',
                    colWidths=[0.2, 0.15, 0.12, 0.12, 0.1, 0.1])
    table.auto_set_font_size(False)
    table.set_fontsize(8)
    table.scale(1, 1.6)
    for j in range(6):
        table[0, j].set_facecolor('#4472C4')
        table[0, j].set_text_props(color='white', fontweight='bold', fontsize=7)
    ax.set_title('Results Summary', fontsize=11, fontweight='bold', pad=15)
    
    plt.tight_layout()
    plt.savefig(os.path.join(os.path.dirname(__file__), '..', 
                'idt_validation_suite.png'), dpi=150, bbox_inches='tight')
    plt.close()
    print(f"\nValidation plot saved: idt_validation_suite.png")
    
    # ============================================================
    # Final verdict
    # ============================================================
    print("\n" + "=" * 70)
    print("VALIDATION SUMMARY")
    print("=" * 70)
    
    all_pass = True
    for res in all_results:
        name = res['name']
        issues = []
        if not res['conservation']:
            issues.append("conservation fails")
        if not res['w_ok']:
            issues.append("w(z) ill-behaved")
        if not res['sn_ok']:
            issues.append("SN constraint violated")
        
        status = "PASS ✓" if not issues else f"ISSUES: {', '.join(issues)}"
        print(f"  {name}: {status}")
        if issues:
            all_pass = False
    
    print(f"\nOverall: {'ALL TESTS PASS ✓' if all_pass else 'SOME ISSUES — review above'}")
    print("\nNext step: Run idt_classy_wrapper.py with CLASS installed")
    print("to perform perturbation-level sanity check.")


if __name__ == "__main__":
    run_all_tests()
