import sys
import os
import numpy as np

d = 10.24 / 16

table = {
    "Si": {"iz": 14, "neigmx": 4, "mass":51194.00},
    "O": {"iz": 8, "neigmx": 4, "mass":29164.45},
}

def read_poscar(file_poscar):
    with open(file_poscar) as fh:
        title = fh.readline()
        scale = float(fh.readline())
        a1 = scale * np.fromstring(fh.readline(), sep=" ", dtype=float)
        a2 = scale * np.fromstring(fh.readline(), sep=" ", dtype=float)
        a3 = scale * np.fromstring(fh.readline(), sep=" ", dtype=float)
        tmp = fh.readline().split()
        if tmp[0][0].isdigit():
            elem = ["" * len(tmp)]
        else:
            elem = tmp
            tmp = fh.readline().split()
        num = [int(x) for x in tmp]
        tmp = fh.readline()
        if "selective dynamics" in tmp.lower():
            tmp = fh.readline()
        if "direct"  in tmp.lower():
            mode = "direct"
        if "cartesian" in tmp.lower():
            raise ValueError
        coord = []
        for i in range(len(elem)):
            for j in range(num[i]):
                tmp = fh.readline().split()
                coord.append((elem[i], np.array(tmp[0:3], dtype=float)))
    return a1, a2, a3, elem, num, mode, coord

def search(a1, a2, a3, eps = 1e-3):
    target = []
    for i1 in [0, 1, -1, 2, -2, 3, -3]:
        for i2 in [0, 1, -1, 2, -2, 3, -3]:
            for i3 in [0, 1, -1, 2, -2, 3, -3]:
                target.append([i1, i2, i3])
    for k3 in target:
        A3 = np.dot(k3, [a1, a2, a3])
        if np.linalg.norm(A3) < eps:
            continue
        for k2 in target:
            A2 = np.dot(k2, [a1, a2, a3])
            if np.linalg.norm(A2) < eps:
                continue
            if abs(np.dot(A2, A3) / np.linalg.norm(A2) / np.linalg.norm(A3)) > eps:
                continue
            for k1 in target:
                A1 = np.dot(k1, [a1, a2, a3])
                if np.linalg.norm(A1) < eps:
                    continue
                if abs(np.dot(A1, A2) / np.linalg.norm(A1) / np.linalg.norm(A2)) > eps:
                    continue
                if abs(np.dot(A1, A3) / np.linalg.norm(A1) / np.linalg.norm(A3)) > eps:
                    continue
                V = np.dot(A1, np.cross(A2, A3))
                if V < eps:
                    continue
                return k1, k2, k3
            
def expand(a1, a2, a3, k1, k2, k3, coord, eps=1e-3):
    A1 = np.dot(k1, [a1, a2, a3])
    A2 = np.dot(k2, [a1, a2, a3])
    A3 = np.dot(k3, [a1, a2, a3])
    V = np.dot(A1, np.cross(A2, A3))
    B1 = np.cross(A2, A3) / V
    B2 = np.cross(A3, A1) / V
    B3 = np.cross(A1, A2) / V
    COORD = []
    for i1 in range(-10, 10):
        for i2 in range(-10, 10):
            for i3 in range(-10, 10):
                for elem, (r1, r2, r3) in coord:
                    xyz = np.dot([r1+i1, r2+i2, r3+i3], [a1, a2, a3])
                    R1 = np.dot(B1, xyz)
                    R2 = np.dot(B2, xyz)
                    R3 = np.dot(B3, xyz)
                    if (-eps <= R1 <= 1.0 + eps):
                        if (-eps <= R2 <= 1.0 + eps):
                            if (-eps <= R3 <= 1.0 + eps):
                                flag = True
                                for _, (RR1, RR2, RR3) in COORD:
                                    D1 = (RR1 - R1)
                                    D2 = (RR2 - R2)
                                    D3 = (RR3 - R3)
                                    D1 = abs(np.rint(D1) - D1)
                                    D2 = abs(np.rint(D2) - D2)
                                    D3 = abs(np.rint(D3) - D3)
                                    if abs(D1) < eps and abs(D2) < eps and abs(D3) < eps:
                                        flag = False
                                        break
                                if flag:
                                    COORD.append((elem, (R1, R2, R3)))
    return A1,A2,A3,COORD


a1, a2, a3, elem, num, mode, coord = read_poscar(sys.argv[1])
k1,k2,k3=search(a1,a2,a3)
A1,A2,A3,COORD=expand(a1,a2,a3,k1,k2,k3,coord)

COORD.sort()


LX = np.linalg.norm(A1) / 0.529177210903
LY = np.linalg.norm(A2) / 0.529177210903
LZ = np.linalg.norm(A3) / 0.529177210903

NEIGMX = 0
for elem, _ in COORD:
    NEIGMX += table[elem]["neigmx"]


print("""
&nml_inp_prm_kukan
    ! Parallelization condition
    nprocx = 1      ! # of processes (x)
    nprocy = 1      ! # of processes (y)
    nprocz = 1      ! # of processes (z)
    nprock = 1      ! of processes (k)

    nperi = 3       ! switchs for periodic boundary conditions (0; isolated, 3; periodic)

    xmax = {XMAX:.3f}d0     ! length of supercell (x in bohr, total length is 2*xmax)
    ymax = {YMAX:.3f}d0     ! length of supercell (y in bohr, total length is 2*xmax)
    zmax = {ZMAX:.3f}d0     ! length of supercell (z in bohr, total length is 2*xmax)

    nxmax = {NXMAX:d}       ! # of grid points (x, total number is 2*nxmax)
    nymax = {NYMAX:d}       ! # of grid points (y, total number is 2*nxmax)
    nzmax = {NZMAX:d}       ! # of grid points (z, total number is 2*nxmax)
    
    numkx = 3               ! # of sampling k points (x)
    numky = 3               ! # of sampling k points (y)
    numkz = 3               ! # of sampling k points (z)

    kmeshgen = 2            ! 1:nonsym 2:sym

    natom = {NATOM:d}       ! # of atoms
    neigmx = {NEIGMX:d}     ! # of of states per k point

    ncgscf = 300            ! min. # of SCF its. using CG before DIIS
    eps_scf = 1.0d-6        ! criteria of the convergency for SCF
/
""".format(
    XMAX=(LX*0.5),
    YMAX=(LY*0.5),
    ZMAX=(LZ*0.5),
    NXMAX=int(LX*0.5/d),
    NYMAX=int(LY*0.5/d),
    NZMAX=int(LZ*0.5/d),
    NEIGMX=NEIGMX,
    NATOM=len(COORD),
))

print("! [x], [y], [z], [atom number], switch [x], [y], [z], [weight], switches [soc], [pp], [na]")
for n, (elem, (R1, R2, R3)) in enumerate(COORD, start=1):
    print("{X:+7.3f} {Y:+7.3f} {Z:+7.3f} {IZ:2d} 1 1 1 {MASS:12.2f} 11 1 {N}a".format(
        X=LX*(R1-0.5),
        Y=LY*(R2-0.5),
        Z=LZ*(R3-0.5),
        IZ=table[elem]["iz"],
        MASS=table[elem]["mass"],
        N=n
    ))

    