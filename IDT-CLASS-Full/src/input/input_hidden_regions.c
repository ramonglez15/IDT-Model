/**
 * Input module for hidden regions parameters
 * 
 * This file contains the functions to read and process hidden regions parameters
 * from the configuration file for the Enhanced Inflationary Domain Theory (IDT) model.
 */

#include "input.h"
#include "background.h"
#include "hidden_regions.h"

/**
 * Read hidden regions parameters from the configuration file.
 * 
 * @param pfc        Input: pointer to file content
 * @param pba        Input/Output: pointer to background structure
 * @param errmsg     Output: error message
 * @return the error status
 */
int input_read_hidden_regions_parameters(
                                        struct file_content * pfc,
                                        struct background * pba,
                                        ErrorMsg errmsg
                                        ) {
  
  int flag;
  
  /* Check if hidden region is enabled */
  class_call(parser_read_bool(pfc, "hidden_region", &flag, &(pba->hr.has_hidden_region), errmsg),
             errmsg,
             errmsg);
  
  /* If hidden region is enabled, read the parameters */
  if (pba->hr.has_hidden_region == _TRUE_) {
    
    /* Read the redshift of the hidden region transition */
    class_call(parser_read_double(pfc, "z_hidden_region", &(pba->hr.z_transition), &flag, errmsg),
               errmsg,
               errmsg);
    
    /* If not specified, use the default value */
    if (flag == _FALSE_) {
      pba->hr.z_transition = 0.35; /* Default value */
    }
    
    /* Read the amplitude of the hidden region effect */
    class_call(parser_read_double(pfc, "amplitude_hidden_region", &(pba->hr.amplitude), &flag, errmsg),
               errmsg,
               errmsg);
    
    /* If not specified, use the default value */
    if (flag == _FALSE_) {
      pba->hr.amplitude = 0.05; /* Default value */
    }
    
    /* Read the width of the hidden region transition */
    class_call(parser_read_double(pfc, "width_hidden_region", &(pba->hr.width), &flag, errmsg),
               errmsg,
               errmsg);
    
    /* If not specified, use the default value */
    if (flag == _FALSE_) {
      pba->hr.width = 0.1; /* Default value */
    }
    
    /* Set the verbosity level */
    class_call(parser_read_int(pfc, "hidden_region_verbose", &(pba->hr.hidden_regions_verbose), &flag, errmsg),
               errmsg,
               errmsg);
    
    /* If not specified, use the same verbosity as background */
    if (flag == _FALSE_) {
      pba->hr.hidden_regions_verbose = pba->background_verbose;
    }
    
    /* Print information if verbose */
    if (pba->hr.hidden_regions_verbose > 0) {
      printf("-> Hidden region enabled with parameters:\n");
      printf("   z_transition = %f\n", pba->hr.z_transition);
      printf("   amplitude = %f\n", pba->hr.amplitude);
      printf("   width = %f\n", pba->hr.width);
    }
  }
  else {
    /* If hidden region is disabled, set default values */
    pba->hr.z_transition = 0.0;
    pba->hr.amplitude = 0.0;
    pba->hr.width = 0.0;
    pba->hr.hidden_regions_verbose = 0;
    
    /* Print information if verbose */
    if (pba->background_verbose > 0) {
      printf("-> Hidden region disabled\n");
    }
  }
  
  return _SUCCESS_;
}

/**
 * Initialize the hidden regions structure after reading parameters.
 * 
 * @param ppr        Input: pointer to precision structure
 * @param pba        Input/Output: pointer to background structure
 * @param errmsg     Output: error message
 * @return the error status
 */
int input_initialize_hidden_regions(
                                   struct precision * ppr,
                                   struct background * pba,
                                   ErrorMsg errmsg
                                   ) {
  
  /* Initialize the hidden regions structure */
  class_call(hidden_regions_init(ppr, pba, &(pba->hr), errmsg),
             errmsg,
             errmsg);
  
  return _SUCCESS_;
}
