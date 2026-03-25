/**
 * Precision Module for Enhanced IDT
 * 
 * This is a simplified version of the precision module for the Enhanced
 * Inflationary Domain Theory (IDT) with Hidden Regions.
 * 
 * @author IDT-CLASS Team
 * @date March 2025
 */

#ifndef __PRECISION_IDT__
#define __PRECISION_IDT__

#include "common.h"

/**
 * Structure containing all precision parameters.
 *
 * Precision parameters are parameters controlling the precision of the
 * output. They are not related to the physics of the model, but to the
 * way in which the code computes the results. They mainly control the
 * precision of the various integration routines and of the approximation
 * schemes.
 */
struct precision {

  /** @name - background integration parameters */
  //@{

  double background_integration_stepsize; /**< integration step in terms of the scale factor */
  double tol_background_integration; /**< tolerance for background integration */
  double tol_initial_Omega_r; /**< tolerance on initial radiation density (recommended: 1e-4) */
  double tol_M_ncdm; /**< tolerance on ncdm mass in eV (recommended: 1e-7) */
  double tol_ncdm; /**< tolerance on ncdm density (recommended: 1e-3) */
  double tol_ncdm_synchronous; /**< tolerance on ncdm density (recommended: 1e-3) */
  double tol_ncdm_newtonian; /**< tolerance on ncdm density (recommended: 1e-5) */
  double tol_ncdm_bg; /**< tolerance on ncdm density in background (recommended: 1e-5) */
  double tol_ncdm_initial_w; /**< tolerance on ncdm initial equation of state (recommended: 1e-3) */

  //@}

  /** @name - hidden regions parameters */
  //@{

  double tol_hidden_regions; /**< tolerance for hidden regions calculations */
  double hidden_regions_integration_stepsize; /**< integration step for hidden regions */

  //@}
};

#endif /* __PRECISION_IDT__ */
