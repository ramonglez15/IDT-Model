"""
ΛCDM Baseline Cosmology
========================
Standard Friedmann equation components used by IDT domain module.
Separated for clean imports and testability.
"""

import numpy as np
from scipy.integrate import quad

# Default Planck 2018 parameters
_H0 = 67.36
_Omega_m = 0.3153
_Omega_b = 0.0493
_Omega_r = 9.1e-5
_Omega_gamma = 5.38e-5  # photons only
_Omega_Lambda = 1.0 - _Omega_m - _Omega_r
_c_km_s = 2.998e5


def E2_LCDM(z, Omega_m=_Omega_m, Omega_r=_Omega_r, Omega_Lambda=_Omega_Lambda):
    """
    (H/H₀)² for flat ΛCDM.
    
    E²(z) = Ω_m(1+z)³ + Ω_r(1+z)⁴ + Ω_Λ
    """
    z = np.asarray(z, dtype=float)
    return Omega_m * (1+z)**3 + Omega_r * (1+z)**4 + Omega_Lambda


def H_LCDM(z, H0=_H0, **kwargs):
    """H(z) in km/s/Mpc for flat ΛCDM."""
    return H0 * np.sqrt(E2_LCDM(z, **kwargs))


def sound_horizon(H_func, z_drag=1059.94, Omega_b=_Omega_b, 
                  Omega_gamma=_Omega_gamma):
    """
    Comoving sound horizon at the drag epoch.
    
    r_d = ∫_{z_drag}^{∞} c_s(z)/H(z) dz
    
    where c_s(z) = c / √(3(1 + R_b(z)))
    and R_b = 3ρ_b/(4ρ_γ) = 3Ω_b / (4Ω_γ(1+z))
    """
    def integrand(z):
        R_b = 3.0 * Omega_b / (4.0 * Omega_gamma * (1.0 + z))
        c_s = _c_km_s / np.sqrt(3.0 * (1.0 + R_b))
        return c_s / H_func(z)
    
    result, _ = quad(integrand, z_drag, 1e5, limit=500)
    return result  # Mpc


def comoving_distance(z_val, H_func):
    """Comoving distance d_C(z) in Mpc."""
    if z_val < 1e-6:
        return 0.0
    result, _ = quad(lambda zp: _c_km_s / H_func(zp), 0, z_val, limit=200)
    return result


def luminosity_distance(z_val, H_func):
    """Luminosity distance d_L(z) in Mpc."""
    return (1 + z_val) * comoving_distance(z_val, H_func)


def angular_diameter_distance(z_val, H_func):
    """Angular diameter distance d_A(z) in Mpc."""
    return comoving_distance(z_val, H_func) / (1 + z_val)


def distance_modulus(z_val, H_func):
    """Distance modulus μ(z) in magnitudes."""
    dl = luminosity_distance(z_val, H_func)
    if dl <= 0:
        return np.nan
    return 5.0 * np.log10(dl) + 25.0


def CMB_shift_parameters(H_func, z_star=1089.92, z_drag=1059.94,
                          H0=_H0, Omega_m=_Omega_m):
    """
    CMB shift parameters R and l_a.

    These compress the main CMB constraints into two numbers:

    R = √(Ω_m) · (H₀/c) · d_C(z*)
        (shift parameter — constrains comoving distance to LSS)

    l_a = π · d_C(z*) / r_s(z_drag)
        (acoustic scale — constrains peak positions)

    These are useful for quick CMB consistency checks before full
    CLASS integration.
    """
    d_C = comoving_distance(z_star, H_func)
    d_A = d_C / (1 + z_star)
    r_s = sound_horizon(H_func, z_drag=z_drag)

    R = np.sqrt(Omega_m) * H0 / _c_km_s * d_C
    l_a = np.pi * d_C / r_s

    return {'R': R, 'l_a': l_a, 'd_A': d_A, 'd_C': d_C, 'r_s': r_s}
