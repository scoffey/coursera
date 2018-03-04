#!/usr/bin/env python2.7

import heapq
import sys

def add_job(jobs, score, weight, length):
    """ Adds a job with the given score, wight and length to a heap """
    # push a tuple of job score, weight and length into the jobs heap,
    # so that score tie-breaking is done by weight, but using their
    # additive inverse values for sorting in descending order
    heapq.heappush(jobs, (-score, -weight, length))

def get_schedule(jobs):
    """ Returns a schedule of jobs by descending score, using heap sort """
    return [heapq.heappop(jobs) for i in xrange(len(jobs))]

def get_total_completion_time(schedule):
    """ Returns the sum of weighted completion times of the scheduled jobs """
    time = 0 # time spent so far by previous jobs
    c = 0 # sum of weighted completion times
    for k, w, length in schedule:
        weight = -w # w is the additive inverse of weight
        time += length
        c += weight * time
    return c

def main(program, scoring='/', *args):
    """ Main program """
    jobs = []

    # parse job weight and length on every line (but first line is total count)
    delimiter = ' '
    for line in sys.stdin:
        s = line.strip()
        if delimiter not in line:
            print 'Scheduling %s jobs...' % s
        else:
            try:
                weight, length = map(int, s.split(delimiter))
            except Exception:
                sys.stderr.write('Not a pair of integers: %s\n' % s)
                sys.exit(1)
            # set score according to the scoring algorithm
            score = weight / float(length) if scoring == '/' \
                    else weight - length
            add_job(jobs, score, weight, length)

    # schedule jobs by score and print the sum of weighted completion times
    schedule = get_schedule(jobs)
    c = get_total_completion_time(schedule)
    print 'Sum of weighted completion times: %d' % c

# usage: python greedy_sched.py [scoring] < jobs.txt
if __name__ == '__main__':
    main(*sys.argv)

