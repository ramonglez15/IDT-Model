"""
IDT CLASS Module
================
Inflationary Domain Theory — Minimal effective model for CLASS integration.

Components:
    idt_domain      : Core domain fluid (ρ, p, w, perturbations)
    cosmology_base  : ΛCDM baseline functions
    class_integration: CLASS .ini generation and source patches

Quick start:
    from idt_class_module.idt_domain import IDTDomain, IDTModel
    
    domain = IDTDomain(f_dom=0.10, z_c=2000, delta_z=600)
    model = IDTModel(domains=[domain])
    model.summary()
"""

from .idt_domain import IDTDomain, IDTModel
from .cosmology_base import E2_LCDM, H_LCDM, sound_horizon
