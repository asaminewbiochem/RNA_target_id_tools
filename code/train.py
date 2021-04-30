# datamine.py

import csv
from os import readlink


def read_file(filename, mode='warn'):
    '''read csv file and save data in the list'''
    # check for correct mode
    if mode not in ['warn', 'silent', 'stop']:
        raise ValueError("possible modes are 'warn','silent','stop' ")

    ring_data = []  # create empty list
    with open(filename, 'r') as f:
        rows = csv.reader(f)
        headers = next(rows)  # skip the header

        # change the type of the columns
        for row in rows:
            try:
                row[2] = float(row[2])
                row[3] = float(row[3])
                row[4] = int(row[4])
            except ValueError as err:  # process value error only
                if mode == 'warn':
                    print("Invalid data, row is skipped")
                    print("Row: {}, reason: {}".format(row_num, err))
                elif mode == 'silent':
                    pass  # do nothing
                elif mode == 'stop':
                    raise  # raise the exception
                continue
            # append data in the list in the form of tubple
            ring_data.append(tuple(row))
    return ring_data


def main():
    ring_data = read_file('price.csv')

    # total rows in the file

    print("Total rows: ", len(ring_data))

    # total price calculation
    total_price = 0
    for row in ring_data:
        total_price += row[3]*row[4]
    print("total price: {:10.2f}".format(total_price))


if __name__ == '__main__':
    main()
