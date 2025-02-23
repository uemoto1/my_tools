from pymatgen.core import Structure, Lattice
import numpy as np
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('--input', '-i', required=True)
parser.add_argument('--output', '-o', required=True)
parser.add_argument('--xdir', default="", type=str)
parser.add_argument('--ydir', default="", type=str)
parser.add_argument('--zdir', default="0,0,1", type=str)
parser.add_argument('--nmax', default=2, type=int)
parser.add_argument('--epsilon', default=1e-3, type=float)
args = parser.parse_args()




def grid3d(n):
    tmp = []
    for i1 in range(-n, n+1):
        for i2 in range(-n, n+1):
            for i3 in range(-n, n+1):
                if not (i1 == i2 == i3 == 0):
                    tmp.append(np.array((i1, i2, i3)))
    return tmp

def init_list(s, n):
    if s:
        return [
            [int(x) for x in s.split(",")]
        ]
    else:
        return grid3d(n)

def is_ortho(u, v, eps=1e-3):
    cos_uv = np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v))
    return abs(cos_uv) < eps

structure = Structure.from_file(args.input)
a1, a2, a3 = structure.lattice.matrix

idir_x_list = init_list(args.xdir, args.nmax)
idir_y_list = init_list(args.ydir, args.nmax)
idir_z_list = init_list(args.zdir, args.nmax)

result = []
for idir_x in idir_x_list:
    AX = np.dot(idir_x, [a1, a2, a3])

    for idir_y in idir_y_list:
        AY = np.dot(idir_y, [a1, a2, a3])
        if not is_ortho(AX, AY, args.epsilon):
            continue

        for idir_z in idir_z_list:
            AZ = np.dot(idir_z, [a1, a2, a3])
            if not is_ortho(AX, AZ, args.epsilon):
                continue
            if not is_ortho(AY, AZ, args.epsilon):
                continue
            vol = np.dot(AX, np.cross(AY, AZ))
            if vol > 0:
                result.append(
                    [idir_x, idir_y, idir_z, AX, AY, AZ, vol]
                )


if len(result) > 0:
    print("# %d results are detected." % len(result))
else:
    raise ValueError("Increase nmax!")

def penalty(it):
    idir_x, idir_y, idir_z, A1, A2, A3, vol = it
    penalty = round(vol)
    penalty += 0.1 * np.sum(np.abs(idir_x))
    penalty += 0.1 * np.sum(np.abs(idir_y))
    penalty += 0.1 * np.sum(np.abs(idir_z))
    penalty += 0.01 * np.dot([-1, 0, 0], idir_x)
    penalty += 0.01 * np.dot([0, -1, 0], idir_y)
    penalty += 0.01 * np.dot([0, 0, -1], idir_z)
    return penalty

result.sort(key=penalty)

idir_x, idir_y, idir_z, AX, AY, AZ, vol = result[0]
print("# [%d, %d, %d] is employed as AX" % tuple(idir_x))
print("# [%d, %d, %d] is employed as AY" % tuple(idir_y))
print("# [%d, %d, %d] is employed as AZ" % tuple(idir_z))
print("# AX = %.6f" % np.linalg.norm(AX))
print("# AY = %.6f" % np.linalg.norm(AY))
print("# AZ = %.6f" % np.linalg.norm(AZ))
BX = np.cross(AY, AZ) / vol
BY = np.cross(AZ, AX) / vol
BZ = np.cross(AX, AY) / vol


def is_duplicated(t, t_list, eps):
    for t1 in t_list:
        d = t1 - t
        d = d - np.round(d)
        if np.amax(np.abs(d)) < eps:
            return True
    return False


t_list = []
e_list = []
for site in structure.sites:
    t1, t2, t3 = site.frac_coords
    for i1 in range(-3*args.nmax, 3*args.nmax+1):
        for i2 in range(-3*args.nmax, 3*args.nmax+1):
            for i3 in range(-3*args.nmax, 3*args.nmax+1):
                r = np.dot([t1 + i1, t2 + i2, t3 + i3], [a1, a2, a3])
                t = np.dot([BX, BY, BZ], r) % 1.0
                if not is_duplicated(t, t_list, args.epsilon):
                    t_list.append(t)
                    e_list.append(site.specie.name)
                    print("# %3s %12.6f %12.6f %12.6f" % (site.specie.name, t[0], t[1], t[2]))





LATTICE = Lattice.orthorhombic(
    np.linalg.norm(AX),
    np.linalg.norm(AY),
    np.linalg.norm(AZ),
)

STRUCTURE = Structure(LATTICE, e_list, t_list)

STRUCTURE.to_file(args.output)
