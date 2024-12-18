#!/usr/bin/env python3
import numpy as np

n_order_array = np.arange(10)
angle_array = np.arange(0, 360)

import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", type=str, required=True)
parser.add_argument("-n", "--nthread", type=int, default=0)
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
target_list = list(range(1, macro+1))[:3]

import scipy.signal

# Perform fourier transformation at omega_n
def fourier(imacro):
    filepath = f"{basedir}/{sysname}_sbe_m/m{imacro:06d}/{sysname}_sbe_rt.data"
    print(filepath)
    dat = np.loadtxt(filepath, dtype=float)
    t = dat[:, 1-1]
    jm_z = dat[:, 16-1]
    nt = len(t)
    window = scipy.signal.blackman(nt)
    result_fourier = []
    for omega in omega_array:
        jm_omega = sum(jm_z * np.exp(1.0j * omega * t) * window) * (1.0 / len(t))
        result_fourier.append(jm_omega)
    return result_fourier

omega_array = n_order_array * omega1

if args.nthread > 1:
    from multiprocessing import Pool
    with Pool(args.nthread) as p:
        result_list = p.map(fourier, target_list)
else:
    result_list = list(map(fourier, target_list))

c_speed = 137.03597

tmp = np.zeros(
    [len(angle_array), len(omega_array)],
    dtype=complex
)

for imacro, result_fourier in zip(target_list, result_list):
    ix, iy, iz = point[imacro]
    x = hx_m * ix
    y = hy_m * iy
    for iangle, angle in enumerate(angle_array):
        theta = angle * (np.pi / 180.0)
        sin_theta = np.sin(theta)
        cos_theta = np.cos(theta)
        for iomega, omega in enumerate(omega_array):
            k_wave = omega / c_speed
            jm_omega = result_fourier[iomega]
            tmp[iangle][iomega] += hx_m * hy_m * (
                (-jm_omega) * np.exp(-1.0j * k_wave * (
                    x * cos_theta + y * sin_theta
                ))
            )

for iomega in n_order_array:
    n = n_order_array[iomega]
    with open(f"direction_order_{n}.txt", "w") as fh:
        print(fh.name)
        fh.write(f"# Direction at {n}-th harmonic field\n")
        fh.write("# angle' |scat|^2\n")
        for iangle, angle in enumerate(angle_array):
            scat = abs(tmp[iangle][iomega])**2
            fh.write(f"{angle:12.6f} {scat:24.12e}\n")

