#!/bin/bash
for i in ptb/23/*.onf

do
	filename=$i

	#fpn="11docsonly/"$filename
	echo $filename
	#filename=$(basename "$fullfile")
	extension="${filename##*.}"
	firstname="${filename%.*}"
	newfile=$firstname".txt"
	echo $newfile
	#python processGold.py $filename | python ontoConvertConll.py - >> $newfile
	python onf2plain.py $filename >> $newfile 
done