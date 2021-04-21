def main():
    import sys
    import math
    import getopt

    log = False
    sqrt = False
    inputName = ""

    argv = sys.argv[1:]  # grap all the arguments(everything)

    def Usage():
        print('''
        python getprob.py -i input.txt [-l || -s] >output.probs
        Options:
        -h, --help

        Required:
        -i, --input format base_i base_j prob
        optional
        -l, --log
        -s, --sqrt
        ''')
    if len(argv) == 0:
        Usage()
        sys.exit()

    try:
        opts, args = getopt.getopt(
            argv, "hi:ls", ["help", "input=", "log", "sqrt"])
    except getopt.GetoptError:  # option help input log and sqrt
        Usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            Usage()
            sys.exit()
        elif opt in ("-i", "--input"):
            inputName = arg
        elif opt in ("-l", "--log"):
            log = True
        elif opt in ("-s", "--sqrt"):
            sqrt = True

    if log and sqrt:
        print("probability cannot be in both -log10 and sqrt format")
        Usage()
        sys.exit()
    source = "".join(args)
    if len(args) > 0:
        print("Warning: unused options", source)
    # end of command line option
    infile = open(inputName, 'r')
    allprobs = infile.read().splitlines()
    probs = []
    # size of the sequnce must be given at first line
    size = int(allprobs[0].strip())
    for i in range(0, size):
        probs.append([0]*size)
    for i in range(2, len(alprobs)):
        info = allprobs[i].split()
        base1 = int(info[0])
        base2 = int(info[1])
        prob = float(info[2])
        if log:
            prob = 10**(-1*float(info[2]))
        elif sqrt:
            prob = float(info[2])**2
        probs[base1-1][base2-1] = prob
        probs[base2-1][base1-1] = prob

    for i in range(0, len(probs)):
        downstream = 0.00
        for j in range(0, i):
            downstream += probs[i][j]
        upstream = 0.0
        for j in range(i+1, size):
            upstream += probs[i][j]
        if upstream > 1.0:
            upstream = 1.0
            downstream = 0.0
        elif downstream > 1.0:
            upstream = 0.0
            downstream = 1.0
        none = 1.0-upstream-downstream

        print(str(upstream)+"\t"+str(downstream)+"\t"+str(none))
    infile.close()


main()
