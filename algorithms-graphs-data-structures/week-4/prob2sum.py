#!/usr/bin/env python2.7

import sys

def find_2sum(dataset, t):
    """ Returns 2 values of the dataset whose sum is t, or None if not found """
    for x in dataset:
        y = t - x # find y such that x + y = t
        if y != x and y in dataset:
            return (x, y)
    return None

def main(program, tmin=-10000, tmax=10000, *args):
    """ Main program """
    dataset = set()

    # parse an integer on every line
    for line in sys.stdin:
        s = line.strip()
        try:
            dataset.add(int(s))
        except ValueError:
            sys.stderr.write('Not an integer: %s\n' % s)
            sys.exit(1)

    # count how many target values in the range [tmin, tmax] are the sum of
    # 2 distinct values belonging to the input dataset
    count = 0
    tmin = int(tmin)
    tmax = int(tmax)
    for t in xrange(tmin, tmax + 1):
        result = find_2sum(dataset, t)
        if result is not None:
            count += 1
            print '%d = %d + %d' % (t, result[0], result[1])

    print 'number of target values in range [%d, %d] that are the sum of ' \
            '2 distinct values in the dataset: %d' % (tmin, tmax, count)

# usage: python prob2sum.py [tmin] [tmax] < prob-2sum.txt
if __name__ == '__main__':
    main(*sys.argv)

