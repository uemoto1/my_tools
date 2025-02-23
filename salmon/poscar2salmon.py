#!/usr/bin/env python3




template = """
&calculation
    theory = 'dft'
    ! theory = 'tddft_response'
/
&units
    unit_system = 'au'
/
&control
    sysname = 'model'
    ! yn_restart = 'y'
    ! yn_reset_step_restart = 'y'
    ! method_wf_distributor = "slice"
/
&parallel
    nproc_k = 1
    nproc_ob = 1
    nproc_rgrid(1) = 1
    nproc_rgrid(2) = 1
    nproc_rgrid(3) = 1
    ! process_allocation = 'orbital_sequential'
/
&system
    yn_periodic = 'y'
    al(1:3) = {ALX:.6f}, {ALY:.6f}, {ALZ:.6f}
    nelem = {NELEM}
    natom = {NATOM}
    nelec = {NELEC}
    nstate = {NSTATE}
    ! temperature_k = 300.0
/
&functional
    xc = 'PZ'
/
&rgrid
    num_rgrid(1:3) = {NRX}, {NRY}, {NRZ}
/
&kgrid
    num_kgrid(1:3) = {NUM_KGRID}
/
&scf
    nscf = 200
    threshold = 1.0d-9
    ! method_init_density = 'pp'
    ! method_init_density = 'read_dns_cube'
    method_init_density = 'wf'
    ! ncg_init = 50
    ! nscf_init_mix_zero = 25
    yn_preconditioning = 'y'

    mixrate = 0.1
    method_mixing = 'simple'
    ! nmemory_mb = 4
    ! alpha_mb = 0.30d0
/
&tgrid
    dt = 0.02d0
    nt = 50000
/
&emfield
    ae_shape1 = 'impulse'
    ! ae_shape1 = 'Acos2'
    ! I_wcm2_1 = 1.0d9
    ! tw1 = 500.0
    ! omega1 = 0.057
    epdir_re1(1:3) = 0.0, 0.0, 1.0
/
&analysis  
    yn_out_dns = "y"
    yn_out_dos = "y"
    yn_out_dos_set_fe_origin = "y"
/
&pseudo
{PSEUDO}
/
&atomic_red_coor
{COORD}
/
"""

pseudo_tbl = {
  # "Si": {"number": 14, "file": "./Si_rps.dat", "lloc": 1, "nelec": 4},
  # "H": {"number": 1, "file": "./Si_rps.dat", "lloc": 0, "nelec": 1},
  'H': {'number': 1, 'file': 'H.psp8', 'nelec': 1},
  'He': {'number': 2, 'file': 'He.psp8', 'nelec': 2},
  'Li': {'number': 3, 'file': 'Li.psp8', 'nelec': 3},
  'Be': {'number': 4, 'file': 'Be.psp8', 'nelec': 4},
  'B': {'number': 5, 'file': 'B.psp8', 'nelec': 3},
  'C': {'number': 6, 'file': 'C.psp8', 'nelec': 4},
  'N': {'number': 7, 'file': 'N.psp8', 'nelec': 5},
  'O': {'number': 8, 'file': 'O.psp8', 'nelec': 6},
  'F': {'number': 9, 'file': 'F.psp8', 'nelec': 7},
  'Ne': {'number': 10, 'file': 'Ne.psp8', 'nelec': 8},
  'Na': {'number': 11, 'file': 'Na.psp8', 'nelec': 9},
  'Mg': {'number': 12, 'file': 'Mg.psp8', 'nelec': 10},
  'Al': {'number': 13, 'file': 'Al.psp8', 'nelec': 3},
  'Si': {'number': 14, 'file': 'Si.psp8', 'nelec': 4},
  'P': {'number': 15, 'file': 'P.psp8', 'nelec': 5},
  'S': {'number': 16, 'file': 'S.psp8', 'nelec': 6},
  'Cl': {'number': 17, 'file': 'Cl.psp8', 'nelec': 7},
  'Ar': {'number': 18, 'file': 'Ar.psp8', 'nelec': 8},
  'K': {'number': 19, 'file': 'K.psp8', 'nelec': 9},
  'Ca': {'number': 20, 'file': 'Ca.psp8', 'nelec': 10},
  'Sc': {'number': 21, 'file': 'Sc.psp8', 'nelec': 11},
  'Ti': {'number': 22, 'file': 'Ti.psp8', 'nelec': 12},
  'V': {'number': 23, 'file': 'V.psp8', 'nelec': 13},
  'Cr': {'number': 24, 'file': 'Cr.psp8', 'nelec': 14},
  'Mn': {'number': 25, 'file': 'Mn.psp8', 'nelec': 15},
  'Fe': {'number': 26, 'file': 'Fe.psp8', 'nelec': 16},
  'Co': {'number': 27, 'file': 'Co.psp8', 'nelec': 17},
  'Ni': {'number': 28, 'file': 'Ni.psp8', 'nelec': 18},
  'Cu': {'number': 29, 'file': 'Cu.psp8', 'nelec': 19},
  'Zn': {'number': 30, 'file': 'Zn.psp8', 'nelec': 20},
  'Ga': {'number': 31, 'file': 'Ga.psp8', 'nelec': 13},
  'Ge': {'number': 32, 'file': 'Ge.psp8', 'nelec': 14},
  'As': {'number': 33, 'file': 'As.psp8', 'nelec': 15},
  'Se': {'number': 34, 'file': 'Se.psp8', 'nelec': 16},
  'Br': {'number': 35, 'file': 'Br.psp8', 'nelec': 7},
  'Kr': {'number': 36, 'file': 'Kr.psp8', 'nelec': 8},
  'Rb': {'number': 37, 'file': 'Rb.psp8', 'nelec': 9},
  'Sr': {'number': 38, 'file': 'Sr.psp8', 'nelec': 10},
  'Y': {'number': 39, 'file': 'Y.psp8', 'nelec': 11},
  'Zr': {'number': 40, 'file': 'Zr.psp8', 'nelec': 12},
  'Nb': {'number': 41, 'file': 'Nb.psp8', 'nelec': 13},
  'Mo': {'number': 42, 'file': 'Mo.psp8', 'nelec': 14},
  'Tc': {'number': 43, 'file': 'Tc.psp8', 'nelec': 15},
  'Ru': {'number': 44, 'file': 'Ru.psp8', 'nelec': 16},
  'Rh': {'number': 45, 'file': 'Rh.psp8', 'nelec': 17},
  'Pd': {'number': 46, 'file': 'Pd.psp8', 'nelec': 18},
  'Ag': {'number': 47, 'file': 'Ag.psp8', 'nelec': 19},
  'Cd': {'number': 48, 'file': 'Cd.psp8', 'nelec': 20},
  'In': {'number': 49, 'file': 'In.psp8', 'nelec': 13},
  'Sn': {'number': 50, 'file': 'Sn.psp8', 'nelec': 14},
  'Sb': {'number': 51, 'file': 'Sb.psp8', 'nelec': 15},
  'Te': {'number': 52, 'file': 'Te.psp8', 'nelec': 16},
  'I': {'number': 53, 'file': 'I.psp8', 'nelec': 7},
  'Xe': {'number': 54, 'file': 'Xe.psp8', 'nelec': 8},
  'Cs': {'number': 55, 'file': 'Cs.psp8', 'nelec': 9},
  'Ba': {'number': 56, 'file': 'Ba.psp8', 'nelec': 10},
  'La': {'number': 57, 'file': 'La.psp8', 'nelec': 11},
  'Lu': {'number': 71, 'file': 'Lu.psp8', 'nelec': 25},
  'Hf': {'number': 72, 'file': 'Hf.psp8', 'nelec': 12},
  'Ta': {'number': 73, 'file': 'Ta.psp8', 'nelec': 13},
  'W': {'number': 74, 'file': 'W.psp8', 'nelec': 14},
  'Re': {'number': 75, 'file': 'Re.psp8', 'nelec': 15},
  'Os': {'number': 76, 'file': 'Os.psp8', 'nelec': 16},
  'Ir': {'number': 77, 'file': 'Ir.psp8', 'nelec': 17},
  'Pt': {'number': 78, 'file': 'Pt.psp8', 'nelec': 18},
  'Au': {'number': 79, 'file': 'Au.psp8', 'nelec': 19},
  'Hg': {'number': 80, 'file': 'Hg.psp8', 'nelec': 20},
  'Tl': {'number': 81, 'file': 'Tl.psp8', 'nelec': 13},
  'Pb': {'number': 82, 'file': 'Pb.psp8', 'nelec': 14},
  'Bi': {'number': 83, 'file': 'Bi.psp8', 'nelec': 15},
  'Po': {'number': 84, 'file': 'Po.psp8', 'nelec': 16},
  'Rn': {'number': 86, 'file': 'Rn.psp8', 'nelec': 18},
}

bohr_ang = 0.529177210903
epsilon = 1e-6

import sys
import numpy as np
import argparse
from pymatgen.core import Structure

parser = argparse.ArgumentParser()
parser.add_argument('filename', default="POSCAR")
parser.add_argument('--spacing', default=0.5, type=float)
parser.add_argument('--nkgrid', default="1,1,1")
parser.add_argument('--element', default="")
args = parser.parse_args()

structure = Structure.from_file(args.filename)
spacing = float(args.spacing)

alx = structure.lattice.a / bohr_ang
aly = structure.lattice.b / bohr_ang
alz = structure.lattice.c / bohr_ang

if args.element:
    element_list = args.element.split(",")
else:
    element_list = []
for site in structure:
    e = site.specie.symbol
    if e not in element_list:
        element_list.append(e)
    

pseudo_list = []
for n, symbol in enumerate(element_list, start=1):
    file = pseudo_tbl[symbol]["file"]
    number = pseudo_tbl[symbol]["number"]
    # lloc = pseudo_tbl[symbol]["lloc"]
    pseudo_list.append(f"    file_pseudo({n}) = '{file}'")
    pseudo_list.append(f"    izatom({n}) = {number}")
    # pseudo += f"lloc_ps({n}) = {lloc}\n"
pseudo = "\n".join(pseudo_list)

coord_list = []
nelec = 0
for site in structure:
    RX, RY, RZ = site.frac_coords
    N = element_list.index(site.specie.symbol) + 1
    coord_list.append(f"    'site' {RX:.6f} {RY:.6f} {RZ:.6f} {N}")
    nelec += pseudo_tbl[site.specie.symbol]["nelec"]
coord = "\n".join(coord_list)


print(template.format(
    ALX=alx,
    ALY=aly,
    ALZ=alz,
    NRX=round(alx/spacing/2)*2,
    NRY=round(aly/spacing/2)*2,
    NRZ=round(alz/spacing/2)*2,
    NUM_KGRID=args.nkgrid,
    PSEUDO=pseudo,
    COORD=coord,
    NELEM=len(element_list),
    NATOM=len(structure),
    NELEC=nelec,
    NSTATE=nelec,
))

