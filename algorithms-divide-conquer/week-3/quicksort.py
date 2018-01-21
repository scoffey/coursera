#!/usr/bin/env python2.7

import sys
import random

def choose_pivot_on_first(array, left, right):
    return left

def choose_pivot_on_last(array, left, right):
    return right - 1

def choose_pivot_on_median(array, left, right):
    """ Returns the index of the median value among the first, the middle
        and the last elements of the slice of the given array that spans
        between indexes left and right - 1. """
    m = int((left + right - 1) / 2)
    first = array[left]
    middle = array[m]
    last = array[right - 1]
    x = first - middle
    y = middle - last
    z = first - last
    if x * y > 0: return m
    if x * z > 0: return right - 1
    return left

def choose_pivot_randomly(array, left, right):
    """ Returns a random index between left and right - 1. """
    return random.randrange(left, right)

def partition(array, left, right):
    """ Partitions the array between indexes left and right - 1 so that
        all elements smaller than the pivot (initially at the left index)
        are to its left and all the elements greater than the pivot are
        to its right. """
    p = array[left] # pivot value
    i = left + 1 # index that separates parts smaller/greater than pivot
    for j in range(left + 1, right): # index that separates unpartitioned values
        if array[j] < p:
            array[i], array[j] = array[j], array[i]
            i = i + 1
    # swap pivot to put it at its final position
    array[left], array[i - 1] = array[i - 1], array[left]
    return i - 1 # return new pivot index

def quicksort(array, left, right, choose_pivot):
    """ Sorts the given array between indexes left and right - 1,
        using the given method for selecting the pivot position. """

    if right - left  <= 1:
        return 0

    pivot = choose_pivot(array, left, right) # index of the selected pivot
    array[left], array[pivot] = array[pivot], array[left] # pre-processing swap
    pivot = partition(array, left, right) # new pivot index after partition

    count = right - left - 1 # comparison count
    left_count = quicksort(array, left, pivot, choose_pivot)
    right_count = quicksort(array, pivot + 1, right, choose_pivot)
    return count + left_count + right_count

def main(program, method='first', *args):
    """ Main program """
    array = []

    for line in sys.stdin:
        s = line.strip()
        try:
            array.append(int(s))
        except ValueError:
            sys.stderr.write('Not an integer: %s\n' % s)
            sys.exit(1)

    methods = {
        'first': choose_pivot_on_first,
        'last': choose_pivot_on_last,
        'median': choose_pivot_on_median,
        'random': choose_pivot_randomly
    }
    if not method or method.lower() not in methods:
        sys.stderr.write('Not a valid method: %s\n' % method)
        sys.exit(1)
    choose_pivot = methods.get(method)

    count = quicksort(array, 0, len(array), choose_pivot)
    print '\n'.join(map(str, array))
    print 'comparison count: %d' % count

if __name__ == '__main__':
    main(*sys.argv)

