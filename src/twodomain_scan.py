"""Two-domain localized IDT discovery scan."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'archive', 'class', 'python'))
import numpy as np
from classy import Class

C = 299792.458
R_OBS = 1.7502; R_ERR = 0.0046
LA_OBS = 301.471; LA_ERR = 0.090

def test(label, H0, obh2, ocdmh2, f1=0, zc1=2000, sig1=0.15, f2=0, zc2=1, sig2=0.5):
    cosmo = Class()
    p = {'output': 'tCl,pCl,lCl,mPk', 'l_max_scalars': 2500,
         'P_k_max_h/Mpc': 1.0, 'H0': H0, 'omega_b': obh2, 'omega_cdm': ocdmh2,
         'T_cmb': 2.7255, 'N_ur': 2.0328, 'N_ncdm': 1, 'm_ncdm': 0.06}
    if f1 > 0:
        p['f_dom_idt_1'] = f1; p['z_c_idt_1'] = zc1; p['sigma_ln_idt_1'] = sig1
    if f2 > 0:
        p['f_dom_idt_2'] = f2; p['z_c_idt_2'] = zc2; p['sigma_ln_idt_2'] = sig2
    cosmo.set(p)
    try:
        cosmo.compute()
    except Exception as e:
        print(f'  {label:<48} FAILED: {str(e)[:60]}')
        cosmo.struct_cleanup(); cosmo.empty()
        return
    h = H0 / 100; Om = (obh2 + ocdmh2) / h**2
    da = cosmo.angular_distance(1089.92); dc = da * (1 + 1089.92)
    bg = cosmo.get_background()
    rs_star = np.interp(1089.92, bg['z'][::-1], bg['comov.snd.hrz.'][::-1])
    R = np.sqrt(Om) * H0 / C * dc; la = np.pi * dc / rs_star
    rd = cosmo.rs_drag(); s8 = cosmo.sigma8()
    R_sig = abs(R - R_OBS) / R_ERR; la_sig = abs(la - LA_OBS) / LA_ERR
    H0_inf = 67.36 * 147.10 / rd
    flag = ' ★' if s8 < 0.808 else (' ✓' if s8 < 0.815 else '')
    print(f'  {label:<48} H₀i={H0_inf:>5.1f} σ₈={s8:.4f}{flag:3s} '
          f'R={R_sig:>4.1f}σ la={la_sig:>4.1f}σ rd={rd:.1f}')
    cosmo.struct_cleanup(); cosmo.empty()

print('=== TWO LOCALIZED IDT DOMAINS — DISCOVERY SCAN ===')
print()

print('--- Baselines ---')
test('ΛCDM', 67.36, 0.02237, 0.12)
test('Early only (f=0.10,zc=2000,s=0.18)', 67.36, 0.02237, 0.12, f1=0.10, zc1=2000, sig1=0.18)
test('Late only (f=0.03,zc=1.0,s=0.5)', 67.36, 0.02237, 0.12, f2=0.03, zc2=1.0, sig2=0.5)
test('Late only (f=0.05,zc=1.0,s=0.5)', 67.36, 0.02237, 0.12, f2=0.05, zc2=1.0, sig2=0.5)

print('\n--- Two localized domains ---')
for f1, zc1, s1 in [(0.05,2000,0.15), (0.08,2000,0.18), (0.10,2000,0.18), (0.10,1500,0.15)]:
    for f2, zc2, s2 in [(0.02,1.0,0.5), (0.03,1.0,0.5), (0.05,1.0,0.5),
                         (0.03,2.0,0.8), (0.05,2.0,0.8), (0.05,2.0,1.0)]:
        label = f'E({f1},{zc1},{s1})+L({f2},{zc2},{s2})'
        test(label, 67.36, 0.02237, 0.12, f1, zc1, s1, f2, zc2, s2)
    print()
