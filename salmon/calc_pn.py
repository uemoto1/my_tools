#!/usr/bin/env python3

target1 = "Si_rt.data"
target2 = "Si_rt.data"
target3 = "Si_rt.data"
target4 = "Si_rt.data"
vec_e_dir = (0.0, 0.0, 1.0) # z-direction
vec_p_dir = (0.0, 0.0, 1.0) # z-direction





# DO NOT CHANGE FOLLOWING BLOCK:
import numpy as np

vec_e_dir = np.array(vec_e_dir)
vec_p_dir = np.array(vec_p_dir)
vec_e_dir = vec_e_dir * (1.0 / np.linalg.norm(vec_e_dir))
vec_p_dir = vec_p_dir * (1.0 / np.linalg.norm(vec_p_dir))

target_list = [target1, target2, target3, target4]
E_list = []
P_list = []
for item in target_list:
    print(f"# retrieving {item}")
    dat = np.loadtxt(item)
    t = dat[:, 1-1]
    E_tot_x = dat[:, 11-1]
    E_tot_y = dat[:, 12-1]
    E_tot_z = dat[:, 13-1]
    Jm_x = dat[:, 14-1]
    Jm_y = dat[:, 15-1]
    Jm_z = dat[:, 16-1]
    dt = t[1] - t[0]
    P_x = -np.cumsum(Jm_x) * dt
    P_y = -np.cumsum(Jm_y) * dt
    P_z = -np.cumsum(Jm_z) * dt
    E = np.dot(vec_e_dir, [E_tot_x, E_tot_y, E_tot_z])
    P = np.dot(vec_p_dir, [P_x, P_y, P_z])
    E_list.append(E)
    P_list.append(P)

N = len(target_list)
A = np.zeros([N, N])
it_max = np.argmax(np.abs(E_list[0]))

for i in range(N):
    E_max = E_list[i][it_max]
    for j in range(N):
        A[i, j] = E_max ** j

B = np.linalg.inv(A)
pn_list = []
for n in range(N):
    pn = np.dot(B[n, :], E_list)
    pn_list.append(pn)
    # Export pn data:
    with open(f"p{n}.txt", "w") as fh:
        print(f"# exporting {fh.name}")
        fh.write(f"# Time[au] p{n}[au]\n")
        for i in range(len(t)):
            fh.write(f"{t[i]:12.6f} {pn[i]:12.6e}\n")


epsilon_0 = 8.8541878128e-12
a_B = 5.29177210903e-11
q_e = 1.602176634e-19

for n in range(1, N):
    chi_trans_factor = (4.0*np.pi)**n * (epsilon_0 * a_B ** 2 / q_e)**(n-1)
    print(chi_trans_factor)


