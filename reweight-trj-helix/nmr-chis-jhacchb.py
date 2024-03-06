import math,sys
from math import cos,sin,pi, exp


in_file=open(sys.argv[1],"r")
expt=float(sys.argv[2])
for lines in in_file:
        field=lines.split()
        x=float(field[0])
        print 9.50*(cos((x-0.0)*pi/180.0))**2 - 1.60*cos((x-0.0)*pi/180.0) + 1.80 ,expt

