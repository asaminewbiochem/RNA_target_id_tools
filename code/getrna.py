import argparse
import os
import sys

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="""
    This script is going to extract RNA sequence from genome reference based on bed files.
    """)
    parser.add_argument("transcript", help="ENSEMBL transcript id")
    parser.add_argument("gffgz", help="gene model file, e.g. gencode.v36.annotation.gff3.gz file")
    parser.add_argument("genome", help="genome reference fasta file, e.g. GRCh38.primary_assembly.genome.fa ")
    parser.add_argument("-t","--type", default="five_prime_utr",help="model type, e.g. transcript, five_prime_utr, three_prime_utr, exon")
    parser.add_argument("-b","--bedoutput", default=None,help="bedoutput type, outBed, tab etc")
    parser.add_argument("-o","--outfile", default=None,help="output file")
    args = parser.parse_args()

    TRANSCRIPT = args.transcript 
    GFFGZ = args.gffgz
    TYPE = args.type

    GENOME = args.genome
    BEDOUTPUT = args.bedoutput
    OUTFILE = args.outfile


    # grep gff based on transcript id and type
    com_bed = "zgrep %s %s | awk '$3==\"%s\"'" % (TRANSCRIPT, GFFGZ, TYPE)
    # extract RNA seq based on genome ref, bed, and strand info
    com_fa = "bedtools getfasta -fi %s -bed -  -s  -name" % (GENOME) # may result in multi records/exons
    # concat fast a files

    if BEDOUTPUT is not None:
        com_fa = "%s -%s" % (com_fa,BEDOUTPUT)

    if OUTFILE is not None:
        com_fa = "%s > %s" % (com_fa, OUTFILE)

    com = com_bed + " | " + com_fa
    eprint(com)
    os.system(com)
