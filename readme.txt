Parse OntoNotes coreference gold files and convert into CONLL 2011 shared task file format. Goal is to use the official scorer script for evaluating the coreferencer. 

Multiple gold files from the ./11docs/ directory will be read.Output will be one file, containing all docs under that directory. Each doc will begin with a comment #begin document ...

Usage:
#to run it on a directory 11docs/ and write to one output file:
python genConllGold.py -w 11docs/

#alternatively, to run it with a print option will take one file (.coref) as input and output the converted format into the stdout, for example:
python genConllGold.py -p wsj_0120.coref
