#!/usr/bin/env python3
import numpy as np

n_order_list = list(range(10))

import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", type=str, required=True)
parser.add_argument("-n", "--nthread", type=int, default=0)
parser.add_argument("--nmax", type=int, default=10)
args = parser.parse_args()

basedir = os.path.dirname(os.path.abspath(args.input))

if args.nthread < 1:
    args.nthread = int(os.environ.get("OMP_NUM_THREADS", "1"))

parse_float = lambda x: float(x.lower().replace("d","e"))
parse_string = lambda x: x.replace('"', '').replace("'", "").strip()
with open(args.input, "r") as fh:
    print(fh.name)
    for line in fh:
        tmp = line.split("=")
        if len(tmp) == 2:
            lhs = tmp[0].strip()
            rhs = tmp[1].split("!")[0].strip()
            if lhs.lower() == "sysname":
                sysname = parse_string(rhs)
            if lhs.lower() == "hx_m":
                hx_m = parse_float(rhs)
            if lhs.lower() == "hy_m":
                hy_m = parse_float(rhs)
            if lhs.lower() == "dt":
                dt = parse_float(rhs)
            if lhs.lower() == "nt":
                nt = int(rhs)
            if lhs.lower() == "omega1":
                omega1 = parse_float(rhs)

with open(f"{basedir}/.shape.txt", "r") as fh:
    print(fh.name)
    macro = int(fh.readline())
    point = {}
    for i in range(macro):
        line = fh.readline()
        tmp = line.split()
        imacro, ix, iy, iz = map(int, tmp[0:4])
        point[imacro] = (ix, iy, iz)
target_list = list(range(100, nt+1, 100))

def read2d(it):
    with open(f"{basedir}/Si_sbe_RT_Ac/Si_Ac_{it:06d}.data", "r") as fh:
        print(fh.name)
        dat = np.loadtxt(fh)
        ix = dat[:, 1-1]
        iy = dat[:, 2-1]
        ix_min = round(np.amin(ix))
        ix_max = round(np.amax(ix))
        iy_min = round(np.amin(iy))
        iy_max = round(np.amax(iy))
        # ez2d = dat[:,  9-1].reshape([iy_max-iy_min+1,ix_max-ix_min+1]).T
        # by2d = dat[:, 11-1].reshape([iy_max-iy_min+1,ix_max-ix_min+1]).T
        jz2d = dat[:, 15-1].reshape([iy_max-iy_min+1,ix_max-ix_min+1]).T
    return jz2d

if args.nthread > 1:
    from multiprocessing import Pool
    with Pool(args.nthread) as p:
        dat2d_list = p.map(read2d, target_list)
else:
    dat2d_list = list(map(read2d, target_list))

import scipy.signal
window = scipy.signal.blackman(nt+1)

def fourier(n_order):
    omega_n = omega1 * n_order
    tmp = np.zeros_like(dat2d_list[0], dtype=complex)
    for it, dat2d in zip(target_list, dat2d_list):
        tmp += dat2d[:, :] * (np.exp(1.0j * omega_n * dt * it) * window[it])
    tmp *= (1.0 / len(dat2d_list))
    return np.abs(tmp)**2

n_order_list = list(range(args.nmax))

if args.nthread > 1:
    from multiprocessing import Pool
    with Pool(args.nthread) as p:
        fourier_list = p.map(fourier, n_order_list)
else:
    fourier_list = list(map(fourier, n_order_list))

for n_order, dat2d in zip(n_order_list, fourier_list):
    name = f"{basedir}/fourier_{n_order}.txt"
    print(name)
    np.savetxt(name, dat2d)


