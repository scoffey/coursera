#!/usr/bin/env python2.7

import sys

def count_inversion(array):
    """ Returns the number of inversions in the given array """
    sorted_array, count = merge_count_inversion(array)
    return count

def merge_count_inversion(array):
    """ Returns a sorted copy of the given array (using merge sort algorithm)
        and the number of inversions in it """
    if len(array) <= 1:
        return array, 0
    middle = int(len(array) / 2)
    left, a = merge_count_inversion(array[:middle])
    right, b = merge_count_inversion(array[middle:])
    sorted_array, c = merge_count_split_inversion(left, right)
    return (sorted_array, a + b + c)

def merge_count_split_inversion(left, right):
    """ Returns the sorted merge of the given array slices and the number of
        split inversions between them """
    sorted_array = []
    count = 0
    i, j = 0, 0
    left_len = len(left)
    right_len = len(right)
    while i < left_len and j < right_len:
        if left[i] <= right[j]:
            sorted_array.append(left[i])
            i += 1
        else:
            sorted_array.append(right[j])
            count += left_len - i
            j += 1
    sorted_array += left[i:]
    sorted_array += right[j:]
    return sorted_array, count        

def main(program, *args):
    """ Main program """
    array = []

    for line in sys.stdin:
        s = line.strip()
        try:
            array.append(int(s))
        except ValueError:
            sys.stderr.write('Not an integer: %s\n' % s)
            sys.exit(1)

    print count_inversion(array)

if __name__ == '__main__':
    main(*sys.argv)

