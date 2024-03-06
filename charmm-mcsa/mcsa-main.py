#!/usr/bin/env python3
"""
Monte Carlo reweight dihedral force constant
Author: Asaminew Haile Aytenfisu (2017)
Updated for Python 3 compatibility and improved practices.
"""

import math
import random
import sys
import copy
import os
from datetime import datetime
from subprocess import call

# Assuming mcsa_module is updated for Python 3 as well
from mcsa_module import *

def main():
    start_time = datetime.now()

    if len(sys.argv) < 5:
        print("Usage: script.py <run> <thread> <jobid> <f>")
        sys.exit(1)

    run = int(sys.argv[1])
    jobid = int(sys.argv[3])
    thread = int(sys.argv[2])
    f = str(sys.argv[4])
    now = datetime.now()
    tempr0 = 50.0
    nstep = 3
    mm = 1
    qm = 1

    print("""
    Monte Carlo reweight dihedral fitting
    Reweight using NMR as a target function
    """)

    ndih = int(input("Number of path for phi? ").strip())
    print(f"number of paths for phi is {ndih}")

    read_dihedral_index(ndih)

    parm = parmread('/tmp/ahaile/auto/parm.parm', {})

    dih_qm = mm_qm_read([], qm, f"{f}.qm")

    tar_best = tar_old = dtar = tar_new = 99.0
    istep = 0
    parm_best = []
    parm_old = copy.deepcopy(parm)

    while istep < nstep:
        parm_new = copy.deepcopy(parm_old)
        parmlist = []
        par = []
        problist = []

        for i in range(thread):
            par.append(param_update(parm_new, parm_old, kmin, kmax))
            parmlist.append(par[i])
            param2print(par[i], f"tmp.{jobid}.{f}.{run}.{i}.{istep}.str")

        # Replacing os.system with call from subprocess for better practice
        call(["bash", f"./charmm.{jobid}.sh", str(run), str(thread - 1), str(jobid), str(istep)])

        for i in range(thread):
            problist.append(RMSE(dih_qm, qm, mm, i, istep, jobid, f, run))

        ind = problist.index(min(problist))
        prob = problist[ind]

        # Best parameter file naming corrected for consistency
        best_file_name = f"best.{f}.{run}.{ind}.{istep}.str"
        call(["grep", "OD30D", f"tmp.{jobid}.{f}.{run}.{ind}.{istep}.str", ">", best_file_name])

        tempr = tempr0 * math.exp(-1.0 * (float(istep) / (float(nstep) / 4.0)))
        tar_new = prob
        dtar = tar_new - tar_old

        if istep == 0:
            p = 0.0
        else:
            boltz = -dtar / (0.001987 * tempr)
            p = math.exp(boltz)

        prnd = random.uniform(0.0, 1.0)

        accepted = dtar < 0.0 or prnd < p

        if accepted:
            tar_old = tar_new
            parm_old = parmread(best_file_name, parm)

            if tar_new < tar_best:
                tar_best = tar_new
                parm_best = copy.deepcopy(parm_old)

        if istep % 1 == 0:
            print(f"{istep:6}{tempr:7.1f}{p:8.3f}{int(accepted):6}{tar_new:9.5f}{tar_best:9.5f}")

        istep += 1

    param2print(parm_best, f"optimized.{f}.{run}.str", probab=tar_best)

    end_time = datetime.now()
    print(f"Execution Time: {end_time - start_time}")

if __name__ == "__main__":
    main()
