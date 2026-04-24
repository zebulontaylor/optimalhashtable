# Devlog

## Feb 18

Today I wrote the elastic hash table insertion logic. I'm using a rather functional style to get the project off the ground; I will probably have to change this later. One issue I faced with insertion was that the bucket calculation they provided only applies to buckets >= 1. A thing that REALLY messed with me is that their arrays are one-indexed (A1, A2, ...) but their batches are zero-indexed (B0, B1, ...). I think they did this to make some notation slightly cleaner but it took me an hour or so to realize what was going on.

## Feb 19

The paper didn't explicitly explain how searches work??? So yesterday I started trying out search by just brute forcing all the (i, j) pairs that could have been used as insertion addresses. Today I modified it to go sweep the low i values for all j values, which seems to improve performance. But I will have to keep working on it.

## Feb 20

I refactored the elastic hash table to be a class and also wrote a naive hashtable to serve as a baseline. I'm also working on a new testing setup that supports both classes and is able to do very a apples-to-apples comparison across different table parameters (delta, size, test probes). I'm also pretty confident that the right way to search is to sort all the possible keys by the bitwise representation the paper had, and then sweep them in ascending order. This performs best on my tests, but will probably depend on how full the table is & similar.

## Mar 14

I'm just modifying the testing infra today to be able to sweep a bunch of parameters and write the performance info to a csv that I can use for my report/presentation.
