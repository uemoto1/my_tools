import sys
import numpy as np

bohr_ang = 0.529177210903

with open("POSCAR") as fh:
    line = fh.readlines()

title = line[0].strip()
alat = float(line[1])
vec_a1 = alat * np.fromstring(line[2], sep=" ", dtype=float)
vec_a2 = alat * np.fromstring(line[3], sep=" ", dtype=float)
vec_a3 = alat * np.fromstring(line[4], sep=" ", dtype=float)
element_list = line[5].split()
num_atom_list = np.fromstring(line[6], sep=" ", dtype=int)
mode = line[6].strip().lower()

if mode != "direct":
    sys.exit(-1)

if "selective" in line[7].lower():
    k = 8
else:
    k = 7

atom_xyz_list = []
for e, n in zip(element_list, num_atom_list):
    for i in range(n):
        t = np.array(line[k].split()[0:3])
        if mode == "direct":
            r = vec_a1 * t[0] + vec_a2 * t[1] + vec_a3 * t[2]
            atom_xyz_list.append((e, r))
        elif mode == "cartesian":
            atom_xyz_list.append((e, t))


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
  al(1:3) = {LX:.6f}d0, {LY:.6f}d0, {LZ:.6f}d0
  nelem = {NELEM}
  natom = {NATOM}
  nelec = {NELEC}
  nstate = {NSTATE}
/

&pseudo
{PSEUDO_TBL}
/

&functional
  xc = 'PZ'
/

&rgrid
  num_rgrid(1:3) = 16, 16, 16
/

&kgrid
  num_kgrid(1:3) = 8, 8, 8
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
{COOR_TBL}
/

"""






PSEUDO_LIST = ""
  file_pseudo(1) = './Si_rps.dat'
  izatom(1) = 14
  lloc_ps(1) = 2