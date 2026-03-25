/**
 * Background Module for Enhanced IDT
 * 
 * This is a modified version of the CLASS background module that includes
 * support for the Enhanced Inflationary Domain Theory (IDT) with Hidden Regions.
 * 
 * @author IDT-CLASS Team
 * @date March 2025
 */

#ifndef __BACKGROUND__
#define __BACKGROUND__

#include "common.h"
#include "hidden_regions.h"

/**
 * Structure containing all background parameters and variables.
 */
struct background {

  /** @name - input parameters initialized by user in input module
   *  (all other quantities are computed in this module, given these parameters
   *   and the content of the 'precision' structure)
   */

  //@{

  double H0; /**< Hubble parameter today in Km/s/Mpc */
  double h;  /**< reduced Hubble parameter */
  double Omega0_g; /**< photon density parameter */
  double T_cmb; /**< CMB temperature in K */
  double Omega0_b; /**< baryon density parameter */
  double Omega0_cdm; /**< cold dark matter density parameter */
  double Omega0_lambda; /**< cosmological constant density parameter */
  double Omega0_fld; /**< fluid with constant w density parameter */
  double w0_fld; /**< fluid equation of state parameter */
  double wa_fld; /**< fluid equation of state parameter (CPL parametrization) */
  double cs2_fld; /**< sound speed of the fluid in the fluid rest frame */
  double Omega0_ur; /**< ultra-relativistic neutrinos/relics density parameter */
  double Omega0_dcdmdr; /**< dcdm and dr density parameter */
  double Omega0_scf; /**< scalar field density parameter */
  double Omega0_k; /**< curvature density parameter */
  double Omega0_m; /**< total matter density parameter (including non-cold relics) */
  double a_today; /**< scale factor today (arbitrary and irrelevant for most purposes) */

  /* Hidden regions structure */
  struct hidden_regions hr; /**< hidden regions parameters */

  //@}

  /** @name - useful parameters derived from the input parameters */

  //@{

  double age; /**< age in Gyears */
  double conformal_age; /**< conformal age in Mpc */
  double K; /**< curvature parameter K=-Omega0_k*a_today^2*H0^2; */
  double Neff; /**< total effective neutrino number (including ur species) */
  double Omega0_dcdm; /**< decaying cold dark matter density parameter */
  double Omega0_dr; /**< decay radiation density parameter */
  double Omega0_ncdm_tot; /**< total non-cold dark matter density parameter */
  double Omega0_tot; /**< total density parameter */

  //@}

  /** @name - technical parameters */

  //@{

  short background_verbose; /**< flag regulating the amount of information sent to standard output (none if set to zero) */
  ErrorMsg error_message; /**< zone for writing error messages */

  //@}

  /** @name - indices for different quantities */

  //@{

  int index_bg_a;             /**< scale factor */
  int index_bg_H;             /**< Hubble parameter in \f$ Mpc^{-1} \f$ */
  int index_bg_H_prime;       /**< derivative of Hubble parameter wrt conformal time */
  int index_bg_rho_g;         /**< photon density */
  int index_bg_rho_b;         /**< baryon density */
  int index_bg_rho_cdm;       /**< cdm density */
  int index_bg_rho_lambda;    /**< cosmological constant density */
  int index_bg_rho_fld;       /**< fluid with constant w density */
  int index_bg_w_fld;         /**< fluid equation of state */
  int index_bg_rho_ur;        /**< relativistic neutrinos/relics density */
  int index_bg_rho_dcdm;      /**< dcdm density */
  int index_bg_rho_dr;        /**< dr density */
  int index_bg_rho_scf;       /**< scalar field density */
  int index_bg_p_scf;         /**< scalar field pressure */
  int index_bg_phi_scf;       /**< scalar field value */
  int index_bg_phi_prime_scf; /**< scalar field derivative wrt conformal time */
  int index_bg_rho_ncdm1;     /**< density of first ncdm species (others contiguous) */
  int index_bg_p_ncdm1;       /**< pressure of first ncdm species (others contiguous) */
  int index_bg_pseudo_p_ncdm1;/**< another statistical momentum useful in ncdma approximation */
  int index_bg_rho_tot;       /**< total density */
  int index_bg_p_tot;         /**< total pressure */
  int index_bg_p_tot_prime;   /**< derivative of total pressure wrt conformal time */
  int index_bg_Omega_r;       /**< relativistic density fraction (\f$ \Omega_{\gamma} + \Omega_{\nu r} \f$) */
  int index_bg_z;             /**< redshift */
  int index_bg_tau;           /**< conformal time in Mpc */
  int index_bg_D;             /**< scale independent growth factor */
  int index_bg_f;             /**< scale independent growth rate */

  int bg_size; /**< size of background vector */

  //@}

  /** @name - background interpolation tables */

  //@{

  int bt_size;               /**< number of lines (redshift steps) in the array */
  double * tau_table;        /**< vector tau_table[index_tau] with values of conformal time (in Mpc) */
  double * z_table;          /**< vector z_table[index_tau] with values of redshift */
  double * background_table; /**< table background_table[index_tau*pba->bg_size+pba->index_bg] with all other quantities (array of size bg_size*bt_size) **/

  //@}

};

/* Function prototypes */
int background_w_fld(
                    struct background * pba,
                    double a,
                    double * w_fld,
                    double * dw_over_da_fld,
                    double * integral_fld
                    );

int background_w_fld_with_hidden_regions(
                                        struct background * pba,
                                        double a,
                                        double * w_fld,
                                        double * dw_over_da_fld,
                                        double * integral_fld
                                        );

#endif /* __BACKGROUND__ */
