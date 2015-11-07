#!/bin/bash
for i in 11docsonly/*.coref

do
	filename=$i

	#fpn="11docsonly/"$filename
	echo $filename
	#filename=$(basename "$fullfile")
	extension="${filename##*.}"
	firstname="${filename%.*}"
	newfile=$firstname"_gold.html"
	echo $newfile
	#python processGold.py $filename | python ontoConvertConll.py - >> $newfile
	python OntoToHtml.py $filename >> $newfile 
done