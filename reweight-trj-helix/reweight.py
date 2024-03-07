#!/usr/bin/python
"""
Monte Carlo reweight dihedral force constant
Asaminew Haile Aytenfisu 2017
"""

import math
import random
import string
import sys
import copy
from datetime import datetime

def read_dihedral_files():
    """
    Read dihedral files and extract atom types and values from trajectories.
    """
    dihedral_charmm = []
    phipsiname = []

    print("\nMonte Carlo reweight dihedral fitting\nReweight using RMSD with NMR Jcoupling as a target function\n")

    # Get the number of dihedral paths
    ndih = int(input("Number of paths for phi? "))
    print(f"Number of paths for phi is {ndih}")

    for i in range(ndih):
        file = input(f"What is the file name of the dihedral path {i + 1}? ")
        print(f"  dih{i + 1} file = {file}")
        in_file = open(f"{file}.dihe", "r")

        # Read atom types
        field = string.split(string.strip(in_file.readline()))
        atomindex = f"{field[0]} {field[1]} {field[2]} {field[3]}"
        dihedral_charmm.append(atomindex)
        phipsiname.append([file, atomindex])

        # Read dihedral values
        phipsi[file] = [float(line.split()[0]) for line in in_file.readlines()]
        nconf = len(phipsi[file])
        print(f"Read {nconf} phi for {file}")

    return dihedral_charmm, phipsiname

def read_parameter_file():
    """
    Read the original parameter file.
    """
    parm = {}
    print("Number of parameters")
    nparm = int(input())
    print(f"Number of NMR is {nparm}")

    file = input("What is the original parameter file name path? ")
    print(f"Parameter file = {file}")
    in_file = open(f"{file}.parm", "r")

    ipar = 0
    for line in in_file.readlines():
        field = string.split(string.strip(line))
        atomindex = f"{field[0]} {field[1]} {field[2]} {field[3]}"
        if atomindex not in parm.keys():
            parm[atomindex] = [[float(field[4]), int(field[5]), float(field[6])]]
        else:
            parm[atomindex].append([float(field[4]), int(field[5]), float(field[6])])
        ipar += 1

    return parm

def read_nmr_files():
    """
    Read NMR files for each frame of the trajectories.
    """
    dih_nmr = {}
    nmrname = []

    print("Number of NMR files")
    nmr = int(input())
    print(f"Number of NMR is {nmr}")

    for i in range(nmr):
        file = input(f"What is the file name of the NMR file {i + 1}? ")
        nmrname.append(file)
        print(f"  NMR{i + 1} file = {file}")
        dih_nmr[file] = [float(line.split()[0]) - float(line.split()[1]) for line in open(f"{file}.nmr", "r").readlines()]

    return dih_nmr, nmrname

def read_phi_psi_files():
    """
    Read phi/psi files and extract alpha, beta, and pi values.
    """
    dih_phipsi_alpha = {}
    dih_phipsi_beta = {}
    dih_phipsi_pii = {}
    phipsi_name = []

    print("Number of phi/psi files")
    phipsi = int(input())
    print(f"Number of phi/psi is {phipsi}")

    for i in range(phipsi):
        file = input(f"What is the file name of the phi/psi file {i + 1}? ")
        phipsi_name.append(file)
        print(f"  phi/psi{i + 1} file = {file}")

        dih_phipsi_alpha[file] = []
        dih_phipsi_beta[file] = []
        dih_phipsi_pii[file] = []

        for line in open(f"{file}.phipsi", "r").readlines():
            x, y = map(float, line.split())

            # Assign alpha, beta, and pi values based on specific conditions
            if (-95 < x < -40 and -70 < y < -32) or (-107 < x < -40 and -32 < y < -12) or (-165 < x < -95 and -70 < y < -32) or (-107 < x < -40 and -12 < y < 8) or (-150 < x < -67 and 8 < y < 40) or (-150 < x < -107 and -32 < y < 8):
                dih_phipsi_alpha[file].append(1.0)
                dih_phipsi_beta[file].append(0.0)
                dih_phipsi_pii[file].append(0.0)
            elif (-135 < x < -100 and 95 < y < 150) or (-175 < x < -135 and 95 < y < 136) or (-180 < x < -135 and 136 < y < 180) or (-135 < x < -105 and 150 < y < 180) or (-180 < x < -135 and -180.1 < y < -160):
                dih_phipsi_alpha[file].append(0.0)
                dih_phipsi_beta[file].append(1.0)
                dih_phipsi_pii[file].append(0.0)
            elif (-100.0 < x < -30.0 and 95.0 < y < 180.0) or (-100.0 < x < -60.0 and -180.1 < y < -150.0):
                dih_phipsi_alpha[file].append(0.0)
                dih_phipsi_beta[file].append(0.0)
                dih_phipsi_pii[file].append(1.0)
            else:
                dih_phipsi_alpha[file].append(0.0)
                dih_phipsi_beta[file].append(0.0)
                dih_phipsi_pii[file].append(0.0)

    return dih_phipsi_alpha, dih_phipsi_beta, dih_phipsi_pii, phipsi_name

def energy(parm, cosfun):
    """
    Calculate the CHARMM dihedral energy.
    """
    nconfdi = 0
    e = []

    while nconfdi < len(cosfun):
        e.append(0.0)
        i = 0
        for k in phipsiname:
            j = 0
            val = parm.get(k[1])
            for value in range(len(val)):
                e[nconfdi] += parm[k[1]][j][0] * cosfun[nconfdi][i][j]
                j += 1
            i += 1
        nconfdi += 1

    return e

def weight(parm_new, parm, phipsi_name, dih_nmr, nmrname):
    """
    Calculate the weight based on RMSD and NMR values.
    """
    e = energy(parm_new, cosfun)
    e0 = energy(parm, cosfun)

    w1 = []
    wa = []
    wb = []
    wp = []
    w0 = []

    invkt = -1.0 / (0.0019872041*300)

    for nconfnmr in range(len(dih_nmr[nmrname[0]])):
        w0.append(math.exp((e0[nconfnmr] - e[nconfnmr]) * invkt))
        wa.append(dih_phipsi_alpha[phipsi_name[0]][nconfnmr] * math.exp((e0[nconfnmr] - e[nconfnmr]) * invkt))
        wb.append(dih_phipsi_beta[phipsi_name[0]][nconfnmr] * math.exp((e0[nconfnmr] - e[nconfnmr]) * invkt))
        wp.append(dih_phipsi_pii[phipsi_name[0]][nconfnmr] * math.exp((e0[nconfnmr] - e[nconfnmr]) * invkt))
        w1.append((abs(dih_nmr[nmrname[0]][nconfnmr]) + abs(dih_nmr[nmrname[1]][nconfnmr])) * math.exp((e0[nconfnmr] - e[nconfnmr]) * invkt))

    return w0, wa, wb, wp, w1

def move(parm_new, kmin, kmax):
    """
    Move the parameters randomly.
    """
    for k in phipsiname:
        val = parm_new.get(k[1])
        for value in range(len(val)):
            for j in range(len(parm_new[k[1]])):
                if j < 3:
                    parm_new[k[1]][j][0] += random.uniform(-0.005, 0.005)
                if j == 3:
                    parm_new[k[1]][j][0] += random.uniform(-0.001, 0.001)
                else:
                    parm_new[k[1]][j][0] += random.uniform(-0.0001, 0.0001)

                if parm_new[k[1]][j][0] > kmax:
                    parm_new[k[1]][j][0] = kmax
                elif parm_new[k[1]][j][0] < kmin:
                    parm_new[k[1]][j][0] = -parm_new[k[1]][j][0]

    return parm_new

def rmsd_parameter(parm_old, parm_new):
    """
    Calculate the RMSD of parameters.
    """
    rmsd_param = 0.0
    cnt = 0

    for k in phipsiname:
        val_old = parm_old.get(k[1])
        val_new = parm_new.get(k[1])
        for value in range(len(val_old)):
            rmsd_param += (parm_old[k[1]][value][0] - parm_new[k[1]][value][0]) ** 2
            cnt += 1

    return math.sqrt(rmsd_param) / cnt

def monte_carlo_reweight(parm, dihedral_charmm, phipsiname, dih_nmr, nmrname, dih_phipsi_alpha, dih_phipsi_beta, dih_phipsi_pii):
    """
    Perform Monte Carlo reweighting.
    """
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
            par.append(move(parm_new, kmin, kmax))
            parmlist.append(par[i])

            if weight(par[i], parm, phipsiname, dih_nmr, nmrname)[4]:
                problist.append(weight(par[i], parm, phipsiname, dih_nmr, nmrname)[0] + 1.0 * abs(weight(par[i], parm, phipsiname, dih_nmr, nmrname)[1] - 0.05) + 1.0 * abs(weight(par[i], parm, phipsiname, dih_nmr, nmrname)[2] - 0.56) + 1.0 * abs(weight(par[i], parm, phipsiname, dih_nmr, nmrname)[3]-0.39))
            else:
                problist.append(99.0)

        ind = problist.index(min(problist))
        prob = problist[ind]

        if qweight == True:
            cutof += 0.00005
            rmsdw = rmsd_parameter(parm, parmlist[ind])
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
                print(f"{istep:6}{prob_best:9.5f}{rmsdw:9.5f}{tar_best:9.5f}")

        istep += 1

    print("=== Best Parameters ===")
    print(parm_best)
    print(f"Probability: {prob_best}")
    print(f"RMSD: {rmsd_best}")
    print(f"Target: {tar_best}")

if __name__ == "__main__":
    # Set the number of steps
    nstep = 10000

    # Set the temperature
    tempr0 = 1.0

    # Set the switch for weighting for NMR
    qweight = True

    # Read dihedral files
    dihedral_charmm, phipsiname = read_dihedral_files()

    # Read parameter file
    parm = read_parameter_file()

    # Read NMR files
    dih_nmr, nmrname = read_nmr_files()

    # Read phi/psi files
    dih_phipsi_alpha, dih_phipsi_beta, dih_phipsi_pii, phipsi_name = read_phi_psi_files()

    # Perform Monte Carlo reweighting
    monte_carlo_reweight(parm, dihedral_charmm, phipsiname, dih_nmr, nmrname, dih_phipsi_alpha, dih_phipsi_beta, dih_phipsi_pii)
