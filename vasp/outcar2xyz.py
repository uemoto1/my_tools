import os
import ase.io
from sklearn.model_selection import train_test_split

basedir = "./"
ratio = 0.10 # ratio for validation dataset
seed = 1234 # random seed to split data

data = []
for dirname, dirlist, filelist in os.walk(basedir):
    if "OUTCAR" in filelist:
        atoms = ase.io.read(os.path.join(dirname, "OUTCAR"))
        data.append(atoms)

train, valid = train_test_split(data, test_size=ratio, random_state=seed)

ase.io.write("data.xyz", data, format="extxyz")
ase.io.write("train.xyz", train, format="extxyz")
ase.io.write("valid.xyz", valid, format="extxyz")

print("# data.xyz : train.xyz (%d) valid.xyz (%d)" % (len(train), len(valid)))
