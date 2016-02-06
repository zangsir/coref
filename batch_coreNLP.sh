#!/bin/bash
for i in sec23_plain/*.txt

do
	filename=$i
	echo $filename
	#filename=$(basename "$fullfile")
	#extension="${filename##*.}"
	#firstname="${filename%.*}"
	#xmlfile=$firstname".xml"
	#newfile=$firstname"_dcoref.conll"
	#echo $newfile
	java -Xmx3g -cp stanford-corenlp-3.6.0.jar:stanford-corenlp-models-3.6.0.jar:* edu.stanford.nlp.pipeline.StanfordCoreNLP -annotators tokenize,ssplit,pos,lemma,ner,parse,dcoref -outputFormat xml  -tokenize.whitespace true -ssplit.eolonly true -dcoref.postprocessing true -file $filename -dcoref.use.big.gender.number true
	
     

	
done


# annotators needed for coreference resolution
#annotators = pos, lemma, ner, parse    

# Scoring the output of the system. 
# Scores in log file are different from the output of CoNLL scorer because it is before post processing.
#dcoref.score = true                    

                                       
# Do post processing
#dcoref.postprocessing = true           
# Maximum sentence distance between two mentions for resolution (-1: no constraint on the distance)
#dcoref.maxdist = -1                    
# Load a big list of gender and number information
#dcoref.use.big.gender.number = true    
#dcoref.big.gender.number = edu/stanford/nlp/models/dcoref/gender.data.gz
# Turn on this for replicating conllst result
#dcoref.replicate.conll = true        

#java -Xmx3g -cp stanford-corenlp-3.6.0.jar:stanford-corenlp-models-3.6.0.jar:* edu.stanford.nlp.pipeline.StanfordCoreNLP -annotators tokenize,ssplit,pos,lemma,ner,parse,dcoref -file example_file.txt

#with dcoref options
#java -Xmx3g -cp stanford-corenlp-3.6.0.jar:stanford-corenlp-models-3.6.0.jar:* edu.stanford.nlp.pipeline.StanfordCoreNLP -annotators tokenize,ssplit,pos,lemma,ner,parse,dcoref -outputFormat xml  -tokenize.whitespace true -ssplit.eolonly true -dcoref.postprocessing true -file input.txt -dcoref.use.big.gender.number true

#original:
#java -Xmx3g -cp stanford-corenlp-3.6.0.jar:stanford-corenlp-models-3.6.0.jar:* edu.stanford.nlp.pipeline.StanfordCoreNLP -annotators tokenize,ssplit,pos,lemma,ner,parse,dcoref -outputFormat xml  -tokenize.whitespace true -ssplit.eolonly true -dcoref.postprocessing true -dcoref.maxdist -1 -dcoref.use.big.gender.number true -file $filename