#!/usr/bin/env python2.7
  
import sys

def knapsack(values, weights, size):
    """ Returns the optimal total value of items that fit their total weight
        in the given knapsack size """
    n = len(values)
    s = [0] * (size + 1) # current optimal solutions for each residual capacity
    for i in xrange(n):
        prev_s = tuple(s) # previous solutions (with 1 less item)
        for x in xrange(size + 1):
            s[x] = prev_s[x] # case 1: i-th item not included
            j = x - weights[i]
            if j >= 0: # if the i-th item fits into the knapsack size
                v = prev_s[j] + values[i]
                if v > prev_s[x]:
                    s[x] = v # case 2: i-th item is included
    return s[-1] # optimal total value considering all items

def main(program, *args):
    """ Main program """
    size = None
    values = []
    weights = []

    # parse value and weight pairs on every line
    for line in sys.stdin:
        s = line.strip()
        try:
            row = map(int, s.split())
        except Exception:
            sys.stderr.write('Not a row of integers: %s\n' % s)
            sys.exit(1)

        if size is None:
            size, n = row
            print 'Parsing %d pairs of value and weight...' % n
        else:
            v, w = row
            values.append(v)
            weights.append(w)

    print 'Calculating optimal total value for knapsack size of %d...' % size
    print knapsack(values, weights, size)

# usage: python knapsack.py < knapsack1.txt
if __name__ == '__main__':
    main(*sys.argv)

