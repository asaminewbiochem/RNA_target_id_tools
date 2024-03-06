#!/usr/bin/python2.7
"""
Monte Carlo reweight dihedral force constant
Asaminew Haile Aytenfisu 2017
"""

import string
import sys
import copy
import os
import math
from math import sqrt
import random
from datetime import datetime
now = datetime.now()


def read_dihedral_index(ndih):
    global phipsi
    global phipsiname
    global dihedral_charmm
    global dihedral_charmmr
    i = 0
    phipsi = {}
    phipsiname = []
    dihedral_charmm = []
    dihedral_charmmr = []
    while i < ndih:
        file = string.strip(sys.stdin.readline())
        in_file = open("tmp.%s.parm" % (file), "r")
        field = string.split(string.strip(in_file.readline()))
        if len(field) != 4:
            raise "The first line in %s must contain four fields corresponding to atom types." % (
                file)
        atomindex = str(field[0])+" "+str(field[1])+" " + \
            str(field[2])+" "+str(field[3])
        dihedral_charmm.append(atomindex)
        phipsiname.append([file, atomindex])
        phipsi[file] = []
        nconf = 0
        for line in in_file.readlines():
            field = string.split(string.strip(line))
            phipsi[file].append(float(field[0]))
            nconf += 1
        i += 1
    return i


# Read QM Energy
def mm_qm_read(dih_qm, nlin, filepath):
    i = 0
    dih_qm = []
    while i < nlin:
        nconf = 0
        in_file = open("%s" % (filepath), "r")
        for line in in_file.readlines():
            field = string.split(string.strip(line))
            dih_qm.append(float(field[0]))
            nconf += 1
        i += 1
    return dih_qm


def parmread(filename, param):
    # read initial dihedral parameter or read modified dihedral from mcsa iteslfwwwww
    jpar = 0
    param = {}
    in_file = open("%s" % (filename), "r")
    for line in in_file.readlines():
        field = string.split(string.strip(line))
        atomindex = str(field[0])+" "+str(field[1])+" " + \
            str(field[2])+" "+str(field[3])
        if not atomindex in param.keys():
            param[atomindex] = [
                [float(field[4]), int(field[5]), float(field[6])]]
        else:
            param[atomindex].append(
                [float(field[4]), int(field[5]), float(field[6])])
    jpar += 1
    return param


def param2print(inputparm, filepath, probab='NA'):
    out_file = open(filepath,  "w")
    out_file.write("* mcsa parameter\n\
* reweight function %s \n\
* \n \n \n\
read para card append \n\
* reweight: by ahaile on %s/%s/%s\n\
* \n \n \n\
BONDS \n \nANGLES \n \nDIHEDRALS \n" % (probab, now.month,  now.day, now.year))

    current = []
    for line in dihedral_charmm:
        if line not in current:
            current.append(line)
    i = 0
    for line in current:
        j = 0
        a, b, c, d = line.split(" ")
        val = inputparm.get(line)
        for value in range(0, len(val)):
            out_file.write("%-9s%-9s%-9s%-9s%9.4f%3i%9.2f\n" %
                           (a, b, c, d, inputparm[line][j][0], inputparm[line][j][1], inputparm[line][j][2]))
            j += 1
        i += 1
    out_file.write("\n \nIMPROPERS \n \nEND \n \n")
    out_file.close()


def param_update_partial(parmnew, parm_old, kmin, kmax):
    i = 0
    for k in phipsiname:
        if i <= 4:
            j = 0
            val = parmnew.get(k[1])
            for value in range(0, len(val)):
                if j < 2:  # n=1 & 2
                    parmnew[k[1]
                            ][j][0] = parm_old[k[1]][j][0]
                elif j == 2:  # n=3
                    parmnew[k[1]
                            ][j][0] = parm_old[k[1]][j][0]
                else:  # n=6
                    parmnew[k[1]
                            ][j][0] = parm_old[k[1]][j][0]

                parmnew[k[1]][j][2] = parm_old[k[1]][j][2]  # phase no update
                if parmnew[k[1]][j][0] > kmax:
                    parmnew[k[1]][j][0] = kmax
                elif parmnew[k[1]][j][0] < kmin:
                    parmnew[k[1]][j][0] = -parmnew[k[1]][j][0]  # dihedral >0
                j += 1
        else:
            j = 0
            val = parmnew.get(k[1])
            for value in range(0, len(val)):
                if j < 2:  # n=1 & 2
                    parmnew[k[1]
                            ][j][0] = random.uniform(-0.4, 0.0) + parm_old[k[1]][j][0]
                elif j == 2:  # n=3
                    parmnew[k[1]
                            ][j][0] = random.uniform(-0.3, 0.0) + parm_old[k[1]][j][0]
                else:  # n=6
                    parmnew[k[1]
                            ][j][0] = random.uniform(-0.1, 0.1) + parm_old[k[1]][j][0]

                parmnew[k[1]][j][2] = parm_old[k[1]][j][2]  # phase no update
                if parmnew[k[1]][j][0] > kmax:
                    parmnew[k[1]][j][0] = kmax
                elif parmnew[k[1]][j][0] < kmin:
                    parmnew[k[1]][j][0] = -parmnew[k[1]][j][0]  # dihedral >0
                j += 1
        i += 1
    return parmnew


def param_random_initial(parmnew, kmin, kmax):
    i = 0
    for k in phipsiname:
        j = 0
        val = parmnew.get(k[1])
        for value in range(0, len(val)):
            if j < 2:
                parmnew[k[1]
                        ][j][0] = random.uniform(-2.75, 2.75)
            elif j == 2:
                parmnew[k[1]
                        ][j][0] = random.uniform(-1.5, 1.5)
            else:
                parmnew[k[1]
                        ][j][0] = random.uniform(-0.25, 0.25)

            if parmnew[k[1]][j][0] > kmax:
                parmnew[k[1]][j][0] = kmax
            elif parmnew[k[1]][j][0] < kmin:
                parmnew[k[1]][j][0] = -parmnew[k[1]][j][0]

            parmnew[k[1]][j][2] = random.uniform(-1.0, 1.0)
            if parmnew[k[1]][j][2] < 0.0:
                parmnew[k[1]][j][2] = 0.0
            else:
                parmnew[k[1]][j][2] = 180.0
            j += 1
        i += 1
    return parmnew


def read_mm_energy(mm, runi, stepi, jobid, f, run):
    curren = []
    i = 0
    while i < mm:
        in_file = open("tmp.%s.%s.%s.%s.%s.mme" %
                       (jobid, f, run, runi, stepi), "r")
        nconf = 0
        for line in in_file.readlines():
            field = string.split(string.strip(line))
            curren.append(float(field[0]))
            nconf += 1
        i += 1
    return curren


def RMSE(dih_qm, qm, mm, runi, stepi, jobid, f, run):
    dih_qm = mm_qm_read(dih_qm, qm, "%s.qm" % (f))
    emm = read_mm_energy(mm, runi, stepi, jobid, f, run)
    qmin_p1 = sum(dih_qm[:1544])/1544
    qmin_p0 = sum(dih_qm[1544:])/1396
    emin_p1 = sum(read_mm_energy(mm, runi, stepi, jobid, f, run)[:1544])/1544
    emin_p0 = sum(read_mm_energy(mm, runi, stepi, jobid, f, run)[1544:])/1396
    i = 0
    resi_p1 = 0.0
    resi_p0 = 0.0
    ss = 0
    while i < len(dih_qm):
        if i < 1544:
            resi_p1 = resi_p1 + (dih_qm[i] - qmin_p1 - (emm[i] - emin_p1)) * \
                (dih_qm[i] - qmin_p1 - (emm[i] - emin_p1))
        else:
            resi_p0 = resi_p0 + (dih_qm[i] - qmin_p0 - (emm[i] - emin_p0)) * \
                (dih_qm[i] - qmin_p0 - (emm[i] - emin_p0))
        i += 1
    return math.sqrt(resi_p1/1544) + math.sqrt(resi_p0/1396)
