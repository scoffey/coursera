#!/usr/bin/env python2.7
  
import sys

def get_max_weight_independent_set(weights):
    """ Finds the max-weight independent set of a path graph, with the given
        vertex weights, using dynamic programming """

    n = len(weights)
    a = [None] * (n + 1) # memoization table
    a[0] = 0
    a[1] = weights[0]
    for i in xrange(2, n + 1):
        a[i] = max(a[i - 1], a[i - 2] + weights[i - 1])

    mwis = set()
    i = n
    while i > 0:
        if a[i - 1] >= a[i - 2] + weights[i - 1]:
            i -= 1
        else: # vertex belongs to mwis
            mwis.add(i) # use 1-based indexing for vertices
            i -= 2

    return mwis

def main(program, *args):
    """ Main program """
    count = None
    weights = []
    targets = []

    # parse vertex weights on every line
    for line in sys.stdin:
        s = line.strip()
        try:
            w = int(s)
        except ValueError:
            sys.stderr.write('Not an integer: %s\n' % s)
            sys.exit(1)

        if count is None:
            count = w
            print 'Parsing %d vertex weights...' % count
        else:
            weights.append(w)

    # parse arguments as the target vertices to search on the resulting set
    for i in args:
        try:
            targets.append(int(i))
        except ValueError:
            sys.stderr.write('Argument is not an integer: %s\n' % i)
            sys.exit(1)

    # find the max-weight independent set and search for the target vertices
    mwis = get_max_weight_independent_set(weights)
    print ''.join('1' if i in mwis else '0' for i in targets)

# usage: python mwis.py [targets...] < mwis.txt
if __name__ == '__main__':
    main(*sys.argv)

