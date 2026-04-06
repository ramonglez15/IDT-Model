"""
DESI DR1 (Year 1) BAO Distance Measurements
=============================================

Data from DESI 2024 VI: Cosmological Constraints from the Measurements
of Baryon Acoustic Oscillations (arXiv:2404.03002).

Seven redshift bins spanning 0.1 < z < 4.2, using over 6 million
extragalactic objects: BGS, LRG, ELG, QSO, and Lyman-alpha forest.

Measurement types:
  - BGS and QSO: D_V / r_d  (angle-averaged, lower S/N)
  - LRG, LRG+ELG, ELG, Lya: D_M / r_d and D_H / r_d (with correlation)

References:
  DESI 2024 III (galaxies+QSO BAO): arXiv:2404.03000
  DESI 2024 IV (Lya BAO):           arXiv:2404.03001
  DESI 2024 VI (cosmological fits):  arXiv:2404.03002
"""

import numpy as np

# ── DESI DR1 BAO measurements (Table 1 of arXiv:2404.03002) ────────────

DESI_DR1_BAO = [
    # ── BGS: isotropic measurement only ──
    {
        "tracer":   "BGS",
        "z_eff":    0.295,
        "z_range":  (0.1, 0.4),
        "N_tracers": 300_017,
        "meas_type": "DV_over_rd",
        "DV_over_rd":     7.93,
        "DV_over_rd_err": 0.15,
    },
    # ── LRG bin 1 ──
    {
        "tracer":   "LRG1",
        "z_eff":    0.510,
        "z_range":  (0.4, 0.6),
        "N_tracers": 506_905,
        "meas_type": "DM_DH",
        "DM_over_rd":     13.62,
        "DM_over_rd_err":  0.25,
        "DH_over_rd":     20.98,
        "DH_over_rd_err":  0.61,
        "corr_DM_DH":    -0.445,
    },
    # ── LRG bin 2 ──
    {
        "tracer":   "LRG2",
        "z_eff":    0.706,
        "z_range":  (0.6, 0.8),
        "N_tracers": 771_875,
        "meas_type": "DM_DH",
        "DM_over_rd":     16.85,
        "DM_over_rd_err":  0.32,
        "DH_over_rd":     20.08,
        "DH_over_rd_err":  0.60,
        "corr_DM_DH":    -0.420,
    },
    # ── LRG bin 3 + ELG bin 1 (combined) ──
    {
        "tracer":   "LRG3+ELG1",
        "z_eff":    0.930,
        "z_range":  (0.8, 1.1),
        "N_tracers": 1_876_164,
        "meas_type": "DM_DH",
        "DM_over_rd":     21.71,
        "DM_over_rd_err":  0.28,
        "DH_over_rd":     17.88,
        "DH_over_rd_err":  0.35,
        "corr_DM_DH":    -0.389,
    },
    # ── ELG bin 2 ──
    {
        "tracer":   "ELG2",
        "z_eff":    1.317,
        "z_range":  (1.1, 1.6),
        "N_tracers": 1_415_687,
        "meas_type": "DM_DH",
        "DM_over_rd":     27.79,
        "DM_over_rd_err":  0.69,
        "DH_over_rd":     13.82,
        "DH_over_rd_err":  0.42,
        "corr_DM_DH":    -0.444,
    },
    # ── QSO: isotropic measurement only ──
    {
        "tracer":   "QSO",
        "z_eff":    1.491,
        "z_range":  (0.8, 2.1),
        "N_tracers": 856_652,
        "meas_type": "DV_over_rd",
        "DV_over_rd":     26.07,
        "DV_over_rd_err":  0.67,
    },
    # ── Lyman-alpha forest ──
    {
        "tracer":   "Lya",
        "z_eff":    2.330,
        "z_range":  (1.77, 4.16),
        "N_tracers": 709_565,
        "meas_type": "DM_DH",
        "DM_over_rd":     39.71,
        "DM_over_rd_err":  0.94,
        "DH_over_rd":      8.52,
        "DH_over_rd_err":  0.17,
        "corr_DM_DH":    -0.477,
    },
]


# ── Convenience arrays for MCMC fitting ─────────────────────────────────

def get_desi_bao_arrays():
    """
    Return DESI DR1 BAO data as flat arrays suitable for chi-squared
    computation in an MCMC.

    Returns
    -------
    dict with keys:
        z_eff_DV       : array of z_eff for isotropic (D_V/r_d) measurements
        DV_over_rd     : measured D_V/r_d values
        DV_over_rd_err : 1-sigma uncertainties

        z_eff_DMDH     : array of z_eff for anisotropic measurements
        DM_over_rd     : measured D_M/r_d values
        DM_over_rd_err : 1-sigma uncertainties
        DH_over_rd     : measured D_H/r_d values
        DH_over_rd_err : 1-sigma uncertainties
        corr_DM_DH     : correlation coefficient between D_M and D_H

        cov_DMDH       : list of 2x2 covariance matrices (one per z-bin)
    """
    dv_bins = [b for b in DESI_DR1_BAO if b["meas_type"] == "DV_over_rd"]
    dm_bins = [b for b in DESI_DR1_BAO if b["meas_type"] == "DM_DH"]

    out = {}

    # Isotropic bins (BGS, QSO)
    out["z_eff_DV"]       = np.array([b["z_eff"] for b in dv_bins])
    out["DV_over_rd"]     = np.array([b["DV_over_rd"] for b in dv_bins])
    out["DV_over_rd_err"] = np.array([b["DV_over_rd_err"] for b in dv_bins])

    # Anisotropic bins (LRG1, LRG2, LRG3+ELG1, ELG2, Lya)
    out["z_eff_DMDH"]     = np.array([b["z_eff"] for b in dm_bins])
    out["DM_over_rd"]     = np.array([b["DM_over_rd"] for b in dm_bins])
    out["DM_over_rd_err"] = np.array([b["DM_over_rd_err"] for b in dm_bins])
    out["DH_over_rd"]     = np.array([b["DH_over_rd"] for b in dm_bins])
    out["DH_over_rd_err"] = np.array([b["DH_over_rd_err"] for b in dm_bins])
    out["corr_DM_DH"]     = np.array([b["corr_DM_DH"] for b in dm_bins])

    # Build 2x2 covariance matrices for each anisotropic bin
    cov_list = []
    for b in dm_bins:
        s_m = b["DM_over_rd_err"]
        s_h = b["DH_over_rd_err"]
        rho = b["corr_DM_DH"]
        cov = np.array([
            [s_m**2,         rho * s_m * s_h],
            [rho * s_m * s_h, s_h**2         ],
        ])
        cov_list.append(cov)
    out["cov_DMDH"] = cov_list

    return out


def chi2_bao_desi(theory_DV_func, theory_DM_func, theory_DH_func, r_d):
    """
    Compute chi-squared for DESI DR1 BAO given theory predictions.

    Parameters
    ----------
    theory_DV_func : callable
        DV(z) in Mpc  (angle-averaged distance)
    theory_DM_func : callable
        DM(z) in Mpc  (comoving angular diameter distance)
    theory_DH_func : callable
        DH(z) = c/H(z) in Mpc  (Hubble distance)
    r_d : float
        Sound horizon at drag epoch in Mpc.

    Returns
    -------
    chi2 : float
    """
    d = get_desi_bao_arrays()
    chi2 = 0.0

    # Isotropic bins
    for i, z in enumerate(d["z_eff_DV"]):
        pred = theory_DV_func(z) / r_d
        chi2 += ((pred - d["DV_over_rd"][i]) / d["DV_over_rd_err"][i])**2

    # Anisotropic bins (use full 2x2 covariance)
    for i, z in enumerate(d["z_eff_DMDH"]):
        pred_m = theory_DM_func(z) / r_d
        pred_h = theory_DH_func(z) / r_d
        delta = np.array([
            pred_m - d["DM_over_rd"][i],
            pred_h - d["DH_over_rd"][i],
        ])
        cov_inv = np.linalg.inv(d["cov_DMDH"][i])
        chi2 += delta @ cov_inv @ delta

    return chi2


# ── Quick sanity check ──────────────────────────────────────────────────

if __name__ == "__main__":
    print("DESI DR1 BAO Measurements (arXiv:2404.03002)")
    print("=" * 60)
    for b in DESI_DR1_BAO:
        if b["meas_type"] == "DV_over_rd":
            print(f"  {b['tracer']:12s}  z_eff={b['z_eff']:.3f}  "
                  f"D_V/r_d = {b['DV_over_rd']:.2f} +/- {b['DV_over_rd_err']:.2f}")
        else:
            print(f"  {b['tracer']:12s}  z_eff={b['z_eff']:.3f}  "
                  f"D_M/r_d = {b['DM_over_rd']:.2f} +/- {b['DM_over_rd_err']:.2f}  "
                  f"D_H/r_d = {b['DH_over_rd']:.2f} +/- {b['DH_over_rd_err']:.2f}  "
                  f"rho = {b['corr_DM_DH']:.3f}")
    print(f"\n  Total tracers: {sum(b['N_tracers'] for b in DESI_DR1_BAO):,}")
    print(f"  Redshift range: 0.1 < z < 4.2")
    print(f"  Number of z-bins: {len(DESI_DR1_BAO)}")
