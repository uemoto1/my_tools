#!/bin/sh
#$ -q r3
#$ -pe smp 64
#$ -N RSPACE
#$ -V -S /bin/bash
#$ -cwd
export OMP_NUM_THREADS=$NSLOTS

mpiexec.hydra -n 1 ./kukan8

