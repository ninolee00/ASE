[ninolee0@n2195 Sample_UMB4334_ba41-42-22_1st_clip_tophat2_masked_3rd_output-done]$ cat /u/project/eeskin/geschwind/ninolee0/bin/program/uniq_chr_correct_50M4sam_v1.py
#!/usr/bin/python

##  add chr before chromosome number if there is no chr (not 1 but chr1).
##  select unique mapped read
##  filter out errorous output (line start with number)
##  prepare sam for ase calculation (using ase_50M_fast_v2.py)
##  If cigar is not 50M, it generates new reads that have cigar, 50M
##  match quality length with sequence 
##  usage : uniq_chr_correct_50M4sam_v1.py accepted_hits.sam > accepted_hits_chr_uniq_50M.sam

import sys

def sum_list(list):
    sum = 0
    for i in list:
        sum +=i
    return sum

def print_list(col):
    # col is list
    line=""
    for i in range(len(col)-1):
        line += col[i]+"\t"
    return line+col[len(col)-1]+"\n"

def print_line(line):
    col = line.split()
    sig = col[5]
    first_seq = col[9]
    first_loc = col[3]
    first_qual = col[10]

    # update cigar
    col[5] = "50M"

    ### change chr format to chr1
    if col[2].find("chr") == -1:
        col[2] = "chr"+col[2]

    num = ""
    # M,N,I,and D are all characters for Tophat Cigar
    m = []  # aligned read length
    n = [] # splicing interval
    d = [] # deletion
    i = [] # insert

    seq_start =0   # seq start location [0:50]
    for j in sig:
        if j.isdigit():  # number
            num += j
        if j == "N":
            n.append(int(num))
            num =""
        if j == "I":
            i.append(int(num))
            num =""
        if j == "D":
            d.append(int(num))
            num = ""
        if j == "M":
            ## print output
            # update loc
            loc = int(first_loc)+sum_list(n)+sum_list(d)+sum_list(m)
            col[3] =str(loc)

            # update seq
            seq_start = sum_list(i)+sum_list(m)
            seq = first_seq[seq_start :seq_start +int(num)]+"x"*(50-int(num))
            col[9] = seq
            
            # update qual
            qual = first_qual[seq_start :seq_start +int(num)]+"I"*(50-int(num))
            col[10] = qual
            
            m.append(int(num))

            # print output
            print print_list(col),

            # reset num
            num = ""

# input
file = sys.argv[1]

data = open(file, "r")

for line in data:
    #  for header
    if line.startswith("@"):
        if line.startswith("@SQ"):
            # change chr format to chr1
            if line.find("SN:") != -1 and line.find("SN:chr") == -1:
                print line.replace("SN:", "SN:chr"),
            else:
                print line,
        else:
            print line,
    # for body
    else:
        col = line.split()
        # select only lines that start with an alphabetic character (not number) to overcome mapping error
        # select only unique mapped read
        if col[0][0].isalpha() and col[4] == "50":

            print_line(line)
data.close()