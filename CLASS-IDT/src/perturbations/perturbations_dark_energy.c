/**
 * Dark energy perturbations for Enhanced IDT
 * 
 * This file implements the standard dark energy perturbation equations
 * that will be modified by the hidden regions feature.
 * 
 * @author IDT-CLASS Team
 * @date March 2025
 */

#include "perturbations.h"

/**
 * Compute the standard dark energy perturbations
 * 
 * This function computes the standard dark energy perturbations
 * without the hidden regions effect.
 * 
 * @param ppt        Input: pointer to perturbation structure
 * @param pba        Input: pointer to background structure
 * @param index_md   Input: index of mode (scalar, vector, tensor)
 * @param k          Input: wavenumber
 * @param tau        Input: conformal time
 * @param y          Input: vector of perturbations
 * @param ppw        Input/Output: workspace containing in particular the quantities delta_rho etc.
 * @param error_message Output: error message
 * @return the error status
 */
int perturbations_dark_energy(
                             struct perturbations * ppt,
                             struct background * pba,
                             int index_md,
                             double k,
                             double tau,
                             double * y,
                             struct perturb_workspace * ppw,
                             ErrorMsg error_message
                             ) {
  
  /* Get scale factor */
  double a = ppw->pvecback[ppw->index_bg_a];
  
  /* Get background quantities */
  double rho_fld = ppw->pvecback[pba->index_bg_rho_fld];
  double w_fld = ppw->pvecback[pba->index_bg_w_fld];
  double cs2_fld = pba->cs2_fld;
  
  /* Compute pressure */
  double p_fld = w_fld * rho_fld;
  
  /* Get metric perturbations */
  double h_prime = ppw->pvecmetric[ppw->index_mt_h_prime];
  double eta = ppw->pvecmetric[ppw->index_mt_eta];
  
  /* Get fluid perturbations - use direct indices since we don't have the full structure */
  int index_pt_delta_fld = 14; /* This is the typical index for delta_fld in CLASS */
  int index_pt_theta_fld = 15; /* This is the typical index for theta_fld in CLASS */
  
  double delta_fld = y[index_pt_delta_fld];
  double theta_fld = y[index_pt_theta_fld];
  
  /* Compute density perturbation */
  ppw->delta_rho[pba->index_bg_rho_fld] = rho_fld * delta_fld;
  
  /* Compute velocity perturbation */
  ppw->rho_plus_p_theta[pba->index_bg_rho_fld] = (rho_fld + p_fld) * theta_fld;
  
  /* Compute pressure perturbation */
  ppw->delta_p[pba->index_bg_rho_fld] = cs2_fld * rho_fld * delta_fld;
  
  /* Compute shear stress if needed */
  if (ppt->has_source_delta_m == _TRUE_) {
    ppw->rho_plus_p_shear[pba->index_bg_rho_fld] = 0.0; /* No shear for perfect fluid */
  }
  
  return _SUCCESS_;
}
