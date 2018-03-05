#!/usr/bin/env python2.7
  
import sys

def parse_bits(bits):
    """ Parses an array of bits (0 or 1) into an integer """
    node = 0
    for bit in bits:
        node = node << 1
        if bit == 1:
            node |= 1
        elif bit != 0:
            raise ValueError
    return node

def get_neighbors(node, bit_start, bit_end, distance):
    """ Returns the neighbors of the given integer up to the given Hamming
        distance, between the given bit numbers """
    out = []
    if distance > 0:
        for i in xrange(bit_start, bit_end):
            neighbor = node ^ (1 << i) # invert the i-th bit of node
            out.append(neighbor) # add 1-distance neighbor of node
            # recursively add neighbors of neighbor with 1 less in distance
            out.extend(get_neighbors(neighbor, i + 1, bit_end, distance - 1))
    return out

def merge_clusters(clusters, leaders, c1, c2):
    """ Merges the cluster c1 to c2 """
    reassigned_nodes = clusters.pop(c1)
    clusters[c2].extend(reassigned_nodes)
    for node in reassigned_nodes:
        leaders[node] = c2

def get_clusters(nodes, bit_count, spacing=2):
    """ Groups the given nodes (integers of the given bit count) by Hamming
        distance (number of different bits) for the given cluster spacing """
    leaders = dict((i, i) for i in nodes)
    clusters = dict((i, [i]) for i in nodes)
    distance = spacing - 1
    for u in nodes:
        for v in get_neighbors(u, 0, bit_count, distance):
            if v in leaders:
                c1, c2 = leaders[u], leaders[v]
                if c1 != c2:
                    if len(clusters[c2]) > len(clusters[c1]):
                        merge_clusters(clusters, leaders, c1, c2)
                    else:
                        merge_clusters(clusters, leaders, c2, c1)
    return clusters

def main(program, spacing='3', *args):
    """ Main program """
    spacing = int(spacing)
    bit_count = None
    node_count = None
    nodes = []

    # parse bits on every line
    for line in sys.stdin:
        s = line.strip()
        try:
            row = map(int, s.split())
        except Exception:
            sys.stderr.write('Not a row of integers: %s\n' % s)
            sys.exit(1)

        if bit_count is None:
            node_count, bit_count = row
            print 'Parsing %d numbers of %d bits...' % (node_count, bit_count)
        else:
            try:
                nodes.append(parse_bits(row))
            except ValueError:
                sys.stderr.write('Not an array of bits: %s\n' % s)
                sys.exit(1)

    # group nodes into clusters by Hamming distance for the given spacing
    clusters = get_clusters(nodes, bit_count, spacing)
    print 'Number of clusters with %d spacing: %d' % (spacing, len(clusters))

# usage: python hamming.py [spacing] < clustering_big.txt
if __name__ == '__main__':
    main(*sys.argv)

