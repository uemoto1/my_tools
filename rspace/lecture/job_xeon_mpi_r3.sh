#!/bin/sh
#$ -q r3
#$ -pe mpi 128
#$ -N RSPACE
#$ -V -S /bin/bash
#$ -cwd
export OMP_NUM_THREADS=16

# Do not change this section:
unset I_MPI_FALLBACK_DEVICE
unset I_MPI_MPD_RSH
export I_MPI_HYDRA_BOOTSTRAP=rsh
export I_MPI_PIN=0
export I_MPI_PERHOST=$((NSLOTS/NHOSTS/OMP_NUM_THREADS))

mpiexec.hydra ./kukan8
