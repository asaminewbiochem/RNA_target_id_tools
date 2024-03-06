#!/usr/bin/python
"""
 Monte Carlo reweight dihedral force constant
 Asaminew Haile Aytenfisu 2017
"""

import math
from math import sqrt, pi, cos, sin
import random
import string
import sys
import copy
import os
from datetime import datetime
start_time = datetime.now()


ctoff = float(sys.argv[2])
run = str(sys.argv[1])
now = datetime.now()
wrmsd = 10.0
tempr0 = 300.0
nstep = 5000

print """
Monte Carlo reweight dihedral fitting
Reweight using RMSD with NMR Jcoupling as a target function
"""

# File name containing lists of dihedral atom types
print "Number of path for phi?"
ndih = int(string.strip(sys.stdin.readline()))
print "number of paths for phi is %i" % (ndih)

i = 0
phipsi = {}
phipsiname = []
dihedral_charmm = []
dihedral_charmmr = []
# Go through individual lines and extract atom type and thier value from the trajectories
while i < ndih:
    print "What is the file path for the dih%i?" % (i + 1)
#	path        = string.strip( sys.stdin.readline() )
    print "What is the file name of the dih%i?" % (i + 1)
    file = string.strip(sys.stdin.readline())
    print "  dih%i file = %s" % (i + 1,  file)
    in_file = open("%s.dihe" % (file), "r")
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
    print "Read %i phi." % (nconf)
    i += 1

# Reading in  initial paramter
print "Number of parameters"
nparm = int(string.strip(sys.stdin.readline()))
print "Number of NMR is %i " % (nparm)


parm = {}
print "What is the original parameter file name path %i?" % (i+1)
file = string.strip(sys.stdin.readline())
print "parameter file %i = %s" % (i+1, file)
in_file = open("%s.parm" % (file), "r")
ipar = 0
for line in in_file.readlines():
    field = string.split(string.strip(line))
    atomindex = str(field[0])+" "+str(field[1])+" " + \
        str(field[2])+" "+str(field[3])
    if not atomindex in parm.keys():
        parm[atomindex] = [[float(field[4]), int(field[5]), float(field[6])]]
    else:
        parm[atomindex].append(
            [float(field[4]), int(field[5]), float(field[6])])
    ipar += 1

# Reading in  NMR for each frame of the trajectories
print "Number of NMR files"
nmr = int(string.strip(sys.stdin.readline()))
print "Number of NMR is %i " % (nmr)

i = 0
dih_nmr = {}
nmrname = []
while i < nmr:
    print "What is the file path for the nmr%i file?" % (i + 1)
#	path           = string.strip( sys.stdin.readline() )
    print "What is the file name of the nmr%i file?" % (i + 1)
    file = string.strip(sys.stdin.readline())
    nmrname.append(file)
    print "  nmr%i file = %s" % (i + 1, file)
    nconf = 0
    dih_nmr[file] = []
    in_file = open("%s.nmr" % (file), "r")
    for line in in_file.readlines():
        field = string.split(string.strip(line))
        dih_nmr[file].append(float(field[0]) - float(field[1]))
        nconf += 1
    i += 1


# Populate table with precomputed values for cosine function
cosfun = []
nconfdi = 0
while nconfdi < nconf:
    cosfun.append([])
    i = 0
    for k in phipsiname:
        j = 0
        val = parm.get(k[1])
        cosfun[nconfdi].append([])
        for value in range(0, len(val)):
            cosfun[nconfdi][i].append(
                1.0 + cos(phipsi[k[0]][nconfdi] * parm[k[1]][j][1] * pi/180.0 - parm[k[1]][j][2] * pi/180.0))
            j += 1
        i += 1
    nconfdi += 1

# Calculate charmm dihedral energy


def energy(parm):
    nconfdi = 0
    e = []
    while nconfdi < nconf:
        e.append(0.0)
        i = 0
        for k in phipsiname:
            j = 0
            val = parm.get(k[1])
            for value in range(0, len(val)):
                e[nconfdi] = e[nconfdi] + \
                    parm[k[1]][j][0] * cosfun[nconfdi][i][j]
                j += 1
            i += 1
        nconfdi += 1
    return e


# Reading in  phi/psi
print "Number of phi/psi files"
phipsi = int(string.strip(sys.stdin.readline()))
print "Number of phi/psi is %i " % (phipsi)

i = 0
dih_phipsi_alpha = {}
dih_phipsi_beta = {}
dih_phipsi_pii = {}

phipsi_name = []
while i < phipsi:
    print "What is the file path for the phipsi%i file?" % (i + 1)
#	path           = string.strip( sys.stdin.readline() )
    print "What is the file name of the phipsi%i file?" % (i + 1)
    file = string.strip(sys.stdin.readline())
    phipsi_name.append(file)
    print "  phipsi%i file = %s" % (i + 1, file)
    nconf = 0
    dih_phipsi_alpha[file] = []
    dih_phipsi_beta[file] = []
    dih_phipsi_pii[file] = []
    in_file = open("%s.phipsi" % (file), "r")
    for line in in_file.readlines():
        field = string.split(string.strip(line))
        x = float(field[0])
        y = float(field[1])
        if ((-95 < x < -40) and (-70 < y < -32)) or ((-107 < x < -40) and (-32 < y < -12)) or ((-165 < x < -95) and (-70 < y < -32)) or ((-107 < x < -40) and (-12 < y < 8)) or ((-150 < x < -67) and (8 < y < 40)) or ((-150 < x < -107) and (-32 < y < 8)):
            dih_phipsi_alpha[file].append(1.0)
            dih_phipsi_beta[file].append(0.0)
            dih_phipsi_pii[file].append(0.0)
        elif ((-135 < x < -100) and (95 < y < 150)) or ((-175 < x < -135) and (95 < y < 136)) or ((-180 < x < -135) and (136 < y < 180)) or ((-135 < x < -105) and (150 < y < 180)) or ((-180 < x < -135) and (-180.1 < y < -160)):
            dih_phipsi_alpha[file].append(0.0)
            dih_phipsi_beta[file].append(1.0)
            dih_phipsi_pii[file].append(0.0)
        elif ((-100.0 < x < -30.0) and (95.0 < y < 180.0)) or ((-100.0 < x < -60.0) and (-180.1 < y < -150.0)):
            dih_phipsi_alpha[file].append(0.0)
            dih_phipsi_beta[file].append(0.0)
            dih_phipsi_pii[file].append(1.0)
        else:
            dih_phipsi_alpha[file].append(0.0)
            dih_phipsi_beta[file].append(0.0)
            dih_phipsi_pii[file].append(0.0)

        nconf += 1
    i += 1


def weight(parm, parm_new):
    e = energy(parm_new)
    e0 = energy(parm)
    w1 = []
    wa = []
    wb = []
    wp = []
    w0 = []
    nconfnmr = 0
    invkt = -1.0 / (0.0019872041*300)
    while nconfnmr < nconf:
        w0.append(math.exp((e0[nconfnmr] - e[nconfnmr]) * (invkt)))
        wa.append(dih_phipsi_alpha[phipsi_name[0]][nconfnmr]
                  * math.exp((e0[nconfnmr] - e[nconfnmr]) * (invkt)))
        wb.append(dih_phipsi_beta[phipsi_name[0]][nconfnmr]
                  * math.exp((e0[nconfnmr] - e[nconfnmr]) * (invkt)))
        wp.append(dih_phipsi_pii[phipsi_name[0]][nconfnmr]
                  * math.exp((e0[nconfnmr] - e[nconfnmr]) * (invkt)))
        w1.append((abs(dih_nmr[nmrname[0]][nconfnmr]) + abs(dih_nmr[nmrname[1]]
                                                            [nconfnmr])) * math.exp((e0[nconfnmr] - e[nconfnmr]) * (invkt)))
        nconfnmr += 1


def move(parmnew):
    i = 0
    for k in phipsiname:
        j = 0
        val = parmnew.get(k[1])
        for value in range(0, len(val)):
            if j < 3:
                parmnew[k[1]][j][0] = parmnew[k[1]][j][0] + \
                    random.uniform(-0.005, 0.005)
            if j == 3:
                parmnew[k[1]][j][0] = parmnew[k[1]][j][0] + \
                    random.uniform(-0.001, 0.001)
            else:
                parmnew[k[1]][j][0] = parmnew[k[1]][j][0] + \
                    random.uniform(-0.0001, 0.0001)
            if parmnew[k[1]][j][0] > kmax:
                parmnew[k[1]][j][0] = kmax
            elif parmnew[k[1]][j][0] < kmin:
                parmnew[k[1]][j][0] = -parmnew[k[1]][j][0]
            j += 1
        i += 1
    return parmnew


def rmsd_parm(parm_old, parm_new):
    rmsd_param = 0.0
    i = 0
    cnt = 0
    for k in phipsiname:
        j = 0
        val_old = parm_old.get(k[1])
        val_new = parm_new.get(k[1])
        for value in range(0, len(val_old)):
            rmsd_param = rmsd_param + \
                (parm_old[k[1]][j][0] - parm_new[k[1]][j][0]) ** 2
            j += 1
            cnt += 1
        i += 1
    return sqrt(rmsd_param) / cnt


cutof = 0.012
tar_best = 99.0
tar_old = 99.0
dtar = 99.0
tar_new = 99.0
istep = 0
parmbest = []
parmcopy = []
kmin = 0.0
kmax = 3.0
phasemin = 0.0
varyphase = 0
parm_old = copy.deepcopy(parm)
while istep < nstep:
    parm_new = copy.deepcopy(parm_old)
    parmlist = []
    par = []
    problist = []
    if istep > 200:
        irang = 200
    else:
        irang = istep
    for i in range(irang+1):
        par.append(move(parm_new))
        parmlist.append(par[i])
        if weight(par[i], parm)[4]:
            problist.append(weight(par[i], parm)[0] + 1.0*abs(weight(par[i], parm)[1] - 0.05) + 1.0*abs(
                weight(par[i], parm)[2] - 0.56) + 1.0*abs(weight(par[i], parm)[3]-0.39))
        else:
            problist.append(99.0)

    ind = problist.index(min(problist))
    prob = problist[ind]
    if qweight == True:
        cutof += 0.00005
        rmsdw = rmsd_parm(parm, parmlist[ind])
        tempr = tempr0 * math.exp(-1.0 * (float(istep) / (float(nstep) / 4.0)))
        tar_new = math.log(prob) + 1.0 * rmsdw
        dtar = tar_new - tar_old
        if istep == 0:
            p = 0.0  # required to prevent overflow
        else:
            dtar = tar_new - tar_old
            boltz = -1.0 * dtar / (0.001987 * tempr)
            p = math.exp(boltz)
        p0 = random.uniform(0.0, 1.0)
        if dtar < 0.0:
            accepted = 1
            p = 1.0
        elif p0 < p:
            accepted = 1
        else:
            accepted = 0
        if accepted:
            tar_old = tar_new
            parm_old = copy.deepcopy(parmlist[ind])
            if tar_new < tar_best:
                tar_best = tar_new
                prob_best = prob
                parm_best = copy.deepcopy(parmlist[ind])
                rmsd_best = rmsdw
        if (istep % 10) == 0:
            print "%6i%9.5f%9.5f%9.5f" % (istep,  prob_best, rmsdw, tar_best)
    istep += 1

# Print the final parameter
out_file = open("parm/reweight.%s.str" % (run), "w")
out_file.write("* toppar_drude_model.str\n\
* reweight\n\
*\n\n\n\
read para card append\n\
* reweight: by ahaile %s/%s/%s\n\
* target_function   = %f \n\
* probability       = %f \n\
* wrmsd             = %f \n\
* nstep             = %i \n\
* Temprature        = %f \n\
* Best_RMSD         = %f \n\
*\n\n\n\
BONDS\n\nANGLES \n\nDIHEDRALS\n" % (now.month,  now.day, now.year, tar_best, prob_best, wrmsd, nstep, tempr0, rmsd_best))

# Remove any duplicated paramer from the trajectories entry
# There may be trajectories that share same dihedral

finale = []
for line in dihedral_charmm:
    if line not in finale:
        finale.append(line)
i = 0
for line in finale:
    j = 0
    a, b, c, d = line.split(" ")
    val = parm_best.get(line)
    for value in range(0, len(val)):
        out_file.write("%-9s%-9s%-9s%-9s%9.4f%3i%9.2f\n" %
                       (a, b, c, d, parm_best[line][j][0], parm_best[line][j][1], parm_best[line][j][2]))
        j += 1
    i += 1

out_file.write("\n\nIMPROPERS\n\nEND\n")

# Print MM energy using original and best parameter together with their difference
# for visual perpose, minimum of energy surface is at zero.
out_ene = open("parm/reweight.%s.ene" % (run), "w")
nconfdi = 0
ee0 = []
eeb = []
min0 = min(energy(parm))
minb = min(energy(parm_best))
while nconfdi < nconf:
    ee0.append(0.0)
    eeb.append(0.0)
    i = 0
    for k in phipsiname:
        j = 0
        val = parm.get(k[1])
        for value in range(0, len(val)):
            ee0[nconfdi] = ee0[nconfdi] + \
                parm[k[1]][j][0] * cosfun[nconfdi][i][j]
            eeb[nconfdi] = eeb[nconfdi] + \
                parm_best[k[1]][j][0] * cosfun[nconfdi][i][j]
            j += 1
        i += 1
    out_ene.write("%8.3f %8.3f %8.3f  \n" % (
        ee0[nconfdi] - min0, eeb[nconfdi] - minb, (ee0[nconfdi]-eeb[nconfdi])))
    nconfdi += 1

end_time = datetime.now()
print('Duration: {}'.format(end_time - start_time))
