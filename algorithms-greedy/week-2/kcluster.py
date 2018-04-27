#!/usr/bin/env python2.7

import heapq
import sys

def add_edge(leaders, edges, u, v, cost):
    """ Adds an edge from u to v with the given cost to the graph """
    leaders[u] = u
    leaders[v] = v
    heapq.heappush(edges, (cost, u, v))

def k_cluster(leaders, edges, k):
    """ Groups the given nodes into k clusters by distance
        (each node being their own cluster leader initially) """
    clusters = dict((i, [i]) for i in leaders.iterkeys())
    while len(clusters) > k:
        cost, u, v = heapq.heappop(edges) # find edge of min distance
        c1, c2 = leaders[u], leaders[v]
        # if nodes are in different clusters, merge smaller to larger
        if c1 != c2:
            if len(clusters[c1]) > len(clusters[c2]):
                merge_clusters(clusters, leaders, c2, c1)
            else:
                merge_clusters(clusters, leaders, c1, c2)
    return clusters

def merge_clusters(clusters, leaders, c1, c2):
    """ Merges the cluster c1 to c2 """
    reassigned_nodes = clusters.pop(c1)
    clusters[c2].extend(reassigned_nodes)
    for v in reassigned_nodes:
        leaders[v] = c2

def get_cluster_spacing(clusters, leaders, edges):
    """ Returns the minimum distance between clusters """
    # the first edge between different clusters in the heap is the minimum
    # distance between separated nodes
    while edges:
        cost, u, v = heapq.heappop(edges)
        c1, c2 = leaders[u], leaders[v]
        if c1 != c2:
            return cost
    return None

def main(program, k='4', *args):
    """ Main program """
    k = int(k)
    leaders = {}
    edges = []

    # parse edge (vertex, vertex, cost) on every line
    for line in sys.stdin:
        s = line.strip()
        try:
            row = map(int, s.split())
        except Exception:
            sys.stderr.write('Not a row of integers: %s\n' % s)
            sys.exit(1)

        if len(row) == 1:
            print 'Calculating %d-clustering of %d vertices...' % (k, row[0])
        else:
            add_edge(leaders, edges, *row)

    # group nodes into k clusters by distance and find the spacing between them
    clusters = k_cluster(leaders, edges, k)
    spacing = get_cluster_spacing(clusters, leaders, edges)
    print 'Spacing of %d-clustering: %r' % (k, spacing)

# usage: python kcluster.py [k] < clustering1.txt
if __name__ == '__main__':
    main(*sys.argv)

