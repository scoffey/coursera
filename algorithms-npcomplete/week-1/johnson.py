#!/usr/bin/env python2.7
  
import heapq
import sys

def dijkstra(graph, source):
    """ Finds the distance between source and each node of the given graph
        using Dijkstra's algorithm """

    queue = [(0, source)]
    distances = {source: 0}
    predecessors = {}
    visited = set()

    while queue:
        # get node with shortest distance so far and mark it as visited
        distance, node = heapq.heappop(queue)
        visited.add(node)
        # find the min distance of each of the node's unvisited neighbors
        for neighbor, edge_length in graph[node]:
            if neighbor not in visited:
                next_distance = distance + edge_length
                d = distances.get(neighbor) # None for infinite distance
                if d is None or next_distance < d:
                    distances[neighbor] = next_distance
                    predecessors[neighbor] = node
                    heapq.heappush(queue, (next_distance, neighbor))

    return distances, predecessors

def bellman_ford(graph, source):
    """ Finds the distance between source and each node of the given graph
        using the Bellman-Ford algorithm """

    distances = {source: 0}
    predecessors = {}

    # collect all the edges (head, tail, length) in a single list
    edges = []
    for u, outgoing_edges in graph.iteritems():
        for v, edge_length in outgoing_edges:
            edges.append((u, v, edge_length))

    # relax the edge distance computation until convergence
    for i in xrange(len(graph) - 1):
        for u, v, edge_length in edges:
            du = distances.get(u) # None for infinite distance
            dv = distances.get(v)
            if du is not None and (dv is None or du + edge_length < dv):
                distances[v] = du + edge_length
                predecessors[v] = u

    # run one more iteration to check if there are negative cost cycles
    for u, v, edge_length in edges:
        du = distances.get(u) # None for infinite distance
        dv = distances.get(v)
        if du is not None and (dv is None or du + edge_length < dv):
            return None, None

    return distances, predecessors

def johnson(graph):
    """ Finds the shortest path between all pairs of nodes of the given graph
        using Johnson's algorithm """
    # make a copy of the graph with an extra node connected to all the
    # original nodes by a directed edge of weight 0
    g = dict(graph)
    s = max(graph.iterkeys()) + 1
    g[s] = [(v, 0) for v in graph.iterkeys()]

    # run Bellman-Ford algorithm (and terminate if there are negative cycles)
    d, p = bellman_ford(g, s)
    if d is None:
        return None, None

    # re-weight the edges of the original graph using the distances found
    g.pop(s)
    for u, edges in graph.iteritems():
        g[u] = [(v, edge_length + d[u] - d[v]) for v, edge_length in edges]

    # run Dijkstra's algorithm for each node of the graph and fix
    # the resulting distances according to the previous re-weighting
    distances = {}
    predecessors = {}
    for u in g.iterkeys():
        du, pu = dijkstra(g, u)
        predecessors[u] = pu
        for v, reweighted_distance in du.iteritems():
            distances[(u, v)] = reweighted_distance - d[u] + d[v]

    return distances, predecessors

def to_path(predecessors, target):
    """ Rebuilds the path to a target node given a dict of predecessors """
    path = (target,)
    while path[0] in predecessors:
        node = predecessors[path[0]]
        path = (node,) + path
    return path

def main(program, *args):
    """ Main program """
    n = None
    m = None
    graph = {}

    # parse edges (head, tail, length) on each line
    for line in sys.stdin:
        s = line.strip()
        try:
            row = map(int, s.split())
        except Exception:
            sys.stderr.write('Not a row of integers: %s\n' % s)
            sys.exit(1)

        if n is None:
            n, m = row
            print 'Parsing %d vertices with %d edges...' % (n, m)
        else:
            u, v, edge_length = row
            if u not in graph:
                graph[u] = []
            graph[u].append((v, edge_length))

    # run Johnson's algorithm for all pairs shortest paths
    print 'Calculating shortest paths between all pairs of nodes...'
    distances, predecessors = johnson(graph)

    # print results
    if distances:
        d, pair = min((d, pair) for pair, d in distances.iteritems())
        u, v = pair
        path = to_path(predecessors[u], v)
        print 'The shortest shortest path is between ' \
                '%d and %d, with length %d' % (u, v, d)
        print 'Path:', ','.join(map(str, path))
    else:
        print 'Error: graph has a negative cost cycle'

# usage: python johnson.py < g1.txt
if __name__ == '__main__':
    main(*sys.argv)

