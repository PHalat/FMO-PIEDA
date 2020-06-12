#!/bin/python3

import glob
import os
import sys
import shutil

os.system("cp ../3*/*pbs ../3*/*inp ./")
# os.system("for file in *F30*; do mv $file ${file//F30/F40}; done")

# Let's start by recognizing all input files

inps = glob.glob("*inp")

# Let's remove PIEDA data

for inpy in inps:
    inp = open(inpy,"r")
    inp2 = inp.readlines()
    inp.close()

    for i in range(len(inp2)):
        if "$FMOPRP" in inp2[i]:
            for j in range(i+1,len(inp2)):
                if "$END" in inp2[j]:
                    del(inp2[i:j+1])
                    break
            break 

    for i in range(len(inp2)):
        if "NGROUP=1" in inp2[i]:
            inp2[i] = inp2[i].replace("NGROUP=1","NGROUP=2")
        if "NBODY=2" in inp2[i]:
            inp2[i] = inp2[i].replace("NBODY=2","NBODY=3")
            break
 
    outinp = open(inpy,"w")
    for i in inp2:
        outinp.write(i)
    outinp.close()

    pbs = open(inpy[:-4] + ".pbs", "r")
    pbs2 = pbs.readlines()
    pbs.close()

    for i in range(len(pbs2)):
        if "walltime" in pbs2[i]:
            pbs2[i] = "#PBS -l walltime=24:00:00 \n"
            break

    pbs = open(inpy[:-4] + ".pbs","w")
    for i in pbs2:
        pbs.write(i)
    pbs.close()

#os.system("cp ../1*/*pbs ../1*/*inp ../1*/*F30* ./")
#os.system("for file in *F30*; do mv $file ${file//F30/F40}; done")
#os.system('for file in *inp; do sed "s/FMO0/ENERGY/g" $file > ${file}2; sed "s/NBODY=1/NBODY=2/g" ${file}2 > ../2POL/$file')
#os.system('rm -r *inp2')
