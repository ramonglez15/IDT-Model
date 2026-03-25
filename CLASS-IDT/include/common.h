/**
 * Common definitions for Enhanced IDT
 * 
 * This file contains common definitions and macros used throughout
 * the Enhanced Inflationary Domain Theory (IDT) code.
 * 
 * @author IDT-CLASS Team
 * @date March 2025
 */

#ifndef __COMMON__
#define __COMMON__

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>

/* Error handling */
#define _ERRORMSGSIZE_ 2048
typedef char ErrorMsg[_ERRORMSGSIZE_];

/* Precision parameters */
typedef double precision;

/* Useful constants */
#define _PI_ 3.1415926535897932384626433832795
#define _SQRT2_ 1.4142135623730950488016887242097
#define _E_ 2.7182818284590452353602874713527
#define _SPEED_OF_LIGHT_ 299792458.0 /* in m/s */
#define _PARSEC_ 3.085677581282e16 /* in m */
#define _MEGAPARSEC_ 3.085677581282e22 /* in m */
#define _KILOPARSEC_ 3.085677581282e19 /* in m */
#define _SOLAR_MASS_ 1.98841e30 /* in kg */
#define _PLANCK_MASS_ 2.17651e-8 /* in kg */
#define _PLANCK_LENGTH_ 1.61625e-35 /* in m */
#define _PLANCK_TIME_ 5.39124e-44 /* in s */
#define _BOLTZMANN_ 1.38064852e-23 /* in J/K */
#define _ASTRONOMICAL_UNIT_ 1.49597870700e11 /* in m */

/* Macros for min and max */
#define MAX(a,b) (((a)>(b))?(a):(b))
#define MIN(a,b) (((a)<(b))?(a):(b))

/* Macro for absolute value */
#define ABS(a) (((a)<0)?-(a):(a))

/* Macro for sign */
#define SIGN(a) (((a)>=0)?(1):(-1))

/* Macro for square */
#define SQR(a) ((a)*(a))

/* Macro for cube */
#define CUBE(a) ((a)*(a)*(a))

/* Macro for fourth power */
#define POW4(a) ((a)*(a)*(a)*(a))

/* Macro for fifth power */
#define POW5(a) ((a)*(a)*(a)*(a)*(a))

/* Macro for sixth power */
#define POW6(a) ((a)*(a)*(a)*(a)*(a)*(a))

/* Macro for seventh power */
#define POW7(a) ((a)*(a)*(a)*(a)*(a)*(a)*(a))

/* Macro for eighth power */
#define POW8(a) ((a)*(a)*(a)*(a)*(a)*(a)*(a)*(a))

/* Macro for ninth power */
#define POW9(a) ((a)*(a)*(a)*(a)*(a)*(a)*(a)*(a)*(a))

/* Macro for tenth power */
#define POW10(a) ((a)*(a)*(a)*(a)*(a)*(a)*(a)*(a)*(a)*(a))

#endif /* __COMMON__ */
