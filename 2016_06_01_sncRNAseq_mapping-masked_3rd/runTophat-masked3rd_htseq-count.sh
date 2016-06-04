#!/bin/bash

# file name: runTophat-masked3rd_htseq-count.sh
# run Topaht2 mapping and HTseq-count read_count for both bam and uniquely mapped bam
# sam files are stored during run at $TMPDIR/
# output: tophat2 output and more files (accepted_hits_sorted.bam, accepted_hits_sorted_uniq.bam, accepted_hits_sorted.bam.bai, accepted_hits_sorted_uniq.bam.bai, accepted_hits_sorted.exon_count, accepted_hits_sorted_uniq.exon_count)
# log file contains read numbers forß fastq, bam, and uniq.bam

PATH=$PATH:/u/home/n/ninolee0/project-geschwind/bin	  		  ### samtools location
PATH=$PATH:/u/project/eeskin/geschwind/ninolee0/bin/tophat-2.0.9.Linux_x86_64/  ### TopHat2 location
PATH=$PATH:/u/home/n/ninolee0/project-geschwind/bin/program	  ### uniq_sam4Tophat2.py location
PATH=$PATH:/u/home/n/ninolee0/.local/bin  					  ### htseq-count location

# TopHat version: v2.0.9
# samtools version: 0.1.19
# HTSeq version: 0.6.1p1


### load inputs
INPATH=$1  	# .fastq.gz file containing directory location: /u/scratch/n/ninolee0/sncRNAseq/clip_fastq/
name=$2    	# file name root: ${name}_clip of ${name}_clip.fastq.gz
# OUTPATH=$3  # /u/scratch/n/ninolee0/sncRNAseq/tophat2_masked_3rd_mapping/${name}_tophat2_masked_3rd_output 

echo
echo "########################################################"
echo "### start script: runTophat-masked3rd_htseq-count.sh ###"
echo "########################################################"
date
echo $INPATH, $name
echo

echo
echo "### tophat mapping ###"
date

#### tophat mapping ###

cd ${INPATH}    # .fastq.gz file containing directory location: /u/scratch/n/ninolee0/sncRNAseq/clip_fastq

GTF=/u/project/eeskin/geschwind/ninolee0/reference/Homo_sapiens.GRCh37.73.gtf

# BOWTIE_INDEX=/u/project/eeskin/geschwind/ninolee0/reference/index_bowtie2/hg19_vivek/hg19_vivek # hg19
# BOWTIE_INDEX=/u/project/eeskin/geschwind/ninolee0/reference/index_bowtie2/hg19_vivek_masked_N/hg19_vivek_masked_N  # hg19 masked using N
BOWTIE_INDEX=/u/project/eeskin/geschwind/ninolee0/reference/index_bowtie2/hg19_vivek_masked_3rd/hg19_vivek_masked_3rd  # hg19 masked using 3rd allele
## chr: just number, generated from Vivek's fa file: /u/project/eeskin/geschwind/ninolee0/reference/hg19_vivek.fa @ hoffman2

tophat -o /u/scratch/n/ninolee0/sncRNAseq/tophat2_masked_3rd_mapping/${name}_tophat2_masked_3rd_output -g 10 -p 8 --no-novel-juncs -G $GTF $BOWTIE_INDEX ${name}.fastq.gz


echo
echo "### total mapped read count per gene (ENSG) ###"
date

cd /u/scratch/n/ninolee0/sncRNAseq/tophat2_masked_3rd_mapping/${name}_tophat2_masked_3rd_output

echo "## sort"
samtools sort accepted_hits.bam accepted_hits_sorted

echo "## index"
samtools index accepted_hits_sorted.bam  ## for index, bam file should be sorted

echo "## bam to sam"
samtools view -h accepted_hits_sorted.bam > $TMPDIR/accepted_hits_sorted.sam

echo "## read count"
htseq-count --stranded=no --mode=union --type=exon --quiet $TMPDIR/accepted_hits_sorted.sam $GTF > accepted_hits_sorted.exon_count


echo
echo "### uniquely mapped read count per gene (ENSG) ###"
date

echo "## uniquely mapped read selection"
uniq_sam4Tophat2.py $TMPDIR/accepted_hits_sorted.sam > $TMPDIR/accepted_hits_sorted_uniq.sam

echo "## sam to bam"
samtools view -bS $TMPDIR/accepted_hits_sorted_uniq.sam > accepted_hits_sorted_uniq.bam

echo "## index"
samtools index accepted_hits_sorted_uniq.bam

echo "## read count"
htseq-count --stranded=no --mode=union --type=exon --quiet $TMPDIR/accepted_hits_sorted_uniq.sam $GTF > accepted_hits_sorted_uniq.exon_count

echo
echo "### mapped read number count ###"
date

echo "## read input number: _clip.fastq ##"
zcat ${INPATH}/${name}.fastq.gz | grep -c ^@ 
echo "## all mapped read: accepted_hits_sorted.bam ##"
grep -vc ^@ $TMPDIR/accepted_hits_sorted.sam
echo "## uniquely mapped read: accepted_hits_sorted_uniq.bam ##"
grep -vc ^@ $TMPDIR/accepted_hits_sorted_uniq.sam


echo
echo "### delte sam files ###"
date

### remove sam files
# rm $TMPDIR/*.sam


echo
echo "##########################"
echo "#### done with script ####"
echo "##########################"
date
echo


##################################################
####  runTophat-masked3rd_htseq-count.sh_code ####
##################################################

### code to run runTophat-masked3rd_htseq-count.sh 
cd /u/scratch/n/ninolee0/sncRNAseq/clip_fastq  ## fastq location

for file in *_clip.fastq.gz ; do
name=$(basename $file _clip.fastq.gz)
echo $name ${name}_clip.fastq.gz

## with 8 threads
qsub -l highp -cwd -o /u/scratch/n/ninolee0/sncRNAseq/tophat2_masked_3rd_mapping/${name}.log -e /u/scratch/n/ninolee0/sncRNAseq/tophat2_masked_3rd_mapping/${name}.log -l h_data=4096M,h_rt=24:00:00 -pe shared 8 /u/scratch/n/ninolee0/sncRNAseq/code/runTophat-masked3rd_htseq-count.sh /u/scratch/n/ninolee0/sncRNAseq/clip_fastq/ ${name}_clip
 
done


### move log file to mapping folder after changing name
cd /u/scratch/n/ninolee0/sncRNAseq/tophat2_masked_3rd_mapping
for file in *.log ; do
name=$(basename $file .log)
echo  $file ${name}_clip_tophat2_masked_3rd_output/
#ls ${name}_clip_tophat2_masked_3rd_output/

mv $file ${name}_clip_tophat2_masked_3rd.log
mv ${name}_clip_tophat2_masked_3rd.log ${name}_clip_tophat2_masked_3rd_output/

done


