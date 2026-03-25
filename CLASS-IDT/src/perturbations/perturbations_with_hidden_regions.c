/**
 * Perturbations module with hidden regions support for Enhanced IDT
 * 
 * This file implements the perturbation equations for the Enhanced
 * Inflationary Domain Theory (IDT) with Hidden Regions model.
 * 
 * @author IDT-CLASS Team
 * @date March 2025
 */

#include "perturbations.h"
#include "hidden_regions.h"

/**
 * Compute the perturbation equations for dark energy with hidden regions
 * 
 * This function modifies the standard perturbation equations for dark energy
 * to account for the effects of hidden regions.
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
int perturbations_dark_energy_with_hidden_regions(
                                                struct perturbations * ppt,
                                                struct background * pba,
                                                int index_md,
                                                double k,
                                                double tau,
                                                double * y,
                                                struct perturb_workspace * ppw,
                                                ErrorMsg error_message
                                                ) {
  
  /* First call the standard dark energy perturbation function */
  class_call(perturbations_dark_energy(ppt, pba, index_md, k, tau, y, ppw, error_message),
             error_message,
             error_message);
  
  /* If hidden region is enabled, modify the dark energy perturbations */
  if (pba->hr.has_hidden_region == _TRUE_) {
    
    /* Get scale factor */
    double a = pba->a_today / (1.0 + ppw->pvecback[pba->index_bg_z]);
    
    /* Calculate the hidden region effect */
    double z = 1.0/a - 1.0;
    double transition = 0.5 * (1.0 - tanh((z - pba->hr.z_transition) / pba->hr.width));
    
    /* Modification factor for dark energy perturbations */
    double modification_factor = 1.0 + pba->hr.amplitude * transition;
    
    /* Apply modification to dark energy density perturbation */
    ppw->delta_rho[pba->index_bg_rho_fld] *= modification_factor;
    
    /* Apply modification to dark energy velocity perturbation */
    ppw->rho_plus_p_theta[pba->index_bg_rho_fld] *= modification_factor;
    
    /* Apply modification to dark energy pressure perturbation */
    ppw->delta_p[pba->index_bg_rho_fld] *= modification_factor;
    
    /* Apply modification to dark energy shear stress */
    if (ppt->has_source_delta_m == _TRUE_) {
      ppw->rho_plus_p_shear[pba->index_bg_rho_fld] *= modification_factor;
    }
    
    /* Verbose output if requested */
    if (pba->hr.hidden_regions_verbose > 1) {
      printf("Hidden region effect on DE perturbations at z=%f: factor=%f\n", 
             z, modification_factor);
    }
  }
  
  return _SUCCESS_;
}

/**
 * Compute the effective sound speed for dark energy with hidden regions
 * 
 * This function modifies the standard effective sound speed for dark energy
 * to account for the effects of hidden regions.
 * 
 * @param pba        Input: pointer to background structure
 * @param a          Input: scale factor
 * @param cs2        Input/Output: sound speed squared
 * @return the error status
 */
int perturbations_effective_cs2_with_hidden_regions(
                                                  struct background * pba,
                                                  double a,
                                                  double * cs2
                                                  ) {
  
  /* If hidden region is enabled, modify the effective sound speed */
  if (pba->hr.has_hidden_region == _TRUE_) {
    
    /* Calculate the hidden region effect */
    double z = 1.0/a - 1.0;
    double transition = 0.5 * (1.0 - tanh((z - pba->hr.z_transition) / pba->hr.width));
    
    /* Modification to sound speed */
    /* We reduce the sound speed near the transition to allow for clustering */
    double cs2_modification = 1.0 - 0.5 * pba->hr.amplitude * transition;
    
    /* Apply modification, ensuring cs2 remains positive */
    *cs2 = (*cs2) * cs2_modification;
    if (*cs2 < 1.0e-6) *cs2 = 1.0e-6;
    
    /* Verbose output if requested */
    if (pba->hr.hidden_regions_verbose > 1) {
      printf("Hidden region effect on DE sound speed at z=%f: cs2=%e\n", 
             z, *cs2);
    }
  }
  
  return _SUCCESS_;
}

/**
 * Compute the growth rate with hidden regions effects
 * 
 * This function calculates the growth rate f = d ln D / d ln a
 * with modifications due to hidden regions.
 * 
 * @param pba        Input: pointer to background structure
 * @param a          Input: scale factor
 * @param growth_rate Output: growth rate f
 * @return the error status
 */
int perturbations_growth_rate_with_hidden_regions(
                                                struct background * pba,
                                                double a,
                                                double * growth_rate
                                                ) {
  
  /* Calculate standard growth rate approximation */
  double Omega_m_a = pba->Omega0_m / (pba->Omega0_m + (1.0 - pba->Omega0_m) * pow(a, -3.0 * pba->w0_fld));
  *growth_rate = pow(Omega_m_a, 0.55); /* Standard LCDM approximation */
  
  /* If hidden region is enabled, modify the growth rate */
  if (pba->hr.has_hidden_region == _TRUE_) {
    
    /* Calculate the hidden region effect */
    double z = 1.0/a - 1.0;
    double transition = 0.5 * (1.0 - tanh((z - pba->hr.z_transition) / pba->hr.width));
    
    /* Modification to growth rate */
    /* We reduce the growth rate after the transition to match observed sigma8 */
    double growth_modification = 1.0 - 0.3 * pba->hr.amplitude * transition;
    
    /* Apply modification */
    *growth_rate *= growth_modification;
    
    /* Verbose output if requested */
    if (pba->hr.hidden_regions_verbose > 1) {
      printf("Hidden region effect on growth rate at z=%f: f=%f\n", 
             z, *growth_rate);
    }
  }
  
  return _SUCCESS_;
}
