#!/usr/bin/python

## put present%, good snp%, hetero%, allele ratio%, and pass/fail by present% and good snp%
## present: >=10 read present 
## good snp: minor allele (3rd and 4th allele) <= 5% of 1st allele
## hetorozygous SNP: 2nd allele >=2, 1st allele/2nd allele <= 5 and 3rd allele < 50% of 2nd allele
## for no_PAR at chrX, delete male allele count to "0,0,0,0"
## usage: filter_ase4PAR.py all_no_bias_sam_order.ase_reorder 20 80 > all_no_bias_sam_order.ase_reorder_20_80
## input: file name, present%, and good snp%
## This program print all ase data and evaluation data as well without filter out data
## ase data column + evaluation data column (at the end of line for both header and body)

import sys

# input
file1 = sys.argv[1]
data = open(file1, "r")

present_per = sys.argv[2]  # read (>=10) present percent
good_per = sys.argv[3]     # good snp percent

# read a file
for line in data:
    col = line.strip().split("\t")
    if not col[1].isdigit():  # col[1].isdigit(): if all characters are digit, true
        print line.strip()+"\tpresent(%)\tgood_snp(%)\thetero(%)\tallele_ratio(%)\tsum\tpass"
        if col[2] == "sex":  # sex info
            f_num = 0
            sex = col[:]
            for s in sex:
                if s == "F":   
                    f_num += 1   ## female number count for PAR at chrX
    else:
	# set variables
        num1, num2, num3, num4 = (0,0,0,0)  # each allele counts
        present = 0.0   # present read for > 10 reads present
        hetero = 0.0    # hetero snp
        bad = 0.0       # bad snp

        ## check pseudoautosomal regions(PAR) for chrX
        # PAR1: chrX:60001-2699520, chrY:10001-2649520
	# PAR2: chrX:154931044-155260560, chrY:59034050-59363566
	# PAR3: chrX:88400000-92000000, chrY:3440000-5750000
        if col[0] == "chrX":
            no_par = True  # no pseudoautosomal regions(PAR)
            if int(col[1])>= 60001 and int(col[1]) <= 2699520:
                no_par = False  # PAR1                
            if int(col[1])>= 88400000 and int(col[1]) <= 92000000:
                no_par = False  # PAR3        
            if int(col[1])>= 154931044 and int(col[1]) <= 155260560:
                no_par = False  # PAR2

        # no PAR data process for chrX --> delete male allele count
            for j in range(len(col)):
                if no_par and sex[j] == "M":  # for no PAR at chrX and male
                    col[j] = "0,0,0,0"  # delete male count 
        
                
        for i in range(5, len(col)):
            a1, a2, a3, a4 = (int(col[i].split(",")[0]), int(col[i].split(",")[1]), int(col[i].split(",")[2]), int(col[i].split(",")[3]))
            # sum count
            num1 += a1
            num2 += a2
            num3 += a3
            num4 += a4
            
            # calulate present%
            if a1 + a2 >= 10:   # read threshold: 10
                present += 1

            # check hetero
            # if a1 and a2:
            if min(a1, a2) >= 2 and max(a1, a2) <= 5.0 * min(a1, a2) and max(a3, a4) < 0.5 *min(a1, a2):
            # if min(a1, a2) >= 2 and max(a3, a4) < 0.5 *min(a1, a2): 
                hetero += 1
                
            # check good snp
            if a3 > max(a1, a2)*5/100 or a4 > max(a1, a2)*5/100:   # 3rd or 4th alleles: <= 5% of 1st allele
                bad += 1
                
        # calculate ratio
        ## setup total
        total = len(col)-5
	if col[0] == "chrX":
	    if no_par:     # no PAR at chrX
                total = f_num

        # present %
        present_out = 100 * present / total
        # good_snp%
        good_out = 100 - (100 * bad / total)
        # sum
        sum_out =str(num1)+","+str(num2)+","+str(num3)+","+str(num4)
        # hetero%
        hetero_out = 100 * hetero / total
        # allele ratio%
        if num1 + num2:
            allele_ratio = 100.0 * min(num1, num2)/max(num1, num2)
        else:
            allele_ratio = "NA"  # no allele1 and allele2 reads
        
        ## print output
        if present_out >= int(present_per) and good_out >= int(good_per):
            print "\t".join(col)+"\t"+str(present_out)+"\t"+str(good_out)+"\t"+str(hetero_out)+"\t"+str(allele_ratio)+"\t"+str(sum_out)+"\tpass"
        else:
            print "\t".join(col)+"\t"+str(present_out)+"\t"+str(good_out)+"\t"+str(hetero_out)+"\t"+str(allele_ratio)+"\t"+str(sum_out)+"\tfail"

data.close()

