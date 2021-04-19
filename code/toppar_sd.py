#! /usr/bin/python
import argparse
import os
import sys
from math import sqrt


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
        vs = []
        vt = []
        for index in range(1, 10, 1):
            s = 0
            t = 0
            pdb = open(pdbid+'.'+str(index)+'.pdb', 'r')
            for p in pdb.readlines():
                if p.startswith('ATOM'):
                    t += float(p.split()[9])
                    for i in range(2, len(line), 1):
                        if p.split()[1] == line[i]:
                            s += float(p.split()[9])
            vs.append(s)
            vt.append(t)
        sd = 0.0
        avg = 0.0
        for value in vs:
            avg += value
        avgs = avg/len(vs)

        for value in vs:
            sd += (value-avgs)**2
        sds = sqrt(sd/len(vs))

        sd = 0.0
        avg = 0.0
        for value in vt:
            avg += value
        avgt = avg/len(vs)

        for value in vt:
            sd += (value-avgt)**2
        sdt = sqrt(sd/len(vt))

        pymol = ("com " + pdbid+'.'+str(index) + " and (")
        for k in range(3, len(line), 1):

            if k != (len(line)-1):
                pymol = pymol + " id " + str(line[k])+" or "
            else:
                pymol = pymol + " id " + str(line[k])+")"

        f.write(pymol+" , object="+pdbid+"."+ring+"\n")
        f.write("%s %1s %s %1s %1s%5.1f %4s %5.1f %1s \n" %
                ("label", " ", pdbid+"."+ring, ",", '"', avgs, "±", sds, '"'))
        f.write("hide everything, " + pdbid+"."+ring+"\n")
        f.write("show label , " + pdbid+"."+ring+"\n")
        f.write("com  "+pdbid+"."+str(index)+",object="+pdbid+".T\n")
        f.write("%s %1s %s %1s %1s%5.1f %4s %5.1f %1s \n" %
                ("label", " ", pdbid+".T", ",", '"', avgt, "±", sdt, '"'))
        f.write("hide everything , " + pdbid+".T\n")
        f.write("show label , " + pdbid+".T\n")
        f.write("set label_size,30 , " + pdbid+".T\n")
        f.write("set label_color,magenta , " + pdbid+".T\n")
