#!/bin/bash
for i in coref23/*.coref

do
	filename=$i

	#fpn="11docsonly/"$filename
	echo $filename
	#filename=$(basename "$fullfile")
	extension="${filename##*.}"
	firstname="${filename%.*}"
	newfile=$firstname"_rmNest.coref"
	echo $newfile
	#python processGold.py $filename | python ontoConvertConll.py - >> $newfile
	python rmNestKilSg.py $filename >> $newfile 
done