## correction of clip_fastq
Sample_directory	Sample	Brain.ID	Region	fastq	clip_fastq	unmapped_read	uniquely_mapped_read
Sample_AN01971_ba9_1st	AN01971_ba9_1st	AN01971	ba9	9962164	7653976	97837	406839
--> 
Sample_AN01971_ba9_1st	AN01971_ba9_1st	AN01971	ba9	9962164	8895789	97837	406839

Sample_AN14757_ba9_2nd	AN14757_ba9_2nd	AN14757	ba9	9903500	6964309	421036	1711943
--> 
Sample_AN14757_ba9_2nd	AN14757_ba9_2nd	AN14757	ba9	9903500	8216944	421036	1711943


### correct the info for metaData_mine.txt, metaData_mine_final.csv, metaData_mine_final.txt
mv metaData_mine.txt metaData_mine.txt_1
mv metaData_mine_final.csv metaData_mine_final.csv_1
mv metaData_mine_final.txt metaData_mine_final.txt_1

sed 's/7653976/8895789/g' metaData_mine.txt_1 | sed 's/6964309/8216944/g' > metaData_mine.txt 
sed 's/7653976/8895789/g' metaData_mine_final.csv_1 | sed 's/6964309/8216944/g' > metaData_mine_final.csv 
sed 's/7653976/8895789/g' metaData_mine_final.txt_1 | sed 's/6964309/8216944/g' > metaData_mine_final.txt

rm *_1


