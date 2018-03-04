#!/usr/bin/env python2.7

import heapq
import sys

def add_edge(graph, cost_lookup, u, v, cost):
    """ Adds an edge from u to v with the given cost to the graph """
    if u not in graph:
        graph[u] = []
    graph[u].append(v)
    cost_lookup[(u, v)] = cost

def prim_mst(graph, cost_lookup, start=1):
    """ Finds a minimum spanning tree on the graph using Prim's algorithm """
    mst = []
    heap = []
    for v in graph[start]:
        edge = (start, v)
        heapq.heappush(heap, (cost_lookup[edge], edge))

    visited = set([start])
    while len(visited) < len(graph):
        cost, edge = heapq.heappop(heap) # find cheapest edge on heap
        u, v = edge
        if v not in visited:
            visited.add(v)
            mst.append(edge) # add v to the tree
            # update heap with edges of the new cut
            for neighbor in graph[v]:
                if neighbor not in visited:
                    new_edge = (v, neighbor)
                    heapq.heappush(heap, (cost_lookup[new_edge], new_edge))

    return mst

def main(program, *args):
    """ Main program """
    graph = {}
    cost_lookup = {}

    # parse edge (vertex, vertex, cost) on every line
    for line in sys.stdin:
        s = line.strip()
        try:
            row = map(int, s.split())
        except Exception:
            sys.stderr.write('Not a row of integers: %s\n' % s)
            sys.exit(1)

        if len(row) == 2:
            print 'Calculating MST of %d vertices and %d edges...' % tuple(row)
        else:
            u, v, cost = row
            add_edge(graph, cost_lookup, u, v, cost)
            add_edge(graph, cost_lookup, v, u, cost)

    # find minimum spanning tree and print the total cost of its edges
    mst = prim_mst(graph, cost_lookup)
    cost = sum(cost_lookup[edge] for edge in mst)
    print 'Total cost of the edges of the MST: %d' % cost

# usage: python prim.py < edges.txt
if __name__ == '__main__':
    main(*sys.argv)

