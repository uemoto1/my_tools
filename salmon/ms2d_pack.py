#!/usr/bin/env python3
import numpy as np

with open("Si_sbe_ms.inp", "r") as fh:
    print(fh.name)
    for line in fh:
        tmp = line.split("=")
        if len(tmp) == 2:
            lhs = tmp[0].strip()
            rhs = tmp[1].split("!")[0].strip()

            if lhs.lower() == "omega1":
                omega1 = float(rhs.replace("d", "e"))
            if lhs.lower() == "dt":
                dt = float(rhs.replace("d", "e"))
            if lhs.lower() == "nx_m":
                nx_m = int(rhs)
            if lhs.lower() == "ny_m":
                ny_m = int(rhs)
            # if lhs.lower() == "nz_m":
            #     nz_m = int(rhs)
            if lhs.lower() == "hx_m":
                hx_m = float(rhs.replace("d", "e"))
            if lhs.lower() == "hy_m":
                hy_m = float(rhs.replace("d", "e"))
            # if lhs.lower() == "hz_m":
            #     hz_m = float(rhs.replace("d", "e"))
            if lhs.lower() == "nt":
                nt = int(rhs)
            if lhs.lower() == "i_wcm2_1":
                i_wcm2_1 = float(rhs.replace("d", "e"))
            
with open(".shape.txt", "r") as fh:
    print(fh.name)
    nmacro = int(fh.readline())
    shape = np.empty([nmacro, 3], dtype=int)
    for imacro in range(nmacro):
        line = fh.readline()
        tmp = line.split()
        shape[imacro, 0] = int(tmp[1])
        shape[imacro, 1] = int(tmp[2])
        shape[imacro, 2] = int(tmp[3])

ez_buf = []
by_buf = []
jz_buf = []
it_buf = []
my_mx = None

for it in range(100, nt, 100):
    with open(f"Si_sbe_RT_Ac/Si_Ac_{it:06d}.data", "r") as fh:
        print(fh.name)
        dat = np.loadtxt(fh)
        ez1 = dat[:,  9-1]
        by1 = dat[:, 11-1]
        jz1 = dat[:, 15-1]
        if my_mx is None:
            ix1 = np.round(dat[:, 1-1])
            iy1 = np.round(dat[:, 2-1])
            ix_min = ix1.min()
            ix_max = ix1.max()
            iy_min = iy1.min()
            iy_max = iy1.max()
            mx = ix_max - ix_min + 1
            my = iy_max - iy_min + 1
        reshape2d = lambda d: d.reshape(my_mx).T
        ez_buf.append(reshape2d(ez1))
        by_buf.append(reshape2d(by1))
        jz_buf.append(reshape2d(jz1))
        it_buf.append(it)

ez_buf = np.asarray(ez_buf, dtype=float)
by_buf = np.asarray(by_buf, dtype=float)
jz_buf = np.asarray(jz_buf, dtype=float)
it_buf = np.asarray(it_buf, dtype=int)

with open(f"{__file__}.npz", "wb") as fh:
    print(fh.name)
    np.savez_compressed(fh,
        ez=ez_buf,
        by=by_buf,
        jz=jz_buf,
        omega1=omega1,
        ix_min=ix_min,
        iy_min=iy_min,
        ix_max=ix_max,
        iy_max=iy_max,
        it=it_buf,
        dt=dt,
        nx_m=nx_m,
        ny_m=ny_m,
        hx_m=hx_m,
        hy_m=hy_m,
        nt=nt,
        i_wcm2_1=i_wcm2_1,
    )


