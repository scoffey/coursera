#!/usr/bin/env python2.7

import sys
import random

def karger_min_cut(graph):
    """ Finds a minimum cut on the given graph using Karger's algorithm
        with random contraction of edges. """
    vertices, edges = graph
    while len(vertices) > 2:
        # pick a random edge and remove it
        u, v = edges.pop(random.randrange(len(edges)))
        vertices = [i for i in vertices if i != v] # keep all vertices but v
        new_edges = []
        for tail, head in edges:
            if tail == v: # apply contraction if edge tail is v
                tail = u
            if head == v: # apply contraction if edge head is v
                head = u
            if tail != head: # keep edge if not a loop
                new_edges.append((tail, head))
        edges = new_edges
    # the resulting cut is the of edges from partition A to B (ignoring
    # edges from B to A), which is half of the total number edges
    return len(edges) / 2

def main(program, runs=None, seed=None, *args):
    """ Main program """
    vertices, edges = [], [] # a graph is a tuple of vertices and edges

    for line in sys.stdin:
        row = line.strip().split()
        try:
            adjacency = map(int, row)
            node = adjacency.pop(0) # first element is the node number
            vertices.append(node)
            for neighbor in adjacency:
                edges.append((node, neighbor))
        except ValueError:
            sys.stderr.write('Not a row of integers: %r\n' % row)
            sys.exit(1)

    runs = int(runs) if runs and runs.isdigit() else 1
    if seed and seed.isdigit():
        random.seed(int(seed))

    min_cut = None
    for i in range(runs):
        graph = vertices[:], edges[:] # deep copy
        cut = karger_min_cut(graph)
        print 'found cut with %d crossing edges' % cut
        if min_cut is None or cut < min_cut:
            min_cut = cut
    print 'min cut: %d' % min_cut

if __name__ == '__main__':
    # python mincut.py [runs] [seed] < kargerMinCut.txt
    main(*sys.argv)

