import sys
from math import pi
import pdb

if len(sys.argv) != 3:
    raise SystemExit("Usage :debuge_ex.py \"metal\"radius")
# sys.argv[0] is the python file name

print("Entered values: ", sys.argv)
pdb.set_trace()
metal = sys.argv[1]

# radius=10

radius = float(sys.argv[2])
perimeter = 2*radius
area = pi*radius**2

print("metal ", metal)
print("perimeter =", perimeter)

print("area =", area)
