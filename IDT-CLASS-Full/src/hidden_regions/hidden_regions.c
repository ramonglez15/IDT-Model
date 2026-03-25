/**
 * Hidden Regions Module Implementation for Enhanced IDT
 * 
 * This file implements the hidden regions feature for the Enhanced
 * Inflationary Domain Theory (IDT) model.
 * 
 * @author IDT-CLASS Team
 * @date March 2025
 */

#include "hidden_regions.h"
#include <math.h>
#include <stdio.h>

/**
 * Initialize the hidden regions structure
 * 
 * @param phr           Input/Output: pointer to hidden regions structure
 * @param error_message Output: error message
 * @return the error status
 */
int hidden_regions_init(
                       struct hidden_regions * phr,
                       ErrorMsg error_message
                       ) {
  
  /* Check if hidden regions structure exists */
  if (phr == NULL) {
    sprintf(error_message, "Hidden regions structure not allocated");
    return _FAILURE_;
  }
  
  /* Set default values if not already set */
  if (phr->has_hidden_region == _TRUE_) {
    
    /* Check if transition redshift is set */
    if (phr->z_transition <= 0.0) {
      phr->z_transition = 0.35; /* Default value */
      if (phr->hidden_regions_verbose > 0) {
        printf("Hidden regions: using default transition redshift z = %f\n", phr->z_transition);
      }
    }
    
    /* Check if amplitude is set */
    if (phr->amplitude <= 0.0) {
      phr->amplitude = 0.05; /* Default value */
      if (phr->hidden_regions_verbose > 0) {
        printf("Hidden regions: using default amplitude = %f\n", phr->amplitude);
      }
    }
    
    /* Check if width is set */
    if (phr->width <= 0.0) {
      phr->width = 0.1; /* Default value */
      if (phr->hidden_regions_verbose > 0) {
        printf("Hidden regions: using default width = %f\n", phr->width);
      }
    }
    
    /* Print info if verbose */
    if (phr->hidden_regions_verbose > 0) {
      printf("Hidden regions: enabled with transition at z = %f, amplitude = %f, width = %f\n",
             phr->z_transition, phr->amplitude, phr->width);
    }
  }
  else {
    if (phr->hidden_regions_verbose > 0) {
      printf("Hidden regions: disabled\n");
    }
  }
  
  return _SUCCESS_;
}

/**
 * Free the hidden regions structure
 * 
 * @param phr           Input/Output: pointer to hidden regions structure
 * @return the error status
 */
int hidden_regions_free(
                       struct hidden_regions * phr
                       ) {
  
  /* Nothing to free for now */
  
  return _SUCCESS_;
}

/**
 * Compute the hidden region transition effect
 * 
 * This function computes the effect of the hidden region transition
 * at a given redshift, using a tanh function.
 * 
 * @param phr           Input: pointer to hidden regions structure
 * @param z             Input: redshift
 * @param effect        Output: transition effect (0 to 1)
 * @param deffect_dz    Output: derivative of effect with respect to z
 * @param error_message Output: error message
 * @return the error status
 */
int hidden_regions_transition_effect(
                                    struct hidden_regions * phr,
                                    double z,
                                    double * effect,
                                    double * deffect_dz,
                                    ErrorMsg error_message
                                    ) {
  
  /* Check if hidden region is enabled */
  if (phr->has_hidden_region == _FALSE_) {
    *effect = 0.0;
    if (deffect_dz != NULL) {
      *deffect_dz = 0.0;
    }
    return _SUCCESS_;
  }
  
  /* Compute the transition effect using tanh function */
  /* Effect goes from 0 (at high z) to 1 (at low z) */
  *effect = 0.5 * (1.0 - tanh((z - phr->z_transition) / phr->width));
  
  /* Compute derivative if requested */
  if (deffect_dz != NULL) {
    /* Derivative of tanh(x) is sech^2(x) = 1 - tanh^2(x) */
    double sech2 = 1.0 - tanh((z - phr->z_transition) / phr->width) * 
                         tanh((z - phr->z_transition) / phr->width);
    *deffect_dz = -0.5 * sech2 / phr->width;
  }
  
  /* Print info if verbose */
  if (phr->hidden_regions_verbose > 1) {
    printf("Hidden regions: at z = %f, effect = %f\n", z, *effect);
    if (deffect_dz != NULL) {
      printf("Hidden regions: at z = %f, deffect_dz = %f\n", z, *deffect_dz);
    }
  }
  
  return _SUCCESS_;
}
