import argparse
import os

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="""
    This script is going to split the bed file after intersecting a fasta bedfile and a shape bedgraph file.  The output is two files.
    One is in fasta format and the other is in shape format.
    """)
    parser.add_argument("bed", help="bed file, e.g. chr12	6534558	6534559	T	+	chr12	6534558	6534559	0.313")
    parser.add_argument("-f","--fo",default="rna.fa",help="output file name for fasta file")
    parser.add_argument("-s","--so",default="rna.shape",help="output file name for shape file")
    args = parser.parse_args()

    BED = args.bed
    FASTA = args.fo
    SHAPE = args.so

    seq = []
    shape = []

    with open(BED) as f:
        for line in f:
            L = line.strip().split()
            if L[3] == "T": 
                seq.append("U")
            else:
                seq.append(L[3])
            shape.append(L[8])

    seq = "".join(seq)
    seq_out = ">seq\n%s" % (seq)
    with open(FASTA,"w") as ff:
        ff.write(seq_out)

    i = 1
    with open(SHAPE,"w") as sf:
        for score in shape:
            if score == '.' :
                out = "%s\t%s" % (i,-999)
                sf.write("%s\n" % out)
            else:
                out = "%s\t%s" % (i,score)
                sf.write("%s\n" % out)
            i +=1
