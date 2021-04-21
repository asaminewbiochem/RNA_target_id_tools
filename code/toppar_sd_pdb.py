#! /usr/bin/python
import argparse
import os
import sys
from math import sqrt, fsum


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="""This script converts LGFE""")
    parser.add_argument(
        "-l", "--listname", help="file containing lists of atom id in mol2")
    parser.add_argument("-o", "--output", help="name of output")
    args = parser.parse_args()

    LISTNAME = args.listname
    OUTPUTNAME = args.output

    lst = open(LISTNAME, 'r')
    f = open(OUTPUTNAME, 'w')

    for line in lst.readlines():
        line = line.split()
        pdbid = line[0]
        ring = line[1]
        cnt = 0

        for l in open(pdbid+'.pdb', 'r'):
            if l.split()[0] == "ATOM":
                cnt += 1
        natom = int(cnt/10)

        vt = []
        vs = []
        if ring != "T":
            for index in range(1, 10*(natom+3), natom+3):
                s = 0
                c = 0
                pdb = open("/Users/ahaile/"+pdbid+'.pdb', 'r')
                for p in pdb:
                    if (index < c) and (c <= index+natom):
                        for d in range(2, len(line), 1):
                            if p.split()[1] == line[d]:
                                s += float(p.split()[9])
                    c += 1
                vs.append(s)
            std = 0.0
            avgs = sum(vs)/len(vs)
            for value in vs:
                std += (value-avgs)**2
            stds = sqrt(std/len(vs))

            pymol = ("com " + pdbid+'.'+str(1) + " and (")
            for k in range(3, len(line), 1):

                if k != (len(line)-1):
                    pymol = pymol + " id " + str(line[k])+" or "
                else:
                    pymol = pymol + " id " + str(line[k])+")"

            f.write(pymol+" , object="+pdbid+"."+ring+"\n")
            f.write("%s %1s %s %1s %1s%5.1f %4s %5.1f %1s \n" %
                    ("label", " ", pdbid+"."+ring, ",", '"', avgs, "±", stds, '"'))
            f.write("hide everything, " + pdbid+"."+ring+"\n")
            f.write("show label , " + pdbid+"."+ring+"\n")

        elif ring == "T":
            for index in range(1, 10*(natom+3), natom+3):
                t = 0
                c = 0
                pdb = open("/Users/ahaile/"+pdbid+'.pdb', 'r')
                for p in pdb:
                    if (index < c) and (c <= index+natom):
                        t += float(p.split()[9])
                    c += 1
                vt.append(t)
            std = 0.0
            avgt = sum(vt)/len(vt)
            for value in vt:
                std += (value-avgt)**2
            stdt = sqrt(std/len(vt))

            f.write("com  "+pdbid+"."+str(1)+",object="+pdbid+".T\n")
            f.write("%s %1s %s %1s %1s%5.2f %4s %5.2f %1s \n" %
                    ("label", " ", pdbid+".T", ",", '"', avgt, "±", stdt, '"'))
            f.write("hide everything , " + pdbid+".T\n")
            f.write("show label , " + pdbid+".T\n")
            f.write("set label_size,30 , " + pdbid+".T\n")
            f.write("set label_color,magenta , " + pdbid+".T\n")
