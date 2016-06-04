#!/bin/bash

# runASE using $SCRATCH and $TMPDIR

PATH=$PATH:/u/project/eeskin/geschwind/ninolee0/bin  ### samtools location
export PATH
PATH=$PATH:/u/project/eeskin/geschwind/ninolee0/bin/program  ### homemade program location
export PATH

ROOT=$1  # Sample_AN13872_ba41-42-22_50 from Sample_AN13872_ba41-42-22_50_clip_tophat2_masked_3rd_output

echo
echo "########################"
echo "#### ASE calcuation ####"
echo "########################"
echo
echo "### ${ROOT} ASE process start ###"
date
echo

## go to directory where bam file is
cd /u/scratch/n/ninolee0/sncRNAseq/tophat2_masked_3rd_mapping/${ROOT}_clip_tophat2_masked_3rd_output


echo "### bam2sam ###"
echo "## output: ${ROOT}.sam ##"
date
echo
samtools view -h accepted_hits.bam > $TMPDIR/${ROOT}.sam


echo "### uniq_chr_correct_M4sam.py : prep sam to count allele by ase_M_fast.py ###"  # not nessarary for ref_bias check
date                                                                                    # add chr, remove errors (number starting sam line),
echo                                                                                    #convert junction, ins, del (N, I, D) --> M (missing part x for seq, i for qaul)
#uniq_chr_correct_50M4sam_v1.py $TMPDIR/${ROOT}.sam > $TMPDIR/${ROOT}_uniq_chr_M.sam  # for 50mer read only
uniq_chr_correct_M4sam.py $TMPDIR/${ROOT}.sam > $TMPDIR/${ROOT}_uniq_chr_M.sam  # work for all seq length
rm $TMPDIR/${ROOT}.sam


echo
echo "### sam2bam: uniq_chr_M.sam to uniq_chr_M.bam ###"
date
samtools view -bS $TMPDIR/${ROOT}_uniq_chr_M.sam > $TMPDIR/${ROOT}_uniq_chr_M.bam  # not nessarary for ref_bias check
rm $TMPDIR/${ROOT}_uniq_chr_M.sam

echo
echo "### sort: uniq_chr_M.bam to uniq_chr_M.sorted.bam ###"
date
samtools sort $TMPDIR/${ROOT}_uniq_chr_M.bam $TMPDIR/${ROOT}_uniq_chr_M.sorted  # not nessarary for ref_bias check
rm $TMPDIR/${ROOT}_uniq_chr_M.bam

echo
echo "### bam2sam: uniq_chr_M.sorted.bam to uniq_chr_M.sorted.sam ###"
date
samtools view -h $TMPDIR/${ROOT}_uniq_chr_M.sorted.bam > $TMPDIR/${ROOT}_uniq_chr_M.sorted.sam  # not nessarary for ref_bias check
rm $TMPDIR/${ROOT}_uniq_chr_M.sorted.bam

echo "### ase_M_fast.py : allele count for seq read length (<= 10000bp) ###"
date
echo

## ase for 50mer read
#ase_50M_fast_v1.py /u/project/eeskin/geschwind/ninolee0/allele/all_snp_list/all_sam_order.list $TMPDIR/${ROOT}_uniq_chr_M.sorted.sam > $TMPDIR/${ROOT}.ase  # only for regular ase calculation

## for  all (<= 10000bp) reads
# - ase for all list: all_sam_order.list.gz
ase_M_fast.py /u/project/eeskin/geschwind/ninolee0/allele/all_snp_list/all_sam_order.list.gz $TMPDIR/${ROOT}_uniq_chr_M.sorted.sam > $TMPDIR/${ROOT}.ase  # only for regular ase calculation  # work for seq read length (<= 10000bp)

# - ase for no ref biased all list: all_no_bias_sam_order.list.gz
ase_M_fast.py /u/project/eeskin/geschwind/ninolee0/allele/all_snp_list/masked_reference/ref_bias/ref_bias_final_result/all_no_bias_sam_order.list.gz $TMPDIR/${ROOT}_uniq_chr_M.sorted.sam > $TMPDIR/${ROOT}_no_bias.ase  # only for regular ase calculation  # work for seq read length (<= 10000bp)

# all list file: /u/project/eeskin/geschwind/ninolee0/allele/all_snp_list/all_sam_order.list.gz
# no ref bias all list file: /u/project/eeskin/geschwind/ninolee0/allele/all_snp_list/masked_reference/ref_bias/ref_bias_final_result/all_no_bias_sam_order.list.gz, (soft link: /u/project/eeskin/geschwind/ninolee0/allele/all_snp_list/all_no_bias_sam_order.list.gz)

rm $TMPDIR/${ROOT}_uniq_chr_M.sorted.sam


echo "### ase_one_line.py ###"
date
echo
## mv ase file to current directory to have short header line: /work/1524477.1.eeskin_idre.q/UMB4334_ba41-42-22_1st.ase --> UMB4334_ba41-42-22_1st.ase
cp $TMPDIR/${ROOT}*.ase .

ase_one_line.py ${ROOT}.ase > ${ROOT}.ase_one_line
ase_one_line.py ${ROOT}_no_bias.ase > ${ROOT}_no_bias.ase_one_line


echo "### gzip ###"
date
echo
gzip ${ROOT}*.ase
gzip ${ROOT}*.ase_one_line


echo "### ${ROOT} change directory name and mv log file ###"
date
echo

# last step before finishing run
mv /u/scratch/n/ninolee0/sncRNAseq/tophat2_masked_3rd_mapping/${ROOT}_clip_tophat2_masked_3rd_output /u/scratch/n/ninolee0/sncRNAseq/tophat2_masked_3rd_mapping/${ROOT}_clip_tophat2_masked_3rd_output-done
mv /u/scratch/n/ninolee0/sncRNAseq/tophat2_masked_3rd_mapping/${ROOT}_ase.log /u/scratch/n/ninolee0/sncRNAseq/tophat2_masked_3rd_mapping/${ROOT}_clip_tophat2_masked_3rd_output-done


echo
echo "#######################"
echo "### ASE process end ###"
echo "#######################"
date
echo






########################################################
######################### code #########################
########################################################

### ASE calculation job submission using -highp ###
### runASE_scTmp_v1.sh run (24hr) @ SCRATCH
cd /u/scratch/n/ninolee0/sncRNAseq/tophat2_masked_3rd_mapping/
for line in *_output; do
name=`basename $line _clip_tophat2_masked_3rd_output`
echo ${name} ${name}_clip_tophat2_masked_3rd_output
qsub -l highp -cwd -o /u/scratch/n/ninolee0/sncRNAseq/tophat2_masked_3rd_mapping/${name}_ase.log -e /u/scratch/n/ninolee0/sncRNAseq/tophat2_masked_3rd_mapping/${name}_ase.log -l h_data=4096M,h_rt=24:00:00 /u/scratch/n/ninolee0/sncRNAseq/code/runASE_scTmp_v1.sh ${name}
done


########################################################

[ninolee0@login4 hg19_masked_3rd_mapping_code]$ cat runASE_scratch.sh_code
# move the previous mapping and ase data into hoffman2 at /u/scratch/n/ninolee0

# directory location (bam files): /u/scratch/n/ninolee0
# runASE_scatch.sh and runASE_scatch.sh_code location: /u/home/eeskin/ninolee0/allele/48moreSamples/hg19_masked_3rd_mapping_code

cd /u/scratch/n/ninolee0

## change directory name
for line in *_PE_tophat_multiread_output-done; do
name=`basename $line _PE_tophat_multiread_output-done`
echo ${name} ${name}_PE_tophat_multiread_output-done
mv ${name}_PE_tophat_multiread_output-done ${name}_PE_tophat_multiread_output
done

### runASE.sh run (24hr)
for line in *_PE_tophat_multiread_output; do
name=`basename $line _PE_tophat_multiread_output`
echo ${name} ${name}_PE_tophat_multiread_output
qsub -cwd -o /u/scratch/n/ninolee0/${name}_correct_ase.log -e /u/scratch/n/ninolee0/${name}_correct_ase.log -l h_data=4096M,h_rt=24:00:00 -pe shared 8 /u/home/eeskin/ninolee0/allele/48moreSamples/hg19_masked_3rd_mapping_code/runASE_scratch.sh ${name}
done

