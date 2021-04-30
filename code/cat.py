# cat.py

import argparse

parser = argparse.ArgumentParser(description="Cat files")

# read arguments

parser.add_argument(nargs="+", dest='files', help='unix cat opera')
parser.add_argument('-n', '--numbers', action='store_true',
                    help='print line numbers')

args = parser.parse_args()  # save argumnets here


line_no = 0  # create
for file_name in args.files:
    with open(file_name, 'r') as w:
        if args.numbers:
            for data in w.readlines():
                line_no += 1
                print("{0:5d}\t{1}".format(line_no, data), end='')
        else:
            data = w.read()
            print(data)
