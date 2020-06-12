#!/bin/python3

import glob
import os
import sys
import shutil

os.system("cp ../1*/*pbs ../1*/*inp ../1*/*dat ../1*/*F30* ./")
os.system("for file in *F30*; do mv $file ${file//F30/F40}; done")

# Let's start by recognizing all .dat files

outputs = glob.glob("*dat")

# Let's extract eFMO0 data

for output in outputs:
    data = open(output,"r")
    data2 = data.readlines()[-100:]
    data.close()

    efmo = []

    corr = True

    for i in range(len(data2)):
        if "efmo0" in data2[i]:
            anchor = i
            efmo.append(data2[anchor])
            while corr:
                anchor += 1
                if "ecorr" in data2[anchor]:
                    corr = False
                else:
                    efmo.append(data2[anchor])
            break

    efmo.append(" $END \n")

    inp = open(output[:-4] + ".inp","r")
    inp2 = inp.readlines()
    inp.close()

    for i in range(len(inp2)):
        if "$FMOPRP" in inp2[i]:
            inp2[i] = " $FMOPRP IREST=2 MAXIT=1 MODORB=3 IPIEDA=2 MODPAR=77 \n"
            inp2[i+1:i+1] = efmo
            break 

    for i in range(len(inp2)):
        if "RUNTYP=FMO0" in inp2[i]:
            inp2[i] = inp2[i].replace("RUNTYP=FMO0","RUNTYP=ENERGY")
        if "NBODY=1" in inp2[i]:
            inp2[i] = inp2[i].replace("NBODY=1","NBODY=2")
            break
 
    outinp = open(output[:-4] + ".inp","w")
    for i in inp2:
        outinp.write(i)
    outinp.close()

#os.system("cp ../1*/*pbs ../1*/*inp ../1*/*F30* ./")
#os.system("for file in *F30*; do mv $file ${file//F30/F40}; done")
#os.system('for file in *inp; do sed "s/FMO0/ENERGY/g" $file > ${file}2; sed "s/NBODY=1/NBODY=2/g" ${file}2 > ../2POL/$file')
#os.system('rm -r *inp2')
