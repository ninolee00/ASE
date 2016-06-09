#!/bin/bash

# run filter_ase4PAR.py

PATH=$PATH:/u/project/eeskin/geschwind/ninolee0/bin  ### samtools location
export PATH
PATH=$PATH:/u/project/eeskin/geschwind/ninolee0/bin/program/  ### homemade program location
export PATH

ROOT=$1  # header_part_aa: product of " split -1000000 all_no_bias_sam_order4sncRNAseq_header.ase header_part_ "
present=$2
good=$3


echo
echo "###############################"
echo "#### run filter_ase4PAR.py ####"
echo "###############################"
echo
echo ${ROOT} ${present} ${good}
date
echo

filter_ase4PAR.py ${ROOT} ${present} ${good} > ${ROOT}_${present}_${good}_check

echo
echo "#####################################"
echo "### filter_ase4PAR.py process end ###"
echo "#####################################"
date
echo

