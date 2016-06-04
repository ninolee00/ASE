#!/usr/bin/python

# generate a unique mapped sam file from HopHat2 output
# usage: uniq_sam4Tophat2.py accepted_hits.sam > accepted_hits_uniq.sam
# input: a sam file (accepted_hits.sam) from TopHat2 output
# output: a _uniq.sam file (accepted_hits_uniq.sam)

import sys

# input
file = sys.argv[1]
data = open(file, "r")

for line in data:
    col = line.split()
    if line.startswith("@"):
        print line,
    ### select errorous lines (line start with number) and select uniqely maapped read
    elif col[0][0].isalpha() and col[4] == "50":
        print line,
data.close()

