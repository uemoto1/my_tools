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

    eig = np.zeros([nk,nb])
    occ = np.zeros([nk,nb])

    for ik in range(nk):
        # Skip empty line
        line = fh.readline()
        # header
        line = fh.readline()
        k1, k2, k3, kw = np.fromstring(line, sep=" ", dtype=float)
        ik1 = ik + 1
        print(f"# {ik1:3d} k=({k1:6.3f}, {k2:6.3f}, {k3:6.3f}) w={kw:12.3e}")
        for ib in range(nb):
            line = fh.readline()
            tmp = line.split()
            eig[ik, ib] = float(tmp[1])
            occ[ik, ib] = float(tmp[2])
        ivb = 0
        icb = nb-1
        for ib in range(nb):
            if (eig[ik, ib] > eig[ik, ivb]) and occ[ik, ib] > 0.75:
                ivb = ib
            if (eig[ik, ib] < eig[ik, icb]) and occ[ik, ib] < 0.25:
                icb = ib
        evb = eig[ik, ivb]
        ecb = eig[ik, icb]
        ivb1 = ivb+1
        icb1 = icb+1
        print(f"# ... vb {ivb1:3d} {evb:8.3f} cb {icb1:3d} {ecb:8.3f}")


ev_max = np.amax(eig[occ > 0.75]) 
ec_min = np.amin(eig[occ < 0.25]) 
e_gap = ec_min - ev_max

print(f"# Maximal energy valence: {ev_max:.6f}")
print(f"# Minimal energy conduction: {ec_min:.6f}")
print(f"# Energy gap: {e_gap:.6f}")

