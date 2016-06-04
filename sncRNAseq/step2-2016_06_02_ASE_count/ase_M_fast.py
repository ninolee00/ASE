#!/usr/bin/python

# caculate ase fast (read list and sam file only once)
# usage: ase_M_fast.py all_sam_order.list accepted_hits_uniq_chr_M.sorted.sam > accepted_hits.ase
# list and sam file should be in coordinate order
# sam file is output of uniq_chr_correct_M4sam.py
# input file can be gzip or not gzip files

import sys
import gzip  # for gzip input


def check_NID(col): # col is SIGAR, check if there are junction, insert, and deletion (N, I, D)
    NID = False
    for i in col:
        if i in ["N", "I", "D"]:
            NID = True
    return NID

def read_M(data_sam):
    # read sam as removing header and junction, insert, and deletion (N, I, D) containing reads
    # end of file returns ""
    line_sam = data_sam.readline()
    # output for end of file
    if line_sam == "":
        return ""
    # remove head
    while (line_sam.startswith("@")):
        line_sam = data_sam.readline()
    col = line_sam.split()[5]  # SIGAR

    # remove junction, insert, and deletion (N, I, D)
    while (check_NID(col)):
        line_sam = data_sam.readline()
        col = line_sam.split()[5]
    return line_sam


# for ASE calcualtion
def allele_count(list, pos):
    dic = {}
    for line in list:
        col = line.split()
        loc = pos - int(col[3])
        if loc <= len(col[9])-1 :   ## one more line_sam fileter for truncated short line
            if not col[9][loc] in dic:
                dic[col[9][loc]] =1
            else:
                dic[col[9][loc]] = dic[col[9][loc]] + 1
    return dic

# print ASE
def print_ASE(line_list, dic):  # dic is output of allele1
    col_list = line_list.split()
    seq1 = col_list[2]  # ref seq
    seq2 = col_list[3]  # SNP seq
    if not seq1 in dic:
        dic[seq1] = 0
    if not seq2 in dic:
        dic[seq2] = 0
    print line_list.strip() + "\t",
    print str(dic[seq1]) +"\t"+ str(dic[seq2]) +"\t",
    del dic[seq1]
    del dic[seq2]
    # delete "N". "x" generated from uniq_chr_correct_50M4sam.py --> change to "N" during samtools sort
    if "N" in dic:
        del dic["N"]
    return dic


# input (list file)
file1 = sys.argv[1]

if file1.endswith(".gz"):
    data_list = gzip.open(file1, "rb")
else:
    data_list = open(file1, "r")


# input (.sam_uniq file)
file2 = sys.argv[2]
if file2.endswith(".gz"):
    data_sam = gzip.open(file2, "rb")
else:
    data_sam = open(file2, "r")

# first sam read collection
line_sam = read_M(data_sam)
col_sam = line_sam.split()


chr = ""   # sam file has to be sorted by coordinate
sam_chr_list = []  # to check processed chr in sam
if not col_sam[2] in sam_chr_list:
    sam_chr_list.append(col_sam[2])

# read a list file
for line_list in data_list:
    col_list = line_list.split()
    if chr != col_list[0]:
        list = []
    chr = col_list[0]
    pos = int(col_list[1])
    seq1 = col_list[2]  # ref seq
    seq2 = col_list[3]  # SNP seq

    if line_sam == "" and not line_list:
        data_sam.close()
        break

    if line_sam == "" and line_list:
        out_dic = allele_count([], pos)
        print  print_ASE(line_list, out_dic)

    if line_sam != "" and line_list:
        # if sam ends at a certain chr before list ends
        if chr != col_sam[2] and chr in sam_chr_list:
            out_dic = allele_count([], pos)
            print  print_ASE(line_list, out_dic)

        else:
            ### read sam file until find the same chr from sam file  ###
            # first read pass for the firt sam read
            while (not chr in sam_chr_list):
                line_sam = read_M(data_sam)
                col_sam = line_sam.split()
                if line_sam == "":
                    data_sam.close()
                    break
                if not col_sam[2] in sam_chr_list:
                    sam_chr_list.append(col_sam[2])

            # first read pass in the sam chr
            # while (chr in sam_chr_list and chr == col_sam[2] and int(col_sam[3]) < pos - 49):  # 50bp read only is 49,  100bp read only is 99
            while (chr in sam_chr_list and chr == col_sam[2] and int(col_sam[3]) < pos - (len(col_sam[9])-1 + 10000) ): ## work for all read length # 10000bp window not to miss short read. work fine read <= 10000bp
                line_sam = read_M(data_sam)
                col_sam = line_sam.split()
                if line_sam == "":
                    data_sam.close()
                    break
                if not col_sam[2] in sam_chr_list:
                    sam_chr_list.append(col_sam[2])

            ### trim out-of-range sam  ###
            # count out-of-range sam
            n = 0
            for i in list:
                col = i.split()
                # if int(col[3]) < pos - 49:   # 50bp is 49,  100bp read is 99
                if int(col[3]) < pos - (len(col_sam[9])-1 + 10000):   ## work for all read length # 10000bp window not to miss short read. work fine read <= 10000bp
                    n += 1
            # delete out-of-range sam from list
            for j in range(0,n):
                list.pop(0)

            ### add in-range sam ###
            while (line_sam != "" and int(col_sam[3]) <= pos and chr == col_sam[2]):
                list.append(line_sam)
                line_sam = read_M(data_sam)
                col_sam = line_sam.split()
                if line_sam == "":
                    data_sam.close()
                    break
                if not col_sam[2] in sam_chr_list:
                    sam_chr_list.append(col_sam[2])

            # check SNP for begining
            out_dic = allele_count(list, pos)
            print  print_ASE(line_list, out_dic)

data_list.close()
