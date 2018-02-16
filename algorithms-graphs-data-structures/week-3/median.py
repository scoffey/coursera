#!/usr/bin/env python2.7

import sys
import heapq

def insert(max_heap, min_heap, i):
    """ Inserts a number in a pair of heaps that maintain the median value
        on every call, in logarithmic time. """
    # heapq works like a min-heap but can behave like a max-heap using
    # the additive inverse of values
    if not max_heap:
        heapq.heappush(max_heap, -i)
    else:
        # insert new item in min_heap if larger than median, else in max_heap
        if i > -max_heap[0]:
            heapq.heappush(min_heap, i)
            # if the new item makes min_heap larger, move its min to max_heap
            if len(max_heap) < len(min_heap):
                j = heapq.heappop(min_heap)
                heapq.heappush(max_heap, -j)
        else:
            heapq.heappush(max_heap, -i)
            # if the new item makes max_heap larger by more than 1,
            # move its max to min_heap
            if len(max_heap) - len(min_heap) > 1:
                j = -heapq.heappop(max_heap)
                heapq.heappush(min_heap, j)
    return -max_heap[0] # median is the root of max_heap

def main(program, *args):
    """ Main program """
    min_heap = []
    max_heap = []
    median_sum = 0

    # parse an integer on every line and apply the median maintenance
    # algorithm to calculate the median value of the stream so far
    for line in sys.stdin:
        try:
            i = int(line.strip())
        except ValueError:
            sys.stderr.write('Not an integer: %s\n' % line.strip())
            sys.exit(1)

        median = insert(max_heap, min_heap, i)
        median_sum += median

    print 'sum of medians: %d' % median_sum

# usage: python median.py < Median.txt
if __name__ == '__main__':
    main(*sys.argv)

