#!/usr/bin/env python2.7

from __future__ import division

import sys

def karatsuba(x, y):
    """
    Calculates the product of integers x and y using the Karatsuba algorithm.
    """
    if len(str(x)) == 1 or len(str(y)) == 1:
        return x * y
    else:
        m = max(len(str(x)), len(str(y)))
        m2 = m // 2

        a = x // 10 ** m2
        b = x % 10 ** m2
        c = y // 10 ** m2
        d = y % 10 ** m2

        z0 = karatsuba(b, d)
        z1 = karatsuba(a + b, c + d)
        z2 = karatsuba(a, c)

        return z2 * 10 ** (2 * m2) + (z1 - z2 - z0) * 10 ** m2 + z0

def str_karatsuba(x, y):
    """
    Calculates the product of numerical strings x and y using the Karatsuba
    algorithm.
    """
    xlen = len(x)
    ylen = len(y)

    if xlen == 1 or ylen == 1:
        return int(x) * int(y)
    else:
        m = max(xlen, ylen)
        m2 = m // 2

        a = x[0:m2].lstrip('0') or '0'
        b = x[m2:].lstrip('0') or '0'
        c = y[0:m2].lstrip('0') or '0'
        d = y[m2:].lstrip('0') or '0'

        z0 = str_karatsuba(b, d)
        z1 = str_karatsuba(str(int(a) + int(b)), str(int(c) + int(d)))
        z2 = str_karatsuba(a, c)

        return z2 * 10 ** (2 * m2) + (z1 - z2 - z0) * 10 ** m2 + z0

def main(program, x=None, y=None, *args):
    """ Main program """
    if not x or not y or not x.isdigit() or not y.isdigit():
        sys.stderr.write('usage: python %s [integer] [integer]\n' % program)
        sys.exit(1)
    else:
        print karatsuba(int(x), int(y))
        # print str_karatsuba(x, y)

if __name__ == '__main__':
    main(*sys.argv)

