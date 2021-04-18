import argparse


def mulNum(a):
    p = 1
    for item in a:
        p *= item
    return p


parser = argparse.ArgumentParser(description="First argparse code")


parser.add_argument(
    type=int,  # type int
    nargs='+',  # read multiple values in a list
    dest='integers',  # name of the attribute returned by argaprse
    help='read list of integer: 1 2 3')


parser.add_argument(
    '-p', '--product',  # name -p or --product
    dest='multiply',  # by default dest=product
    action='store_const',  # store values
    const=mulNum,  # call function 'mulNum'
    help='product of integers')


parser.add_argument('--sum', dest='accumulate',
                    action='store_const', const=sum, help='sum of integers')

args = parser.parse_args()
# if --sum is in command
if args.accumulate:
    sum = args.accumulate(args.integers)
    print('sum = ', sum)ß

# if p=-p or --product is in command
if args.multiply != None:
    product = args.multiply(args.integers)
    print('product = ', product)
