#!/usr/bin/python

'''
### calculate RPKM after (read + 1)
### usage: rpkm_calculation_v1.py all247_clip_sorted_uniq.smallRNA100_exon_count metaData_mine_final.txt > all247_clip_sorted_uniq_smallRNA100.rpkm

### output: does not have gene info

### input: 1MB_all247_clip_sorted_uniq.smallRNA100_exon_count, metaData_mine_final.txt

==> 1MB_all247_clip_sorted_uniq.exon_count <== # 9 information column, 10th column: read counts start
ensembl_gene_id hgnc_symbol     chromosome_name start_position  end_position    strand  band    gene_biotype    exonic_gene_size        Sample_A012_12-BA41-42-22_A012_12_ba41-42-22_
ENSG00000056678 KIFC1   HSCHR6_MHC_MCF  33529672        33530001        1       p21.32  processed_transcript    5       0       0       0       0       0       0       0       0
ENSG00000103253 HAGHL   16      776936  785525  1       p13.3   protein_coding  100     0       0       0       0       0       0       0       0       0       0       0       0
ENSG00000121335 PRB2    12      11544476        11653975        -1      p13.2   protein_coding  100     0       0       0       0       0       0       0       0       0       0


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
	out1 = [col1[0]]+col1[9:]  ## no gene_length for output ####<<<#### count starts from 10th col
	if not col1[-1].isdigit(): ### last column is not digit --> header
		print "\t".join(out1)
	else:
		## calculate RPKM
		gene_length = int(col1[8])   ####<<<#### exonic_gene_size at 9th col
		rpkm = []
		count = col1[9:] # list for string  ####<<<#### count starts from 10th col
		for i in range(len(count)):
			count_i = int(count[i]) + 1 ## add 1 for log2 transition
			mapped_read_i = mapped_read[i]
			rpkm_i = str(count_i * 1000.0 * 1000000 / (gene_length * mapped_read_i))
			rpkm.append(rpkm_i)
		print "\t".join([col1[0]]+rpkm)

data1.close()

