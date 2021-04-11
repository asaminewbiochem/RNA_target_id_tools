import argparse
import os
import operator

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="""
    This script is going to split bed file into one base per row
    """)
    parser.add_argument("bed", help="bed file, column 10 is the sequence")
    args = parser.parse_args()

    BED = args.bed

    bedout = []

    with open(BED) as f:
        for line in f:
            L = line.strip().split()
            start = int(L[3])
            end = int(L[4])
            strand = L[6]
            if strand == '-':
                pos = end
            else:
                pos = start
            bps = list(L[9])
            for bp in bps:
                out = "%s\t%s\t%s\t%s\t%s" % (L[0],pos-1,pos,bp,strand) #minus 1 to make it bed format: start is 0 based
                bedout.append([L[0],pos-1,pos,bp,strand])
                if strand == '-':
                    pos -= 1
                else:
                    pos += 1
#                print(out)

    strand = bedout[0][4]
    if strand == '+':
        bedout = sorted(bedout,key=operator.itemgetter(1))
    else:
        bedout = sorted(bedout,key=operator.itemgetter(1),reverse=True)

    for l in bedout:
        print(*l,sep="\t")
        #print("\t".join(l))
