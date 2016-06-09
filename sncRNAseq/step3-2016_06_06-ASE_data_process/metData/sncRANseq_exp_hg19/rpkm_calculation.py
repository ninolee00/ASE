#!/usr/bin/python

'''
### calculate RPKM for (read + 1)
### usage: rpkm_calculation.py 1MB_all247_clip_sorted_uniq.exon_count metaData_mine_final.txt > 1MB_all247_clip_sorted_uniq.rpkm

### input: 1MB_all247_clip_sorted_uniq.exon_count, metaData_mine_final.txt

==> 1MB_all247_clip_sorted_uniq.exon_count <==
ENSG    gene_length     Sample_A012_12-BA41-42-22_A012_12_ba41-42-22_3rd        Sample_A012_12-BA9_A012_12_ba9_3rd      Sample_A206_89-CB_A2
ENSG00000000003 2968    0       0       1       0       1       0       0       0       0       1       0       0       0       0       1
ENSG00000000005 1610    0       0       0       0       0       0       0       0       0       0       0       0       0       0       0
ENSG00000000419 1207    0       0       0       0       0       1       0       0       0       0       1       0       0       0       0

==> metaData_mine_final.txt <==
        sample  Brain.ID        Region  fastq   clip_fastq      unmapped_read   uniquely_mapped_read    Diagnosis       Age..yrs.       Sex
Sample_A012_12-BA41-42-22_A012_12_ba41-42-22_3rd        A012_12_ba41_42_22_3rd  A012_12 ba41/42/22      4994715 4448218 196395  280132  -
Sample_A012_12-BA9_A012_12_ba9_3rd      A012_12_ba9_3rd A012_12 ba9     4250364 3956404 227606  362785  -       -       -       -       -
Sample_A206_89-CB_A206_89_vermis_3rd    A206_89_vermis_3rd      A206_89 vermis  4238134 3762482 311922  580496  -       -       -       -

'''

import sys

file1 = sys.argv[1]  ## count data

file2 = sys.argv[2] ## metData file

## collect uniqely mapped read
data2 = open(file2, "r")

mapped_read = []  ## uniqeuly mapped read list for all 247 samples 
for line2 in data2:
	if line2.startswith("Sample_"):
		col2 = line2.rstrip().split("\t")
		mapped_read.append(int(col2[7]))
data2.close()


data1 = open(file1, "r")
for line1 in data1:
	col1 = line1.rstrip().split("\t")
	out1 = [col1[0]]+col1[2:]  ## no gene_length for output
	if col1[0] == "ENSG":
		print "\t".join(out1)
	else:
		## calculate RPKM
		gene_length = int(col1[1])
		rpkm = []
		count = col1[2:] # list for string
		for i in range(len(count)):
			count_i = int(count[i]) + 1 ## add 1 for log2 transition
			mapped_read_i = mapped_read[i]
			rpkm_i = str(count_i * 1000.0 * 1000000 / (gene_length * mapped_read_i))
			rpkm.append(rpkm_i)
		print "\t".join([col1[0]]+rpkm)

data1.close()

