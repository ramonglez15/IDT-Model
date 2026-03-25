/**
 * Dark energy equation of state with hidden regions for Enhanced IDT
 * 
 * This file implements the dark energy equation of state with hidden regions
 * for the Enhanced Inflationary Domain Theory (IDT) model.
 * 
 * @author IDT-CLASS Team
 * @date March 2025
 */

#include "background.h"
#include <math.h>
#include <stdio.h>

/**
 * Compute the standard dark energy equation of state
 * 
 * This function computes the standard CPL parametrization for the
 * dark energy equation of state: w(a) = w0 + wa * (1-a)
 * 
 * @param pba           Input: pointer to background structure
 * @param a             Input: scale factor
 * @param w_fld         Output: equation of state
 * @param dw_over_da_fld Output: derivative of equation of state wrt scale factor
 * @param integral_fld  Output: integral of equation of state
 * @return the error status
 */
int background_w_fld(
                    struct background * pba,
                    double a,
                    double * w_fld,
                    double * dw_over_da_fld,
                    double * integral_fld
                    ) {
  
  /* CPL parametrization: w(a) = w0 + wa * (1-a) */
  *w_fld = pba->w0_fld + pba->wa_fld * (1.0 - a);
  
  /* Compute derivative if requested */
  if (dw_over_da_fld != NULL) {
    *dw_over_da_fld = -pba->wa_fld;
  }
  
  /* Compute integral if requested */
  if (integral_fld != NULL) {
    /* Integral of w(a) from a to 1:
     * int_a^1 [w0 + wa*(1-a')]/a' da'
     * = w0 * ln(1/a) + wa * (1 - a + ln(a))
     */
    *integral_fld = pba->w0_fld * log(1.0/a) + pba->wa_fld * (1.0 - a + log(a));
  }
  
  return _SUCCESS_;
}

/**
 * Compute the dark energy equation of state with hidden regions
 * 
 * This function modifies the standard dark energy equation of state
 * to include the effects of hidden regions.
 * 
 * @param pba           Input: pointer to background structure
 * @param a             Input: scale factor
 * @param w_fld         Output: equation of state
 * @param dw_over_da_fld Output: derivative of equation of state wrt scale factor
 * @param integral_fld  Output: integral of equation of state
 * @return the error status
 */
int background_w_fld_with_hidden_regions(
                                        struct background * pba,
                                        double a,
                                        double * w_fld,
                                        double * dw_over_da_fld,
                                        double * integral_fld
                                        ) {
  
  /* First get the standard w_fld */
  int status = background_w_fld(pba, a, w_fld, dw_over_da_fld, integral_fld);
  if (status != _SUCCESS_) {
    return status;
  }
  
  /* If hidden region is enabled, modify w_fld */
  if (pba->hr.has_hidden_region == _TRUE_) {
    
    /* Calculate redshift */
    double z = 1.0/a - 1.0;
    
    /* Get the hidden region effect */
    double effect, deffect_dz;
    status = hidden_regions_transition_effect(&(pba->hr), z, &effect, &deffect_dz, pba->error_message);
    if (status != _SUCCESS_) {
      return status;
    }
    
    /* Modify w_fld */
    *w_fld = *w_fld - pba->hr.amplitude * effect;
    
    /* Modify derivative if needed */
    if (dw_over_da_fld != NULL) {
      /* Chain rule: dw/da = dw/dz * dz/da */
      double dz_da = -1.0/(a*a);
      *dw_over_da_fld = *dw_over_da_fld - pba->hr.amplitude * deffect_dz * dz_da;
    }
    
    /* Modify integral if needed */
    if (integral_fld != NULL) {
      /* This is an approximation; for exact results, numerical integration would be needed */
      *integral_fld = *integral_fld - pba->hr.amplitude * effect * log(a);
    }
    
    /* Print info if verbose */
    if (pba->hr.hidden_regions_verbose > 1) {
      printf("Hidden regions: at a = %f (z = %f), w_fld = %f\n", a, z, *w_fld);
      if (dw_over_da_fld != NULL) {
        printf("Hidden regions: at a = %f (z = %f), dw_over_da_fld = %f\n", a, z, *dw_over_da_fld);
      }
    }
  }
  
  return _SUCCESS_;
}
