/**
 * Main program for Enhanced Inflationary Domain Theory (IDT) with Hidden Regions
 * 
 * This is the main entry point for the IDT-CLASS code, which implements
 * the Enhanced Inflationary Domain Theory (IDT) with Hidden Regions as
 * an extension to the CLASS cosmological code.
 * 
 * @author IDT-CLASS Team
 * @date March 2025
 */

#include "common.h"
#include "parser.h"
#include "background.h"
#include "hidden_regions.h"
#include "input.h"
#include "precision.h"

int main(int argc, char **argv) {
  
  struct precision pr;        /* precision parameters */
  struct background ba;       /* background structure */
  struct file_content fc;     /* file content structure */
  ErrorMsg errmsg;            /* error message */
  
  /* If no arguments are provided, print usage */
  if (argc < 2) {
    printf("Usage: %s <input_file>\n", argv[0]);
    printf("  <input_file>: path to the input file (e.g., config/enhanced_model.ini)\n");
    return _FAILURE_;
  }
  
  /* Initialize structures */
  memset(&pr, 0, sizeof(struct precision));
  memset(&ba, 0, sizeof(struct background));
  memset(&fc, 0, sizeof(struct file_content));
  
  /* Set default precision parameters */
  pr.background_integration_stepsize = 7.0e-3;
  pr.tol_background_integration = 1.0e-2;
  pr.tol_initial_Omega_r = 1.0e-4;
  pr.tol_M_ncdm = 1.0e-7;
  pr.tol_ncdm = 1.0e-3;
  pr.tol_ncdm_synchronous = 1.0e-3;
  pr.tol_ncdm_newtonian = 1.0e-5;
  pr.tol_ncdm_bg = 1.0e-5;
  pr.tol_ncdm_initial_w = 1.0e-3;
  pr.tol_hidden_regions = 1.0e-4;
  pr.hidden_regions_integration_stepsize = 1.0e-3;
  
  /* Read input file */
  printf("Reading input file: %s\n", argv[1]);
  
  /* Parse input file (simplified) */
  fc.filename = argv[1];
  
  /* Read hidden regions parameters */
  printf("Reading hidden regions parameters...\n");
  if (input_read_hidden_regions_parameters(&fc, &ba, errmsg) == _FAILURE_) {
    printf("Error reading hidden regions parameters: %s\n", errmsg);
    return _FAILURE_;
  }
  
  /* Initialize hidden regions */
  printf("Initializing hidden regions...\n");
  if (input_initialize_hidden_regions(&pr, &ba, errmsg) == _FAILURE_) {
    printf("Error initializing hidden regions: %s\n", errmsg);
    return _FAILURE_;
  }
  
  /* Print hidden regions parameters */
  printf("\nHidden Regions Parameters:\n");
  printf("  Enabled: %s\n", ba.hr.has_hidden_region ? "Yes" : "No");
  if (ba.hr.has_hidden_region) {
    printf("  Transition redshift: z = %.4f\n", ba.hr.z_transition);
    printf("  Amplitude: %.4f\n", ba.hr.amplitude);
    printf("  Width: %.4f\n", ba.hr.width);
  }
  
  /* Test the equation of state with hidden regions */
  printf("\nTesting dark energy equation of state with hidden regions:\n");
  printf("  Scale Factor (a)   |   w(a)   |   w_eff(a)\n");
  printf("------------------------------------------\n");
  
  /* Loop over scale factors */
  for (double a = 0.1; a <= 1.0; a += 0.1) {
    double w_fld = 0.0;
    double dw_over_da_fld = 0.0;
    double integral_fld = 0.0;
    
    /* Standard w_fld */
    background_w_fld(&ba, a, &w_fld, &dw_over_da_fld, &integral_fld);
    
    /* w_fld with hidden regions */
    double w_fld_hr = w_fld;
    double dw_over_da_fld_hr = dw_over_da_fld;
    double integral_fld_hr = integral_fld;
    background_w_fld_with_hidden_regions(&ba, a, &w_fld_hr, &dw_over_da_fld_hr, &integral_fld_hr);
    
    printf("      %.2f         |  %.4f  |  %.4f\n", a, w_fld, w_fld_hr);
  }
  
  printf("\nEnhanced Inflationary Domain Theory (IDT) with Hidden Regions\n");
  printf("Model parameters successfully loaded and tested.\n");
  
  return _SUCCESS_;
}
