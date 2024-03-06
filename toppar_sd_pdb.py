#! /usr/bin/python

"""
Script: pymol_command_line_input_write.py
Author: Asaminew Aytenfisu
Description: This script write pymol command line based on mol2 atom list.
"""

import argparse
import os

def calculate_std(values):
    mean = sum(values) / len(values)
    variance = sum((value - mean) ** 2 for value in values) / len(values)
    return variance ** 0.5

def process_file(listname, outputname):
    with open(listname, 'r') as lst, open(outputname, 'w') as f:
        for line in lst:
            pdbid, ring, *atom_ids = line.split()
            cnt = 0

            if os.path.isfile(f"{pdbid}.pdb"):
                with open(f"{pdbid}.pdb", 'r') as pdb:
                    for l in pdb:
                        if l.startswith("ATOM"):
                            cnt += 1
                natom = cnt // 10

                if ring != "T":
                    vs = []
                    for index in range(1, 10 * (natom + 3), natom + 3):
                        s = sum(float(p[61:67]) for p in pdb if index < c <= index + natom for c, _ in enumerate(pdb, 1))
                        vs.append(s)
                    stds = calculate_std(vs)
                    pymol = f"com {pdbid}.1 and ("
                    for atom_id in atom_ids:
                        pymol += f" id {atom_id} or"
                    pymol = pymol[:-3] + ")"
                    f.write(f"{pymol}, object={pdbid}.{ring}\n")
                    f.write(f'label "{pdbid}.{ring}" , "{sum(vs) / len(vs):.1f} ± {stds:.1f}"\n')
                    f.write(f"hide everything, {pdbid}.{ring}\n")
                    f.write(f"show label , {pdbid}.{ring}\n")
                else:
                    vt = []
                    for index in range(1, 10 * (natom + 3), natom + 3):
                        t = sum(float(p[61:67]) for p in pdb if index < c <= index + natom for c, _ in enumerate(pdb, 1))
                        vt.append(t)
                    stdt = calculate_std(vt)
                    f.write(f"com {pdbid}.1, object={pdbid}.T\n")
                    f.write(f'label "{pdbid}.T" , "{sum(vt) / len(vt):.2f} ± {stdt:.2f}"\n')
                    f.write(f"hide everything , {pdbid}.T\n")
                    f.write(f"show label , {pdbid}.T\n")
                    f.write(f"set label_size,30 , {pdbid}.T\n")
                    f.write(f"set label_color,magenta , {pdbid}.T\n")
            else:
                continue

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="This script write pymol command line input")
    parser.add_argument("-l", "--listname", help="file containing lists of atom id in mol2", required=True)
    parser.add_argument("-o", "--output", help="name of output", required=True)
    args = parser.parse_args()
    process_file(args.listname, args.output)
