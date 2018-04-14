#!/usr/bin/env python2.7

import itertools
import math
import sys

def tsp(cities):
    """ Computes the minimum cost tour across all the given cities, using the
        Bellman-Held-Karp algorithm for the traveling salesman problem """

    n = len(cities)
    distances = get_distances(cities)

    a = [dict() for i in xrange(n)] # solutions cache
    s = path_hash({0})
    a[0][s] = 0 # base case for the first city

    for m in xrange(1, n):
        # all possible paths of length m + 1 that include the first city
        paths = [frozenset((0,) + i) for i in \
            itertools.combinations(xrange(1, n), m)]
        print 'Testing %d paths of length %d...' % (len(paths), m + 1)
        for path in paths:
            s = path_hash(path)
            for j in path:
                if j != 0: # avoid closing a cycle back to the first city
                    for k in path: # extend shorter paths from 0 to k with j
                        if k != j: # avoid visiting j more than once
                            t = path_hash(path - {j})
                            if t in a[k]: # else consider the cost infinite
                                cost = a[k][t] + distances[k][j]
                                if s not in a[j] or a[j][s] > cost:
                                    a[j][s] = cost

    # find the min cost of closing a cycle back to the first city
    s = path_hash(xrange(n)) # path that visits all the cities
    return min(a[j][s] + distances[0][j] for j in xrange(1, n) if s in a[j])

def get_distances(cities):
    """ Returns the Euclidean distances between every pair of cities """
    n = len(cities)
    distances = [[None] * n for i in xrange(n)]
    for i in xrange(n):
        for j in xrange(n):
            x1, y1 = cities[i]
            x2, y2 = cities[j]
            dx = x2 - x1
            dy = y2 - y1
            d = math.sqrt(dx * dx + dy * dy)
            distances[i][j] = d
            distances[j][i] = d
    return distances

def path_hash(path):
    """ Calculates a hash for a set of small integers """
    s = 0
    for i in path:
        s |= 1 << i
    return s

def parse_coords(stream):
    """ Parses the number of cities in the first line and the coordinates
        (x, y) of each city in the rest of the lines """

    n = None
    cities = []

    for line in stream:
        s = line.strip()

        if n is None:
            n = int(s)
        else:
            x, y = map(float, s.split())
            cities.append((x, y))

    return cities

def main(program, *args):
    """ Main program """
    print 'Parsing city coordinates...'
    cities = parse_coords(sys.stdin)
    n = len(cities)
    print 'Computing the minimum cost tour across %d cities...' % n
    cost = tsp(cities)
    print 'The minimum cost of the tour across %d cities is: %r' % (n, cost)

# usage: python tsp.py < tsp.txt
if __name__ == '__main__':
    main(*sys.argv)

