#!/usr/bin/env python2.7

import sys
import resource

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
        graph[u] = [v]
    else:
        graph[u].append(v)

def increase_recursion_limit():
    """ Increases the system recursion limit and stack size """
    sys.setrecursionlimit(2 ** 16)
    soft_limit, hard_limit = resource.getrlimit(resource.RLIMIT_STACK)
    resource.setrlimit(resource.RLIMIT_STACK, (hard_limit, hard_limit))

def get_largest_scc_sizes(leaders, n=5):
    """ Returns the sizes of the n largest strongly connected components 
        based on a dict that indicates the leader of each vertex """
    scc_sizes = {}
    for leader in leaders.itervalues():
        scc_sizes[leader] = scc_sizes.get(leader, 0) + 1
    largest_scc_sizes = scc_sizes.values()
    largest_scc_sizes.sort(reverse=True)
    return largest_scc_sizes[:n]

def main(program, limit=None, *args):
    """ Main program """
    graph = {} # dict of vertex number to list of tail vertex numbers
    graph_rev = {} # same graph but with directed edges reversed

    # parse every line representing a directed edge
    for line in sys.stdin:
        row = line.strip()
        try:
            u, v = map(int, row.split())
        except Exception:
            sys.stderr.write('Not a pair of integers: %r\n' % row)
            sys.exit(1)
        add_edge(graph, u, v)
        add_edge(graph_rev, v, u)

    # get the leaders of the strongly connected component for each vertex
    increase_recursion_limit()
    leaders = kosaraju(graph, graph_rev)

    # print the sizes of the n largest strongly connected components
    largest_scc_sizes = get_largest_scc_sizes(leaders, n=int(limit or 5))
    print ','.join(map(str, largest_scc_sizes))

# usage: python kosaraju.py < SCC.txt
if __name__ == '__main__':
    main(*sys.argv)

