/**
 * Input Module for Enhanced IDT
 * 
 * This is a simplified version of the input module for the Enhanced
 * Inflationary Domain Theory (IDT) with Hidden Regions.
 * 
 * @author IDT-CLASS Team
 * @date March 2025
 */

#ifndef __INPUT_IDT__
#define __INPUT_IDT__

#include "background.h"

/**
 * Structure containing the input parameters and other relevant information
 * read from the input file.
 */
struct file_content {
  int size;        /**< number of entries in the file */
  char * filename; /**< name of the input file */
  char ** name;    /**< list of parameter names */
  char ** value;   /**< list of parameter values */
  char ** read;    /**< set to "yes" if this parameter has been read */
};

/* Function prototypes */
int input_read_hidden_regions_parameters(
                                        struct file_content * pfc,
                                        struct background * pba,
                                        ErrorMsg errmsg
                                        );

int input_initialize_hidden_regions(
                                   struct precision * ppr,
                                   struct background * pba,
                                   ErrorMsg errmsg
                                   );

#endif /* __INPUT_IDT__ */
