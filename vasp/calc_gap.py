#!/usr/bin/env python3
import numpy as np

with open("EIGENVAL") as fh:
    # line 1:
    line = fh.readline()
    # line 2:
    line = fh.readline()
    # line 3:
    line = fh.readline()
    # line 4:
    line = fh.readline()
    # line 5:
    line = fh.readline()
    # line 6:
    line = fh.readline()
    ne, nk, nb = np.fromstring(line, sep=" ", dtype=int)

    print(f"# number of electron = {ne}")
    print(f"# number of k = {nk}")
    print(f"# number of band = {nb}")

    eig = np.empty([nk,nb])
    occ = np.empty([nk,nb])

    for ik in range(nk):
        # Skip empty line
        line = fh.readline()
        # header
        line = fh.readline()
        k1, k2, k3, kw = np.fromstring(line, sep=" ", dtype=float)
        print(f"#k {ik:3d} ({k1:6.2f} {k2:6.2f} {k3:6.2f}) {kw:12.3e}")
        for ib in range(nb):
            line = fh.readline()
            tmp = line.split()
            eig[ik, ib] = float(tmp[1])
            occ[ik, ib] = float(tmp[2])
          
ev_max = np.max(eig[occ > 0.5]) 
ec_min = np.min(eig[occ < 0.5]) 
e_gap = ec_min - ev_max

print(f"# Maximal energy valence state: {ev_max:.6f}")
print(f"# Minimal energy conduction band: {ec_min:.6f}")
print(f"# Energy gap: {e_gap:.6f}")

