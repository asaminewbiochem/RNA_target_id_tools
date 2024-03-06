import math,sys
from math import cos,sin,pi, exp


in_file=open(sys.argv[1],"r")
expt=float(sys.argv[2])
for lines in in_file:
        field=lines.split()
        x=float(field[0])
        print 6.51*(cos((x-60.0)*pi/180.0))**2 - 1.76*cos((x-60.0)*pi/180.0) + 1.60 ,expt

