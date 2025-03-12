/**
 * Hidden Regions Module for Enhanced IDT
 * 
 * This module implements the hidden regions feature for the Enhanced
 * Inflationary Domain Theory (IDT) model.
 * 
 * @author IDT-CLASS Team
 * @date March 2025
 */

#ifndef __HIDDEN_REGIONS__
#define __HIDDEN_REGIONS__

#include "common.h"

/**
 * Structure containing all hidden regions parameters.
 */
struct hidden_regions {
  
  short has_hidden_region;     /**< Flag indicating if hidden region is enabled */
  double z_transition;         /**< Redshift of the hidden region transition */
  double amplitude;            /**< Amplitude of the hidden region effect */
  double width;                /**< Width of the hidden region transition */
  short hidden_regions_verbose; /**< Verbosity level for hidden regions */
};

/* Success/error definitions */
#define _SUCCESS_ 0
#define _FAILURE_ 1

/* Boolean definitions */
#define _TRUE_ 1
#define _FALSE_ 0

/* Function prototypes */
int hidden_regions_init(
                       struct hidden_regions * phr,
                       ErrorMsg error_message
                       );

int hidden_regions_free(
                       struct hidden_regions * phr
                       );

int hidden_regions_transition_effect(
                                    struct hidden_regions * phr,
                                    double z,
                                    double * effect,
                                    double * deffect_dz,
                                    ErrorMsg error_message
                                    );

#endif /* __HIDDEN_REGIONS__ */
