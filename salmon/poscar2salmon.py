#!/usr/bin/env python3




template = """
&calculation
  theory = 'dft'
/

&control
  sysname = 'sample'
/

&parallel
  nproc_k = 1
  nproc_ob = 1
  nproc_rgrid(1) = 1
  nproc_rgrid(2) = 1
  nproc_rgrid(3) = 1
/

&units
  unit_system = 'au'
/

&system
  yn_periodic = 'y'
  al(1:3) = {ALX:.6f}d0, {ALY:.6f}d0, {ALZ:.6f}d0
  nelem = {NELEM}
  natom = {NATOM}
  nelec = {NELEC}
  nstate = {NSTATE}
/

&pseudo
{PSEUDO}
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
  nscf = 500
  threshold = 1.0d-9
/

&analysis
  yn_out_dos = "y"
  yn_out_dos_set_fe_origin = "y"
/

&atomic_red_coor
{COOR}
/
"""

tbl = [
    "H", "He", "Li", "Be", "B", "C", "N", "O", "F", "Ne",
    "Na", "Mg", "Al", "Si", "P", "S", "Cl", "Ar", 
    "K", "Ca", "Sc", "Ti", "V", "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Zn", "Ga", "Ge", "As", "Se", "Br", "Kr", 
    "Rb", "Sr", "Y", "Zr", "Nb", "Mo", "Tc", "Ru", "Rh", "Pd", "Ag", "Cd", "In", "Sn", "Sb", "Te", "I", "Xe", 
    "Cs", "Ba", "La", "Ce", "Pr", "Nd", "Pm", "Sm", "Eu", "Gd", "Tb", "Dy", "Ho", "Er", "Tm", "Yb", 
    "Lu", "Hf", "Ta", "W", "Re", "Os", "Ir", "Pt", "Au", "Hg", "Tl", "Pb", "Bi", "Po", "At", "Rn"
]

pseudo_tbl = {
  # "Si": {"number": 14, "file": "./Si_rps.dat", "lloc": 1, "nelec": 4},
  # "H": {"number": 1, "file": "./Si_rps.dat", "lloc": 0, "nelec": 1},
  e1: {"number": iz1+1, "file": f"{e1}.psp8", }
}

bohr_ang = 0.529177210903
epsilon = 1e-6

import sys
import numpy as np
import argparse
from pymatgen.core import Structure

parser = argparse.ArgumentParser()
parser.add_argument('filename', default="POSCAR")
parser.add_argument('--density', default=0.6, type=float)
parser.add_argument('--nkgrid', default="1,1,1")
args = parser.parse_args()

structure = Structure.from_file(args.filename)
density = float(args.density)

alx = structure.lattice.a / bohr_ang
aly = structure.lattice.b / bohr_ang
alz = structure.lattice.c / bohr_ang

element_set = set([])
for site in structure:
    element_set.add(site.specie.symbol)
element_list = list(element_set)

pseudo = []
n = 1
for symbol in element_list:
    file = pseudo_tbl[symbol]["file"]
    number = pseudo_tbl[symbol]["number"]
    lloc = pseudo_tbl[symbol]["lloc"]
    pseudo.append(f"file_pseudo({n}) = '{file}'")
    pseudo.append(f"izatom({n}) = {number}")
    pseudo.append(f"lloc_ps({n}) = {lloc}")
    n = n + 1

coor = []
nelec = 0
for site in structure:
    RX, RY, RZ = site.frac_coords
    N = element_list.index(site.specie.symbol) + 1
    coor.append(f"'atom' {RX:.6f}d0 {RY:.6f}d0 {RZ:.6f}d0 {N}")
    nelec += pseudo_tbl[site.specie.symbol]["nelec"]


print(template.format(
  ALX=alx,
  ALY=aly,
  ALZ=alz,
  NRX=round(alx/density),
  NRY=round(aly/density),
  NRZ=round(alz/density),
  NUM_KGRID=args.nkgrid,
  PSEUDO="\n".join(pseudo),
  COOR="\n".join(coor),
  NELEM=len(element_list),
  NATOM=len(structure),
  NELEC=nelec,
  NSTATE=nelec,
))

