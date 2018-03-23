#!/usr/bin/env python2.7
  
import sys

def optimal_bst(p):
    """ Calculates the weighted search cost of an optimal binary search tree
        with the given key probabilities """
    n = len(p)
    a = [[0] * n for i in xrange(n)]
    get = lambda i, j: 0 if i > j else a[i][j] # consider zeros under diagonal
    for s in xrange(n): # fill the 2D array diagonally
        for i in xrange(n):
            j = i + s
            if j < n:
                v = min(get(i, r - 1) + get(r + 1, j) for r in xrange(i, j + 1))
                a[i][j] = sum(p[i:j + 1]) + v
    return a[0][-1]

def main(program, *args):
    """ Main program """
    p = map(float, args) # probabilities of BST keys
    print optimal_bst(p)

# usage: python bst.py [probabilities...]
if __name__ == '__main__':
    main(*sys.argv)

