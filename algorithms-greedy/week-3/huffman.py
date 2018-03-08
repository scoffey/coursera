#!/usr/bin/env python2.7
  
import heapq
import sys

def add_codes(codes, prefix, tree):
    """ Adds the Huffman code of the tree leaves to the given dict """
    value, left, right = tree
    if left is None or right is None:
        codes[value[0]] = prefix # value is a 1-symbol tuple
    if left is not None:
        add_codes(codes, prefix + '0', left)
    if right is not None:
        add_codes(codes, prefix + '1', right)

def set_node(node_lookup, value, left=None, right=None):
    """ Sets the left and right subtrees of the node of the given value """
    if value in node_lookup:
        node = node_lookup[value]
        node[1] = left
        node[2] = right
    else:
        node = [value, left, right]
        node_lookup[value] = node
    return node

def build_tree(alphabet, node_lookup):
    """ Builds a Huffman tree for coding the symbols of the given alphabet """
    pa, a = heapq.heappop(alphabet) # extract min weight and symbol tuple
    pb, b = heapq.heappop(alphabet)
    ab = a + b # combine symbol tuples
    left = set_node(node_lookup, a)
    right = set_node(node_lookup, b)
    if len(alphabet) == 0: # after popping 2 elements from the alphabet
        return [None, left, right]
    else:
        heapq.heappush(alphabet, (pa + pb, ab))
        tree = build_tree(alphabet, node_lookup)
        set_node(node_lookup, ab, left, right)
        return tree

def huffman(alphabet):
    """ Returns the Huffman codes for the symbols of the given alphabet
        (as a heap of tuples containing a weight and a 1-symbol tuple) """
    n = len(alphabet)
    if n < 2 or n % 2 != 0:
        raise ValueError('Invalid alphabet size: ' + n)
    node_lookup = {}
    tree = build_tree(alphabet, node_lookup)
    codes = {}
    add_codes(codes, '', tree)
    return codes

def main(program, *args):
    """ Main program """
    symbol_count = None
    alphabet = []
    symbol = 0

    # parse symbol weights on every line
    for line in sys.stdin:
        s = line.strip()
        try:
            w = int(s)
        except Exception:
            sys.stderr.write('Not an integer: %s\n' % s)
            sys.exit(1)

        if symbol_count is None:
            symbol_count = w
            print 'Parsing %d symbol weights...' % symbol_count
        else:
            heapq.heappush(alphabet, (w, (symbol,)))
            symbol += 1

    sys.setrecursionlimit(2 * symbol_count)
    codes = huffman(alphabet)
    minlen = min(len(i) for i in codes.itervalues())
    maxlen = max(len(i) for i in codes.itervalues())
    print 'Min code word bit length:', minlen
    print 'Max code word bit length:', maxlen

# usage: python huffman.py < huffman.txt
if __name__ == '__main__':
    main(*sys.argv)

