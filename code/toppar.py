#! /usr/bin/python
import argparse
import os
import sys


# def eprint(*args, **kwargs):
#     print(*args, file=sys.stderr, **kwargs)


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
        for index in range(1, 2, 1):
            s = 0
            t = 0
            pdb = open(pdbid+'.'+str(index)+'.pdb', 'r')
            for p in pdb.readlines():
                if p.startswith('ATOM'):
                    t += float(p.split()[9])
                    # print(len(line))
                    for i in range(2, len(line), 1):
                        # print(i)
                        if p.split()[1] == line[i]:
                            s += float(p.split()[9])
            pymol = ("com " + pdbid+'.'+str(index) + " and (")
            for k in range(3, len(line), 1):
                # print(k, len(line))
                if k != (len(line)-1):
                    pymol = pymol + " id " + str(line[k])+" or "
                else:
                    pymol = pymol + " id " + str(line[k])+")"

            f.write(pymol+" , object="+pdbid+"."+ring+"\n")
            # f.write("\n")
            f.write("%s %1s %s %1s %1s%5.1f %1s \n" %
                    ("label", " ", pdbid+"."+ring, ",", '"', s, '"'))
            f.write("hide everything, " + pdbid+"."+ring+"\n")
            f.write("show label , " + pdbid+"."+ring+"\n")
            f.write("com  "+pdbid+"."+str(index)+",object="+pdbid+".T\n")
            f.write("%s %1s %s %1s %1s%5.1f %1s \n" %
                    ("label", " ", pdbid+".T", ",", '"', t, '"'))
            f.write("hide everything , " + pdbid+".T\n")
            f.write("show label , " + pdbid+".T\n")
            f.write("set label_size,30 , " + pdbid+".T\n")
            f.write("set label_color,magenta , " + pdbid+".T\n")
            # eprint(com)
            # os.system(com)
