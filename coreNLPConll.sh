#!/bin/bash
for i in coreNLPConll/*.conll

do
	filename=$i
	echo $filename
	#filename=$(basename "$fullfile")
	extension="${filename##*.}"
	firstname="${filename%.*}"
	xmlfile=$firstname".xml"
	newfile=$firstname"_dcoref.conll"
	echo $newfile
	#python processGold.py $filename | python ontoConvertConll.py - >> $newfile
	python coreNLP_conll.py $filename $xmlfile >> $newfile 
done