from math import fsum
# outFile = open("/Users/ahaile/result.txt", "w")
# keepCurrentSet = False
# vs = []
inFile = open("/Users/ahaile/rts-v5.pdb")
# atom = ""
cnt = 0
for line in open("/Users/ahaile/rts-v5.pdb"):
    if line.split()[0] == "ATOM":
        # atom = atom + "\n" + line.strip("\n")
        cnt += 1
natom = int(cnt/10)
print(natom)
# print(atom)
vs = []
# s=[]


for i in range(1, 10*(natom+3), natom+3):
    # print(i)
    s = []

    c = 0
    inFile = open("/Users/ahaile/rts-v5.pdb")
    for line in inFile:

        if (i < c) and (c <= i+natom):

            s.append(float(line.split()[9]))
        c += 1

    vs.append(fsum(s))
print(vs)
# print("\n\n\n")
