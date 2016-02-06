<h2> 1. Convert OntoNotes gold file to CoNLL format</h2>
Parse OntoNotes coreference gold files and convert into CONLL 2011 shared task file format. Goal is to use the official scorer script for evaluating the coreferencer. 

Multiple gold files from the ./11docs/ directory will be read.Output will be one file, containing all docs under that directory. Each doc will begin with a comment #begin document ...

Note that due to restricted license on the OntoNotes and PennTreeBank, the actual documents will not be included here.

Usage:

to run it on a directory 11docs/ and write to one output file (11docs containing all ontoNotes gold .coref files): <br>
<code>python genConllGold.py -w 11docs/</code>

alternatively, to run it with a print option will take one file (.coref) as input and output the converted format into the stdout, for example:
<br><code>python genConllGold.py -p wsj_0120.coref</code>

(or to use -w in this case to write output to one file)

There is also a simple script, formatXML.py, to output the well formatted (indented) gold file as xml, for instance:

<code>$ python formatXML.py wsj_2321.coref >> wsj21.xml </code>

<h2> 2. Output OntoNotes gold file to html </h2>

Note: html file must be placed in the correct directory together with the javascript and css files for correct visualization of coreference.

Usage (take one input file and redirect the stdout to a file):

<code>$ python OntoToHtml.py 11docsonly/wsj_0120.coref >>html_ex/wsj_0120_gold.html</code>

if no redirection is used, currently will print html to stdout. To batch process all coref gold files in a directory, use the shell script provided, after modifying it to suit your directory name (below shows usage on UNIX bash):

<code> $ exec ./OntoConll.sh</code>


<h2> 3. Extract all book titles from the constituent parse tree files</h2>

This will output only unique titles existing in the text. 

Usage: 

(1) In "file" -f mode, extract and output (to stdout) all book titles from one .parse file, and redirect the output to a text file using:

<code>$ python extractTTL.py -f const_parses/wsj_0037.parse >> 0037_titles.txt</code>

(2) In "directory" -d mode, extract and output (to stdout) all book titles from all .parse files under the specified directory, and redirect the output to a text file using:

<code>$ python extractTTL.py -d const_parses/ >> all_titles.txt </code>

<h2> 4. More Preprocessing for OntoNotes gold files: nested markable removal and kill singleton (ref. sec.23 of wsj) </h2>

Nested markable is a markable inside another markable with the same ID. After the inner redundant markable is removed, we check if outter markable becomes a singleton - at which occasion we also remove the outter markable. This is in accordance with the OntoNotes coref guidelines. 

Example Usage:

<code> $ python rmNestKilSg.py wsj_2320.coref >> wsj_2320_new.coref </code>

To batch process, use the shell script (Bash on mac) after you've modified the input directory where all the original .coref gold files are located:

<code> $ exec ./fixNest.sh </code>


<h2> 5. Adding coref information to Stanford coreNLP conll output </h2>

Currently there is no easy way to output coref chains from dcoref using Stanford CoreNLP. You can output conll files using CoreNLP but there is no coref chain columns despite it is included in the list of annotators. Alternatively, by default you can output xml files from CoreNLP and it does contain coref chain info if it is indeed in the specified. In this task, we take both formats of output (.cnoll and .xml) and use a simple python script to add the coref chain info from the xml back to the conll files in the last column. Note that it takes plain text of OnteNotes files, one sentence per line, with the OnteNotes tokenization. 

Usage:

<code> $ python coreNLP_conll.py path/to/conll/file path/to/xml/file </code>

This will write output the complete conll file on the stdout. 

If you wish to do batch processing, i.e., read a directory of OntoNotes plain text files, then you can use the bash shell script provided:

<code> $ exec ./coreNLPConll.sh </code>

And this will write complete conll output for all documents into one output conll file, approprite for evaluation using the conll11,12 shared task scorer script. In the big output file, each document is marked by comments for beginning and ending of the document.
