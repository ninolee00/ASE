#!/usr/bin/python

'''
## from metaData_mine.txt find info from meta_242samples_201603.txt
## for sample_name, consider ba41_42_22 and ba41-42-22 same (AN00493_ba41_42_22_105 = AN00493_ba41-42-22_105)
## usage: select_metData_v1.py mapping_stat4tophat_masked3rd.txt meta_242samples_201603.txt > metaData4tophat_masked3rd_final.txt

==> metaData_mine.txt <==
	sample	Brain.ID	Region	fastq	clip_fastq	unmapped_read	uniquely_mapped_read
Sample_A012_12-BA41-42-22_A012_12_ba41-42-22_3rd	A012_12_ba41_42_22_3rd	A012_12	ba41/42/22	4994715	4448218	196395	280132
Sample_A012_12-BA9_A012_12_ba9_3rd	A012_12_ba9_3rd	A012_12	ba9	4250364	3956404	227606	362785

==> meta_242samples_201603.txt <==
        Brain.ID        Diagnosis       Age..yrs.       Sex     Ethnicity       Region  Brain.bank      RIN     PMI..hrs.       TotalOrSelectedRNA      Lib_prep_batch  Seizures
AN00493_ba41_42_22_105  AN00493 ASD     27      M       English-White   BA41/42/22      Harvard-ATP     7.3     8.3     S       16      N       N       N       Synthroid       dr
AN00764_ba41_42_22_62   AN00764 ASD     20      M       English-White   BA41/42/22      Harvard-ATP     2.5     23.7    S       11      N       N       N       minocin, benzamyci
'''

import sys

file1 = sys.argv[1]
data = open(file1, "r")

file2 = sys.argv[2] ## metData file

def find_data(sample, brainID, region):
	data = open(file2, "r")  ## metData file
	for line in data:
		col = line.rstrip().split("\t")
		out = col[2:6]+col[7:]
		sample_meta = col[0]
		brainID_meta = col[1]
		region_meta = col[6]

		## replace ba41_42_22 to ba41-42-22
		sample_fix = sample.replace("ba41_42_22", "ba41-42-22")
		sample_meta_fix = sample_meta.replace("ba41_42_22", "ba41-42-22")

		if sample_fix == sample_meta_fix:
			data.close()
			return out+["Y"]
		#elif brainID == brainID_meta and region == region_meta:
		#	data.close()
		#	return out+["N"]
		elif brainID == brainID_meta:
			data.close()
			return out+["N"]
	data.close()
	return ["-"]*len(out)+["N"]

for line in data:
	col = line.rstrip().split("\t")
	sample = col[1]
	brainID = col[2]
	region = col[3]
	#if line.startswith("Sample_"):
	if col[-1].isdigit():
		print "\t".join(col + find_data(sample, brainID, region))
		#print col + find_data(sample, brainID, region), len(col + find_data(sample, brainID, region)), len(col), len(find_data(sample, brainID, region))
	else:
		data2 = open(file2, "r")
		for line2 in data2:
			col2 = line2.rstrip().split("\t")
			out2 = col2[2:6]+col2[7:]+["metData"]
			#print col2[2:6], col2[7:], ["metData"]
			print "\t".join(col + out2)
			#print col + out2, len(col + out2), len(col), len(out2)
			break
		data2.close()

data.close()
