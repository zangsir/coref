<h2> 1. Convert OntoNotes gold file to CoNLL format</h2>
Parse OntoNotes coreference gold files and convert into CONLL 2011 shared task file format. Goal is to use the official scorer script for evaluating the coreferencer. 

Multiple gold files from the ./11docs/ directory will be read.Output will be one file, containing all docs under that directory. Each doc will begin with a comment #begin document ...

Note that due to restricted license on the OntoNotes and PennTreeBank, the actual documents will not be included here.

Usage:
to run it on a directory 11docs/ and write to one output file (11docs containing all ontoNotes gold .coref files): <br>
<code>python genConllGold.py -w 11docs/</code>

alternatively, to run it with a print option will take one file (.coref) as input and output the converted format into the stdout, for example:
<br><code>python genConllGold.py -p wsj_0120.coref</code>

<h2> 2. Output OntoNotes gold file to html </h2>

Note: html file must be placed in the correct directory together with the javascript and css files for correct visualization of coreference.

Usage (take one input file and redirect the stdout to a file):

<code>$ python OntoToHtml.py 11docsonly/wsj_0120.coref >>html_ex/wsj_0120_gold.html</code>

if no redirection is used, currently will print html to stdout
