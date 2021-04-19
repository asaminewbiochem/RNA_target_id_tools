import argparse
import sys
import os
from pathlib import Path


parser = argparse.ArgumentParser(description='Concating files')
parser.add_argument("--infile", default='a.inp', help='input files name')
parser.add_argument("--outfile", default='a.out', help='output filea')
args = parser.parse_args()

outfiles = open("hbond-data/"+args.outfile, 'w')
for i in range(0, 900, 50):
    if Path("tmp/"+args.infil+"."+str(i) + ".dat").is_file():
        with open("tmp/"+args.infil+"."+str(i)+".dat", 'r') as f:
            for line in f:
                line = line.strip("\n")
                outfiles.write(line)
                outfiles.write('\n')
outfiles.close()
