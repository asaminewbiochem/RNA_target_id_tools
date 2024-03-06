#!/usr/bin/python
"""
Script: 2D_generate_histogram.py
Author: Asaminew Aytenfisu
Description: This script generates a histogram from data points.
"""

import argparse
import sys
import math
import numpy as np

def read_angles(line):
    tokens = line.split()
    x = float(tokens[0])
    y = float(tokens[1])
    return [x, y]

def main(args):
    try:
        data_file = args.data_file
        histogram_file = args.histogram_file
        x_min = args.x_min
        x_max = args.x_max
        y_min = args.y_min
        y_max = args.y_max
        x_resolution = args.x_resolution
        y_resolution = args.y_resolution 

        points = [read_angles(line) for line in open(data_file)]
        count = len(points)
        histogram = np.zeros([x_resolution, y_resolution])
        x_interval_length = (x_max - x_min) / x_resolution
        y_interval_length = (y_max - y_min) / y_resolution
        interval_surface = x_interval_length * y_interval_length
        increment =  count / interval_surface

        for i in points:
            x = int((i[0] - x_min) / x_interval_length)
            y = int((i[1] - y_min) / y_interval_length)
            histogram[x,y] += increment

        x_intervals = np.arange(x_min, x_max, (x_max - x_min) / x_resolution)
        y_intervals = np.arange(y_min, y_max, (y_max - y_min) / y_resolution)

        with open(histogram_file, 'w') as o:
            for i, x in enumerate(x_intervals):
                for j, y in enumerate(y_intervals):
                    if histogram[i,j] != 0.0:
                        o.write('%f %f %f \n' % (x, y,  -0.001982923700*298.0*math.log(histogram[i,j]/histogram.max())))
                    else:
                        o.write('%f %f %f \n' % (x, y,  99999.0))
                o.write('\n')

    except Exception as e:
        print("Error:", e)
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a histogram from data points")
    parser.add_argument("data_file", help="input data file")
    parser.add_argument("histogram_file", help="output histogram file")
    parser.add_argument("x_min", type=float, help="minimum x value")
    parser.add_argument("x_max", type=float, help="maximum x value")
    parser.add_argument("y_min", type=float, help="minimum y value")
    parser.add_argument("y_max", type=float, help="maximum y value")
    parser.add_argument("x_resolution", type=int, help="x resolution")
    parser.add_argument("y_resolution", type=int, help="y resolution")
    args = parser.parse_args()
    main(args)
