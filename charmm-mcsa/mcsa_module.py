#!/usr/bin/env python3
"""
Monte Carlo reweight dihedral force constant
Asaminew Haile Aytenfisu 2017, Updated 2024
"""

import sys
import os
import math
import random
from datetime import datetime

# Global variables (consider encapsulating these in a class or a more structured format)
phipsi = {}
phipsiname = []
dihedral_charmm = []
dihedral_charmmr = []


def read_dihedral_index(ndih):
    global phipsi, phipsiname, dihedral_charmm, dihedral_charmmr
    for _ in range(ndih):
        file = input().strip()
        with open(f"tmp.{file}.parm", "r") as in_file:
            field = in_file.readline().strip().split()
            if len(field) != 4:
                raise ValueError(f"The first line in {file} must contain four fields corresponding to atom types.")
            atomindex = " ".join(field)
            dihedral_charmm.append(atomindex)
            phipsiname.append([file, atomindex])
            phipsi[file] = [float(line.split()[0]) for line in in_file]
    return len(phipsi)


def mm_qm_read(dih_qm, nlin, filepath):
    dih_qm.clear()
    with open(filepath, "r") as in_file:
        for _ in range(nlin):
            dih_qm.extend(float(line.strip().split()[0]) for line in in_file)
    return dih_qm


def parmread(filename):
    param = {}
    with open(filename, "r") as in_file:
        for line in in_file:
            fields = line.strip().split()
            atomindex = " ".join(fields[:4])
            if atomindex not in param:
                param[atomindex] = []
            param[atomindex].append([float(fields[4]), int(fields[5]), float(fields[6])])
    return param


def param2print(inputparm, filepath, probab='NA'):
    now = datetime.now()
    with open(filepath, "w") as out_file:
        out_file.write(f"* mcsa parameter\n* reweight function {probab} \n*\n\n\nread para card append \n")
        out_file.write(f"* reweight: by ahaile on {now.month}/{now.day}/{now.year}\n*\n\nBONDS\n\nANGLES\n\nDIHEDRALS\n")
        for line in set(dihedral_charmm):
            a, b, c, d = line.split()
            for k, (v1, v2, v3) in enumerate(inputparm.get(line, [])):
                out_file.write(f"{a:<9}{b:<9}{c:<9}{d:<9}{v1:9.4f}{v2:3d}{v3:9.2f}\n")
        out_file.write("\n\nIMPROPERS\n\nEND\n\n")


def param_update(parmnew, parm_old, kmin, kmax):
    for i, (file, atomindex) in enumerate(phipsiname):
        for j, _ in enumerate(parmnew.get(atomindex, [])):
            if i <= 4:
                update_rule = j < 2 or j == 2  # Simplify conditional logic here
            else:
                update_rule = j < 2 or j == 2 or j > 3  # Adjust as per your logic
            if update_rule:
                parmnew[atomindex][j][0] = random.uniform(-0.4, 0.4) + parm_old[atomindex][j][0]
                parmnew[atomindex][j][0] = max(min(parmnew[atomindex][j][0], kmax), kmin)
            # Adjust phase as needed; example shown, adjust as per your actual requirement
            parmnew[atomindex][j][2] = parm_old[atomindex][j][2]
    return parmnew


def param_random_initial(parmnew, kmin, kmax):
    for _, atomindex in phipsiname:
        for j, _ in enumerate(parmnew.get(atomindex, [])):
            if j < 2:
                parmnew[atomindex][j][0] = random.uniform(-2.75, 2.75)
            elif j == 2:
                parmnew[atomindex][j][0] = random.uniform(-1.5, 1.5)
            else:
                parmnew[atomindex][j][0] = random.uniform(-0.25, 0.25)
            # Correct phase and k range handling as per logic
            parmnew[atomindex][j][0] = max(min(parmnew[atomindex][j][0], kmax), kmin)
            parmnew[atomindex][j][2] = random.choice([0.0, 180.0])
    return parmnew


def read_mm_energy(mm, runi, stepi, jobid, f, run):
    curren = []
    for _ in range(mm):
        with open(f"tmp.{jobid}.{f}.{run}.{runi}.{stepi}.mme", "r") as in_file:
            curren.extend(float(line.strip().split()[0]) for line in in_file)
    return curren


def RMSE(dih_qm, qm, mm, runi, stepi, jobid, f, run):
    dih_qm = mm_qm_read(dih_qm, qm, f"{f}.qm")
    emm = read_mm_energy(mm, runi, stepi, jobid, f, run)
    
    qmin_p1 = sum(dih_qm[:1544])/1544
    qmin_p0 = sum(dih_qm[1544:])/1396
    
    emin_p1 = sum(emm[:1544])/1544
    emin_p0 = sum(emm[1544:])/1396
    
    resi_p1 = sum((dih_qm[i] - qmin_p1 - (emm[i] - emin_p1))**2 for i in range(1544))
    resi_p0 = sum((dih_qm[i] - qmin_p0 - (emm[i] - emin_p0))**2 for i in range(1544, len(dih_qm)))
    
    rmse_p1 = math.sqrt(resi_p1/1544)
    rmse_p0 = math.sqrt(resi_p0/1396)
    
    return rmse_p1 + rmse_p0