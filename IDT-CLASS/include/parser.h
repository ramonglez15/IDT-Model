/**
 * Parser Module for Enhanced IDT
 * 
 * This is a simplified version of the parser module for the Enhanced
 * Inflationary Domain Theory (IDT) with Hidden Regions.
 * 
 * @author IDT-CLASS Team
 * @date March 2025
 */

#ifndef __PARSER_IDT__
#define __PARSER_IDT__

#include "common.h"

/* Function prototypes */
int parser_read_double(
                      struct file_content * pfc,
                      char * name,
                      double * value,
                      int * flag,
                      ErrorMsg errmsg
                      );

int parser_read_int(
                   struct file_content * pfc,
                   char * name,
                   int * value,
                   int * flag,
                   ErrorMsg errmsg
                   );

int parser_read_bool(
                    struct file_content * pfc,
                    char * name,
                    int * value,
                    int * flag,
                    ErrorMsg errmsg
                    );

int parser_read_string(
                      struct file_content * pfc,
                      char * name,
                      char * value,
                      int * flag,
                      ErrorMsg errmsg
                      );

int parser_read_list_of_doubles(
                               struct file_content * pfc,
                               char * name,
                               int * size,
                               double ** pointer_to_list,
                               int * flag,
                               ErrorMsg errmsg
                               );

int parser_read_list_of_integers(
                                struct file_content * pfc,
                                char * name,
                                int * size,
                                int ** pointer_to_list,
                                int * flag,
                                ErrorMsg errmsg
                                );

#endif /* __PARSER_IDT__ */
