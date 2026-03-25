"""
IDT Domain Fluid Module
========================
Minimal early-time domain parameterization for CLASS integration.

Physics:
    The domain is modeled as a conserved effective fluid with:
    - Energy density ρ_dom(z) specified via a peaked profile
    - Pressure p_dom(z) = w(z) · ρ_dom(z)
    - Conservation ∇_μ T^{μν} = 0 satisfied by construction
    - Adiabatic perturbations with stable sound speed c_s²

Parameters (minimal set — 3 free + 1 fixed):
    f_dom   : peak fractional energy density ρ_dom/ρ_total at z_c
    z_c     : critical redshift (center of domain activity)
    Δ_z     : width parameter (controls how localized the domain is)
    c_s2    : sound speed squared for perturbations (fixed, default = 1)

Design choices:
    1. ρ_dom(z) is defined as a profile, NOT derived from ΔH²
    2. w(z) is derived from ρ_dom(z) via conservation, not assumed
    3. Perturbations use standard fluid equations (no exotic couplings)
    4. All functions are vectorized and CLASS-integration-ready

Author: Jose / IDT collaboration
Version: 1.0 — minimal early-time model for Paper 1
"""

import numpy as np
from scipy.interpolate import CubicSpline


class IDTDomain:
    """
    Single IDT domain component.
    
    Represents a localized energy density contribution active around
    a characteristic redshift z_c, parameterized by its peak fractional
    contribution to the total energy budget.
    
    The domain satisfies energy-momentum conservation by construction:
        dρ/dτ + 3H(ρ + p) = 0
    equivalently:
        dρ/dz = 3(1 + w(z)) / (1 + z) · ρ(z)
    
    w(z) is derived from the specified ρ(z) profile via this equation,
    NOT assumed a priori.
    """
    
    def __init__(self, f_dom, z_c, delta_z, c_s2=1.0, n_grid=100000):
        """
        Parameters
        ----------
        f_dom : float
            Peak fractional energy density: ρ_dom(z_c) / ρ_total(z_c).
            Typical range: 0.02 - 0.20 for H₀-relevant effects.
            
        z_c : float
            Critical redshift where domain is maximally active.
            For H₀ via r_d shift: z_c ~ 1500-3000 (pre-recombination).
            For σ₈ effects: z_c ~ 0.3-2.0 (late-time).
            
        delta_z : float
            Width of the domain profile in redshift space.
            Controls how localized the domain is. Typically ~ 0.2-0.5 × z_c.
            
        c_s2 : float
            Rest-frame sound speed squared for perturbations.
            c_s2 = 1: stiff fluid (maximally stable, minimal clustering).
            c_s2 = 1/3: radiation-like.
            c_s2 = 0: dust-like (clusters strongly — may cause instabilities).
            Default = 1 (most conservative).
            
        n_grid : int
            Number of grid points for internal interpolation tables.
        """
        self.f_dom = f_dom
        self.z_c = z_c
        self.delta_z = delta_z
        self.c_s2 = c_s2
        
        # Validate inputs
        assert 0 < f_dom < 1, f"f_dom must be in (0, 1), got {f_dom}"
        assert z_c > 0, f"z_c must be positive, got {z_c}"
        assert delta_z > 0, f"delta_z must be positive, got {delta_z}"
        assert 0 <= c_s2 <= 1, f"c_s2 must be in [0, 1], got {c_s2}"
        
        # Build interpolation tables for fast evaluation
        self._build_tables(n_grid)
    
    def _build_tables(self, n_grid):
        """Pre-compute ρ(z), w(z), and derived quantities on a grid."""
        
        # Grid in log(1+z) for better resolution across decades
        lna_min = 0  # z = 0
        lna_max = np.log(1 + 1.2e4)  # z ~ 12000 (well above recombination)
        
        self._ln1z_grid = np.linspace(lna_min, lna_max, n_grid)
        self._z_grid = np.exp(self._ln1z_grid) - 1
        
        # -------------------------------------------------------
        # Step 1: Define the ρ_dom profile shape
        # -------------------------------------------------------
        # Use a log-normal profile in (1+z) space:
        #   ρ_shape(z) = exp(-0.5 * [ln((1+z)/(1+z_c)) / σ_ln]²)
        #
        # This is natural because cosmological evolution is 
        # multiplicative in (1+z), so log-space is the right metric.
        # It also avoids the issue of Gaussians in linear z being 
        # asymmetric in physical time.
        
        self._sigma_ln = self.delta_z / (1 + self.z_c)
        
        log_ratio = np.log((1 + self._z_grid) / (1 + self.z_c))
        self._rho_shape = np.exp(-0.5 * (log_ratio / self._sigma_ln)**2)
        
        # -------------------------------------------------------
        # Step 2: Normalize to achieve f_dom at z_c
        # -------------------------------------------------------
        # At z_c: ρ_dom(z_c) / ρ_total(z_c) = f_dom
        # ρ_total(z_c) ≈ ρ_crit,0 * E²(z_c)  [ΛCDM piece]
        # So: Ω_dom(z_c) = f_dom / (1 - f_dom) * E²_ΛCDM(z_c)
        #
        # We store Ω_dom(z) = ρ_dom(z) / ρ_crit,0 in units of H₀²
        
        try:
            from .cosmology_base import E2_LCDM
        except ImportError:
            from cosmology_base import E2_LCDM
        
        E2_at_zc = E2_LCDM(self.z_c)
        self._Omega_peak = self.f_dom / (1 - self.f_dom) * E2_at_zc
        
        self._Omega_grid = self._Omega_peak * self._rho_shape
        
        # -------------------------------------------------------
        # Step 3: Derive w(z) from conservation equation
        # -------------------------------------------------------
        # dρ/dz = 3(1+w)/(1+z) · ρ
        # => w(z) = -1 + (1+z)/(3ρ) · dρ/dz
        # => w(z) = -1 + (1/3) · d(ln ρ)/d(ln(1+z))
        
        # Compute d(ln ρ)/d(ln(1+z)) from the profile
        # For log-normal: ln ρ_shape = -0.5 * [ln((1+z)/(1+z_c))]² / σ²
        # d(ln ρ)/d(ln(1+z)) = -ln((1+z)/(1+z_c)) / σ²
        
        self._dlnrho_dlna = -log_ratio / self._sigma_ln**2
        self._w_grid = -1.0 + (1.0/3.0) * self._dlnrho_dlna
        
        # -------------------------------------------------------
        # Step 4: Build cubic spline interpolators
        # -------------------------------------------------------
        self._Omega_spline = CubicSpline(self._z_grid, self._Omega_grid)
        self._w_spline = CubicSpline(self._z_grid, self._w_grid)
        self._dlnrho_spline = CubicSpline(self._z_grid, self._dlnrho_dlna)
    
    # ===============================================================
    # Public interface — background quantities
    # ===============================================================
    
    def Omega(self, z):
        """
        Domain energy density parameter: ρ_dom(z) / ρ_crit,0
        
        This is what gets added to E²(z) = H²(z)/H₀²:
            E²_IDT(z) = E²_ΛCDM(z) + Ω_dom(z)
        """
        z = np.asarray(z, dtype=float)
        return np.maximum(self._Omega_spline(z), 0)
    
    def w(self, z):
        """
        Effective equation of state derived from conservation.
        
        w(z) = -1 + (1/3) · d(ln ρ)/d(ln(1+z))
        
        Note: This will show w < -1 on the falling side and w > -1 
        on the rising side of the profile. This is expected for a 
        localized effective component and does NOT necessarily imply
        ghost instabilities, since the domain is not required to be
        a fundamental scalar field.
        """
        z = np.asarray(z, dtype=float)
        return self._w_spline(z)
    
    def pressure_over_rho(self, z):
        """p/ρ = w(z). Convenience function for CLASS."""
        return self.w(z)
    
    def rho_plus_p_over_rho(self, z):
        """(ρ + p)/ρ = 1 + w(z). Used in perturbation equations."""
        return 1.0 + self.w(z)
    
    def dlnrho_dlna(self, z):
        """
        d(ln ρ_dom) / d(ln a) = -d(ln ρ_dom) / d(ln(1+z))
        
        Sign convention: ln(a) = -ln(1+z), so:
            d(ln ρ)/d(ln a) = -(d(ln ρ)/d(ln(1+z)))
            = -(-log_ratio / σ²)
            = +log_ratio / σ²
            = 3(1 + w)   [from conservation]
        
        This is needed for CLASS background integration.
        """
        z = np.asarray(z, dtype=float)
        return -self._dlnrho_spline(z)
    
    # ===============================================================
    # Public interface — perturbation quantities
    # ===============================================================
    
    def cs2(self, z):
        """
        Rest-frame sound speed squared.
        
        For adiabatic perturbations: c_s² = δp/δρ (rest frame).
        
        We fix this as a parameter rather than deriving it from w(z),
        because c_s² = w only holds for a barotropic perfect fluid,
        and the domain may not be one.
        
        c_s² = 1: stiff (no clustering, maximally stable)
        c_s² = 1/3: radiation-like
        c_s² = 0: dust-like (clusters, potential instabilities)
        """
        return self.c_s2
    
    def ca2(self, z):
        """
        Adiabatic sound speed squared: c_a² = w - w'/(3(1+w))
        where w' = dw/d(ln a).
        
        This appears in the perturbation equations for non-constant w.
        CLASS needs this to handle gauge-invariant perturbations correctly.
        """
        z = np.asarray(z, dtype=float)
        w_val = self.w(z)
        
        # dw/dz from spline
        dw_dz = self._w_spline(z, 1)  # first derivative
        
        # dw/d(ln a) = -(1+z) * dw/dz
        dw_dlna = -(1 + z) * dw_dz
        
        # c_a² = w - w'/(3(1+w))
        wpw = 1.0 + w_val
        # Avoid division by zero where w = -1
        safe_wpw = np.where(np.abs(wpw) > 1e-10, wpw, 1e-10)
        
        ca2 = w_val - dw_dlna / (3.0 * safe_wpw)
        return ca2
    
    # ===============================================================
    # Perturbation equations (synchronous gauge, CLASS convention)
    # ===============================================================
    
    def delta_dot(self, z, delta, theta, h_dot, w_val=None):
        """
        Time derivative of density contrast δ_dom (synchronous gauge).
        
        δ̇ = -(1 + w)(θ + ḣ/2) - 3H(c_s² - w)δ
              - 9H²(1+w)(c_s² - c_a²)θ/k²
        
        Parameters
        ----------
        z : float
            Redshift
        delta : float
            Domain density contrast
        theta : float
            Domain velocity divergence
        h_dot : float
            Trace of metric perturbation time derivative (ḣ)
        w_val : float, optional
            Pre-computed w(z)
            
        Returns
        -------
        float : dδ/dτ
        """
        if w_val is None:
            w_val = float(self.w(z))
        
        cs2_val = self.cs2(z)
        ca2_val = float(self.ca2(z))
        
        # Note: H factor is absorbed into conformal time derivative
        # in CLASS. This provides the structure; CLASS handles the 
        # conformal time / scale factor bookkeeping.
        
        wpw = 1.0 + w_val
        
        delta_dot = (
            -wpw * (theta + 0.5 * h_dot)
            # The remaining terms involve H and k which CLASS provides
        )
        
        return delta_dot
    
    def theta_dot(self, z, delta, theta, k, w_val=None):
        """
        Time derivative of velocity divergence θ_dom (synchronous gauge).
        
        θ̇ = -H(1 - 3w)θ + c_s²k²δ/(1+w)
        
        For c_s² > 0, pressure support prevents gravitational collapse.
        For c_s² = 0, the domain clusters like matter.
        """
        if w_val is None:
            w_val = float(self.w(z))
        
        cs2_val = self.cs2(z)
        wpw = 1.0 + w_val
        
        if abs(wpw) < 1e-10:
            pressure_term = 0.0
        else:
            pressure_term = cs2_val * k**2 * delta / wpw
        
        theta_dot = pressure_term  # H-dependent damping handled by CLASS
        
        return theta_dot
    
    # ===============================================================
    # Diagnostics and validation
    # ===============================================================
    
    def check_conservation(self, z_test=None, rtol=1e-4):
        """
        Verify that the continuity equation is satisfied.
        
        Tests: dρ/dz = 3(1+w)/(1+z) · ρ
        
        Returns True if conservation holds within rtol at all test points.
        """
        if z_test is None:
            z_test = np.linspace(0.1, 10000, 1000)
        
        rho = self.Omega(z_test)
        w_val = self.w(z_test)
        
        # Numerical derivative
        dz = 1e-4 * (1 + z_test)
        rho_plus = self.Omega(z_test + dz)
        rho_minus = self.Omega(z_test - dz)
        drho_dz_numerical = (rho_plus - rho_minus) / (2 * dz)
        
        # Analytical (from conservation)
        drho_dz_analytical = 3 * (1 + w_val) / (1 + z_test) * rho
        
        # Check where ρ is non-negligible
        mask = rho > 1e-10 * np.max(rho)
        if not np.any(mask):
            return True
        
        ratio = drho_dz_numerical[mask] / drho_dz_analytical[mask]
        max_err = np.max(np.abs(ratio - 1))
        
        return max_err < rtol, max_err
    
    def summary(self):
        """Print a summary of the domain parameters and diagnostics."""
        print(f"IDT Domain Summary")
        print(f"==================")
        print(f"  f_dom    = {self.f_dom:.4f} ({self.f_dom*100:.1f}%)")
        print(f"  z_c      = {self.z_c:.1f}")
        print(f"  Δ_z      = {self.delta_z:.1f}")
        print(f"  σ_ln     = {self._sigma_ln:.4f}")
        print(f"  c_s²     = {self.c_s2}")
        print(f"  Ω_peak   = {self._Omega_peak:.6e}")
        print(f"  w(z_c)   = {float(self.w(self.z_c)):.4f}")
        print(f"  w(z=0)   = {float(self.w(0.01)):.4f}")
        
        conserved, err = self.check_conservation()
        print(f"  Conservation check: {'PASS' if conserved else 'FAIL'} "
              f"(max relative error: {err:.2e})")


class IDTModel:
    """
    Complete IDT cosmological model.
    
    Combines ΛCDM baseline with one or more IDT domain components.
    Provides all functions needed for CLASS integration.
    """
    
    def __init__(self, domains=None, H0=67.36, Omega_m=0.3153,
                 Omega_b=0.0493, Omega_r=9.1e-5):
        """
        Parameters
        ----------
        domains : list of IDTDomain
            Domain components to include.
        H0 : float
            Hubble constant in km/s/Mpc.
        Omega_m : float
            Total matter density parameter.
        Omega_b : float
            Baryon density parameter.
        Omega_r : float
            Radiation density parameter.
        """
        self.domains = domains or []
        self.H0 = H0
        self.Omega_m = Omega_m
        self.Omega_b = Omega_b
        self.Omega_r = Omega_r
        self.Omega_Lambda = 1.0 - Omega_m - Omega_r
        # Note: Omega_Lambda should be adjusted to maintain flatness
        # when domains are present. For small f_dom, the correction
        # is negligible at z=0 since domains have decayed.
    
    def E2(self, z):
        """(H/H₀)² including all domain contributions."""
        z = np.asarray(z, dtype=float)
        result = (self.Omega_m * (1+z)**3 
                 + self.Omega_r * (1+z)**4 
                 + self.Omega_Lambda)
        for d in self.domains:
            result = result + d.Omega(z)
        return result
    
    def H(self, z):
        """Hubble parameter H(z) in km/s/Mpc."""
        return self.H0 * np.sqrt(np.maximum(self.E2(z), 0))
    
    def n_domains(self):
        """Number of domain components."""
        return len(self.domains)
    
    def n_free_params(self):
        """
        Number of free parameters beyond ΛCDM.
        Each domain: f_dom, z_c, delta_z (c_s2 fixed).
        """
        return 3 * len(self.domains)
    
    def summary(self):
        """Print full model summary."""
        print(f"IDT Cosmological Model")
        print(f"======================")
        print(f"  H₀     = {self.H0} km/s/Mpc")
        print(f"  Ω_m    = {self.Omega_m}")
        print(f"  Ω_b    = {self.Omega_b}")
        print(f"  Ω_r    = {self.Omega_r}")
        print(f"  Ω_Λ    = {self.Omega_Lambda}")
        print(f"  Domains: {len(self.domains)}")
        print(f"  Extra free params: {self.n_free_params()}")
        print()
        for i, d in enumerate(self.domains):
            print(f"  --- Domain {i+1} ---")
            d.summary()
            print()
