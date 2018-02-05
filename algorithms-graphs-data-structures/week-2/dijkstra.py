#!/usr/bin/env python2.7

import sys
import heapq

def dijkstra(graph, source, target):
    """ Implements Dijkstra's algorithm for finding the shortest path
        between source and target in a graph. """

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

    # rebuild the shortest path using the predecessor pointers
    path = (target,)
    while path[0] in predecessors:
        node = predecessors[path[0]]
        path = (node,) + path

    # return the distance and shortest path from source to target
    return distances.get(target), path

def main(program, *args):
    """ Main program """
    graph = {}

    # parse every line representing an adjacency list with weights
    parse_weighted_edge = lambda pair: tuple(map(int, pair.split(',')))
    for line in sys.stdin:
        row = line.strip().split()
        try:
            v = int(row[0])
            graph[v] = tuple(map(parse_weighted_edge, row[1:]))
        except Exception:
            sys.stderr.write('Not a valid adjacency list: %r\n' % row)
            sys.exit(1)

    # parse source and target vertices from arguments
    try:
        source = int(args[0])
        targets = map(int, args[1:])
    except Exception:
        sys.stderr.write('Invalid source and target(s): %r\n' % args)
        sys.exit(1)

    # print distance and shortest path between source and each target
    for target in targets:
        distance, path = dijkstra(graph, source, target)
        print '%r\t%s' % (distance, '-'.join(map(str, path)))

# usage: python dijkstra.py [source] [target...] < dijkstraData.txt
if __name__ == '__main__':
    main(*sys.argv)

