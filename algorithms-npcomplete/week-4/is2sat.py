#!/usr/bin/env python2.7

import sys

def kosaraju(graph, graph_rev):
    """ Implements the Kosaraju algorithm for finding the strongly connected
        components of a directed graph """
    leaders = {} # dict of vertex number to SCC leader number
    finishing_times = {}
    dfs_loop(graph_rev, leaders, finishing_times)
    dfs_loop(reorder(graph, finishing_times), leaders, finishing_times)
    return leaders

def reorder(graph, finishing_times):
    g = {} # copy of graph that swaps vertices with their finishing times
    for v, edge_tails in graph.iteritems():
        g[finishing_times[v]] = [finishing_times[i] for i in edge_tails]
    return g

def dfs_loop(graph, leaders, finishing_times):
    explored = {} # dict that contains only explored vertices
    t = 0 # current finishing time
    a, b = min(graph.iterkeys()), max(graph.iterkeys())
    for v in xrange(b, a - 1, -1):
        if v not in explored:
            t = dfs(graph, v, v, explored, leaders, finishing_times, t)

def dfs(graph, v, source, explored, leaders, finishing_times, t):
    explored[v] = True # mark vertex as explored
    leaders[v] = source # the SCC leader is the source vertex
    for u in graph.get(v, []):
        if u not in explored:
            t = dfs(graph, u, source, explored, leaders, finishing_times, t)
    t += 1
    finishing_times[v] = t
    return t

def add_edge(graph, u, v):
    if u not in graph:
        graph[u] = set()
    graph[u].add(v)

def is2sat(n, graph, graph_rev):
    """ Finds strongly connected components in the implication graph
        to determine if the original clauses are 2-satisfiable """
    leaders = kosaraju(graph, graph_rev)
    for i in xrange(1, n + 1):
        u = leaders.get(i, i)
        v = leaders.get(-i, -i)
        if u == v:
            return False
    return True

def parse_conjunction_pairs(stream):
    """ Parses the number of conjunction pairs the first line and the
        indexes of the Boolean operands in the rest of the lines, as
        negated if negative, and builds the implication graph and its
        reverse for finding strongly connected components """

    n = None # number of conjunction pairs
    graph = {} # dict of vertex number to list of tail vertex numbers
    graph_rev = {} # same graph but with directed edges reversed

    for line in stream:
        if n is None:
            n = int(line.strip())
        else:
            u, v = map(int, line.strip().split())
            # when u OR v, add edges from NOT u to v and NOT v to u
            add_edge(graph, -u, v)
            add_edge(graph, -v, u)
            add_edge(graph_rev, v, -u)
            add_edge(graph_rev, u, -v)

    return n, graph, graph_rev

def main(program, *args):
    """ Main program """
    print 'Parsing conjunction pairs to be satisfied...'
    n, graph, graph_rev = parse_conjunction_pairs(sys.stdin)
    print 'Computing if the conjunction pairs are satisfiable...'
    print is2sat(n, graph, graph_rev)

# usage: python is2sat.py < 2sat1.txt
if __name__ == '__main__':
    main(*sys.argv)

