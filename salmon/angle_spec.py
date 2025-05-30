ia01 004_cylinder_5e12]$ cat ../angle_spec.py 
#!/usr/bin/env python3
import numpy as np

angle_array = np.array([0.0, 30.0, 60.0, 90.0, 120.0, 150.0, 180.0])
omega_array = np.linspace(0.0, 10.0/27.2, 1000)

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

with open(f"{basedir}/.shape.txt", "r") as fh:
    print(fh.name)
    macro = int(fh.readline())
    point = {}
    for i in range(macro):
        line = fh.readline()
        tmp = line.split()
        imacro, ix, iy, iz = map(int, tmp[0:4])
        point[imacro] = (ix, iy, iz)
target_list = list(range(1, macro+1))

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

if args.nthread > 1:
    from multiprocessing import Pool
    with Pool(args.nthread) as p:
        result_list = p.map(fourier, target_list)
else:
    result_list = list(map(fourier, target_list))

c_speed = 137.03597

for iangle, angle in enumerate(angle_array):
    theta = angle * (np.pi / 180.0)
    sin_theta = np.sin(theta)
    cos_theta = np.cos(theta)
    tmp = np.zeros_like(omega_array, dtype=complex)

    for imacro, result_fourier in zip(target_list, result_list):
        ix, iy, iz = point[imacro]
        x = hx_m * ix
        y = hy_m * iy
        for iomega, omega in enumerate(omega_array):
            k_wave = omega / c_speed
            jm_omega = result_fourier[iomega]
            tmp[iomega] += hx_m * hy_m * (
                (-jm_omega) * np.exp(-1.0j * k_wave * (
                    x * cos_theta + y * sin_theta
                ))
            )

    with open(f"angle_spec_{angle:03.0f}.txt", "w") as fh:
        print(fh.name)
        fh.write(f"# Spectra at {angle} deg.\n")
        fh.write("# omega scat\n")
        for iomega, omega in enumerate(omega_array):
            scat = abs(tmp[iomega])**2
            fh.write(f"{omega:12.6f} {scat:24.12e}\n")

            
