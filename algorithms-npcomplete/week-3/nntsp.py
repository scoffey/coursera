#!/usr/bin/env python2.7

import math
import sys

def nearest_neighbor_tsp(cities):
    """ Computes an approximate minimum cost tour across all the given cities,
        using the nearest neighbor heuristic """

    n = len(cities)
    distances = get_distances(cities)

    cost = 0 # traveling cost so far
    path = [None] * n # tour path across all cities
    path[0] = 0
    visited = [False] * n # cache of visited cities
    visited[0] = True

    # repeatedly visit the closest city that hasn't been visited yet
    # (and break ties by lowest city index)
    for i in xrange(1, n):
        u = path[i - 1]
        d, v = min((d, v) for v, d in enumerate(distances[u]) if not visited[v])
        cost += d
        path[i] = v
        visited[v] = True

    return cost + distances[path[-1]][0]

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

def parse_coords(stream):
    """ Parses the number of cities in the first line and the index and
        coordinates (x, y) of each city in the rest of the lines """

    n = None
    cities = []

    for line in stream:
        if n is None:
            n = int(line.strip())
            cities = [None] * n
        else:
            i, x, y = line.strip().split()
            cities[int(i) - 1] = (float(x), float(y))

    return cities

def main(program, *args):
    """ Main program """
    print 'Parsing city coordinates...'
    cities = parse_coords(sys.stdin)
    n = len(cities)
    print 'Computing an approximate minimum cost tour across %d cities...' % n
    cost = nearest_neighbor_tsp(cities)
    print cost

# usage: python nntsp.py < nn.txt
if __name__ == '__main__':
    main(*sys.argv)

