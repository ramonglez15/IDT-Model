/**
 * Perturbations Module for Enhanced IDT
 * 
 * This is a modified version of the CLASS perturbations module that includes
 * support for the Enhanced Inflationary Domain Theory (IDT) with Hidden Regions.
 * 
 * @author IDT-CLASS Team
 * @date March 2025
 */

#ifndef __PERTURBATIONS__
#define __PERTURBATIONS__

#include "common.h"
#include "background.h"
#include "hidden_regions.h"

/* Define constants */
#define MD_SIZE 3  /**< Number of modes (scalar, vector, tensor) */

/**
 * Structure containing the indices and values of all perturbation variables.
 */
struct perturb_vector {
  
  int index_pt_delta_g;       /**< photon density perturbation */
  int index_pt_theta_g;       /**< photon velocity perturbation */
  int index_pt_shear_g;       /**< photon shear perturbation */
  int index_pt_pol0_g;        /**< photon polarization perturbation */
  int index_pt_pol1_g;        /**< photon polarization perturbation */
  int index_pt_pol2_g;        /**< photon polarization perturbation */
  int index_pt_delta_b;       /**< baryon density perturbation */
  int index_pt_theta_b;       /**< baryon velocity perturbation */
  int index_pt_delta_cdm;     /**< cdm density perturbation */
  int index_pt_theta_cdm;     /**< cdm velocity perturbation */
  int index_pt_delta_idm;     /**< idm density perturbation */
  int index_pt_theta_idm;     /**< idm velocity perturbation */
  int index_pt_delta_dcdm;    /**< dcdm density perturbation */
  int index_pt_theta_dcdm;    /**< dcdm velocity perturbation */
  int index_pt_delta_fld;     /**< dark energy fluid density perturbation */
  int index_pt_theta_fld;     /**< dark energy fluid velocity perturbation */
  int index_pt_delta_scf;     /**< scalar field density perturbation */
  int index_pt_theta_scf;     /**< scalar field velocity perturbation */
  int index_pt_delta_dr;      /**< decay radiation density perturbation */
  int index_pt_theta_dr;      /**< decay radiation velocity perturbation */
  int index_pt_shear_dr;      /**< decay radiation shear perturbation */
  int index_pt_delta_ur;      /**< ultra-relativistic neutrinos/relics density perturbation */
  int index_pt_theta_ur;      /**< ultra-relativistic neutrinos/relics velocity perturbation */
  int index_pt_shear_ur;      /**< ultra-relativistic neutrinos/relics shear perturbation */
  int index_pt_delta_ncdm1;   /**< first ncdm species density perturbation */
  int index_pt_theta_ncdm1;   /**< first ncdm species velocity perturbation */
  int index_pt_shear_ncdm1;   /**< first ncdm species shear perturbation */
  int index_pt_eta;           /**< metric perturbation eta */
  int index_pt_phi;           /**< metric perturbation phi */
  int index_pt_h;             /**< metric perturbation h */
  int index_pt_h_prime;       /**< metric perturbation h' */
  
  int pt_size;                /**< size of perturbation vector */
};

/**
 * Structure containing all perturbation parameters and workspace.
 */
struct perturbations {

  /** @name - input parameters initialized by user in input module
   *  (all other quantities are computed in this module, given these parameters
   *   and the content of the 'precision', 'background' and 'thermodynamics' structures) */

  //@{

  short has_perturbations;       /**< do we need to compute perturbations at all ? */

  short has_cls;                 /**< do we need to compute Cl_s ? */

  short has_scalars;             /**< do we need to compute scalar perturbations? */
  short has_vectors;             /**< do we need to compute vector perturbations? */
  short has_tensors;             /**< do we need to compute tensor perturbations? */

  short has_ad;                  /**< do we need to compute adiabatic mode? */
  short has_bi;                  /**< do we need to compute baryon isocurvature mode? */
  short has_cdi;                 /**< do we need to compute CDM isocurvature mode? */
  short has_nid;                 /**< do we need to compute neutrino density isocurvature mode? */
  short has_niv;                 /**< do we need to compute neutrino velocity isocurvature mode? */

  /* perturbed recombination */
  short has_perturbed_recombination; /**< do we need to compute perturbed recombination? */

  /* modes */
  int index_md_scalars;            /**< index for scalar modes */
  int index_md_tensors;            /**< index for tensor modes */
  int index_md_vectors;            /**< index for vector modes */

  int md_size;                     /**< number of modes included */
  int index_md_ad;                 /**< index for adiabatic mode */
  int index_md_bi;                 /**< index for BI mode */
  int index_md_cdi;                /**< index for CDI mode */
  int index_md_nid;                /**< index for NID mode */
  int index_md_niv;                /**< index for NIV mode */

  /* initial conditions */
  int ic_size[MD_SIZE];            /**< for a given mode, ic_size[index_md] = number of initial conditions included */
  int index_ic_ad[MD_SIZE];        /**< for a given mode, index of adiabatic */
  int index_ic_bi[MD_SIZE];        /**< for a given mode, index of BI */
  int index_ic_cdi[MD_SIZE];       /**< for a given mode, index of CDI */
  int index_ic_nid[MD_SIZE];       /**< for a given mode, index of NID */
  int index_ic_niv[MD_SIZE];       /**< for a given mode, index of NIV */

  /* source flags */
  short has_source_t;                /**< do we need source for temperature? */
  short has_source_p;                /**< do we need source for polarization? */
  short has_source_delta_m;          /**< do we need source for delta matter? */
  short has_source_delta_cb;         /**< do we need source for delta cb? */
  short has_source_delta_g;          /**< do we need source for delta photons? */
  short has_source_delta_b;          /**< do we need source for delta baryons? */
  short has_source_delta_cdm;        /**< do we need source for delta cold dark matter? */
  short has_source_delta_dcdm;       /**< do we need source for delta decaying cold dark matter? */
  short has_source_delta_fld;        /**< do we need source for delta dark energy? */
  short has_source_delta_scf;        /**< do we need source for delta scalar field? */
  short has_source_delta_dr;         /**< do we need source for delta decay radiation? */
  short has_source_delta_ur;         /**< do we need source for delta ultra-relativistic neutrinos/relics? */
  short has_source_delta_ncdm;       /**< do we need source for delta non-cold dark matter? */
  short has_source_theta_m;          /**< do we need source for theta matter? */
  short has_source_theta_cb;         /**< do we need source for theta cb? */
  short has_source_theta_g;          /**< do we need source for theta photons? */
  short has_source_theta_b;          /**< do we need source for theta baryons? */
  short has_source_theta_cdm;        /**< do we need source for theta cold dark matter? */
  short has_source_theta_dcdm;       /**< do we need source for theta decaying cold dark matter? */
  short has_source_theta_fld;        /**< do we need source for theta dark energy? */
  short has_source_theta_scf;        /**< do we need source for theta scalar field? */
  short has_source_theta_dr;         /**< do we need source for theta decay radiation? */
  short has_source_theta_ur;         /**< do we need source for theta ultra-relativistic neutrinos/relics? */
  short has_source_theta_ncdm;       /**< do we need source for theta non-cold dark matter? */
  short has_source_phi;              /**< do we need source for metric phi? */
  short has_source_phi_prime;        /**< do we need source for metric phi'? */
  short has_source_phi_plus_psi;     /**< do we need source for metric (phi+psi)? */
  short has_source_psi;              /**< do we need source for metric psi? */

  /* workspace */
  double *** sources;  /**< Pointer towards the source interpolation table sources[index_md][index_ic*index_type+index_tp][index_tau*ppt->k_size[index_md]+index_k] (must be freed before calling perturb_free() */

  //@}

  /** @name - technical parameters */

  //@{

  short perturbations_verbose;  /**< flag regulating the amount of information sent to standard output (none if set to zero) */

  ErrorMsg error_message; /**< zone for writing error messages */

  //@}
};

/**
 * Workspace for computing perturbation sources.
 */
struct perturb_workspace {

  /** @name - background, thermodynamics, metric quantities */

  //@{

  double * pvecback;            /**< background quantities */
  double * pvecthermo;          /**< thermodynamics quantities */
  double * pvecmetric;          /**< metric quantities */

  double * pvecback_integration; /**< background quantities for the purpose of perturbation integration */

  //@}

  /** @name - useful indices for calling background, thermodynamics, metric modules */

  //@{

  int index_bg_a;                /**< scale factor */
  int index_bg_H;                /**< Hubble parameter in \f$Mpc^{-1}\f$ */
  int index_bg_H_prime;          /**< derivative of Hubble parameter wrt conformal time */
  int index_bg_rho_g;            /**< photon density */
  int index_bg_rho_b;            /**< baryon density */
  int index_bg_rho_cdm;          /**< cdm density */
  int index_bg_rho_idm;          /**< idm density */
  int index_bg_rho_lambda;       /**< cosmological constant density */
  int index_bg_rho_fld;          /**< fluid density */
  int index_bg_w_fld;            /**< fluid equation of state */
  int index_bg_rho_ur;           /**< relativistic neutrinos/relics density */
  int index_bg_rho_dcdm;         /**< dcdm density */
  int index_bg_rho_dr;           /**< dr density */
  int index_bg_rho_scf;          /**< scalar field density */
  int index_bg_p_scf;            /**< scalar field pressure */
  int index_bg_phi_scf;          /**< scalar field value */
  int index_bg_phi_prime_scf;    /**< scalar field derivative wrt conformal time */
  int index_bg_rho_ncdm1;        /**< density of first ncdm species (others contiguous) */
  int index_bg_p_ncdm1;          /**< pressure of first ncdm species (others contiguous) */
  int index_bg_pseudo_p_ncdm1;   /**< another statistical momentum useful in ncdma approximation */
  int index_bg_rho_tot;          /**< total density */
  int index_bg_p_tot;            /**< total pressure */
  int index_bg_p_tot_prime;      /**< derivative of total pressure wrt conformal time */
  int index_bg_Omega_r;          /**< relativistic density fraction (\f$ \Omega_{\gamma} + \Omega_{\nu r} \f$) */
  int index_bg_z;                /**< redshift */

  int index_th_xe;               /**< ionization fraction */
  int index_th_dkappa;           /**< Thomson scattering rate */
  int index_th_tau_d;            /**< baryon drag optical depth */
  int index_th_ddkappa;          /**< derivative of Thomson scattering rate */
  int index_th_dddkappa;         /**< second derivative of Thomson scattering rate */
  int index_th_exp_m_kappa;      /**< \f$ exp^{-\kappa} \f$ */
  int index_th_g;                /**< visibility function */
  int index_th_dg;               /**< derivative of visibility function */
  int index_th_ddg;              /**< second derivative of visibility function */
  int index_th_rate;             /**< maximum variation rate of thermodynamical quantities */

  /* Metric indices */
  int index_mt_h_prime;          /**< metric perturbation h' */
  int index_mt_eta;              /**< metric perturbation eta */
  int index_mt_h_prime_prime;    /**< metric perturbation h'' */
  int index_mt_eta_prime;        /**< metric perturbation eta' */

  //@}

  /** @name - perturbation quantities */

  //@{

  double * delta_rho;       /**< Pointer towards the vector of density perturbations */
  double * rho_plus_p_theta;/**< Pointer towards the vector of velocity perturbations */
  double * rho_plus_p_shear;/**< Pointer towards the vector of shear perturbations */
  double * delta_p;         /**< Pointer towards the vector of pressure perturbations */

  /* Perturbation vector */
  struct perturb_vector * pv; /**< Pointer to perturbation vector structure */

  //@}
};

/* Function prototypes */
int perturbations_dark_energy(
                             struct perturbations * ppt,
                             struct background * pba,
                             int index_md,
                             double k,
                             double tau,
                             double * y,
                             struct perturb_workspace * ppw,
                             ErrorMsg error_message
                             );

int perturbations_dark_energy_with_hidden_regions(
                                                struct perturbations * ppt,
                                                struct background * pba,
                                                int index_md,
                                                double k,
                                                double tau,
                                                double * y,
                                                struct perturb_workspace * ppw,
                                                ErrorMsg error_message
                                                );

int perturbations_effective_cs2_with_hidden_regions(
                                                  struct background * pba,
                                                  double a,
                                                  double * cs2
                                                  );

int perturbations_growth_rate_with_hidden_regions(
                                                struct background * pba,
                                                double a,
                                                double * growth_rate
                                                );

#endif /* __PERTURBATIONS__ */
