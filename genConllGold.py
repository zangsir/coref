#main script for generating gold response files of OntoNOtes 5 from the coref files. write to one file for all docs in directory. need 2 args: modes (-p or -w) and file name if p, dir name if w
import ontoConvertConll as onto
import processGold as prep
import sys,os
from os import listdir

#two modes:-p=print, -w=write
mode=sys.argv[1]
inputname=sys.argv[2]

newfile="ontoGoldAll.response"
g=open(newfile,"w")
g.close()

def process(file):
    cf=prep.mainPreprocess(file)
    output=onto.mainOutput(cf)
    return output
    
#if a directory, process every file and write to one big file. in this mode, we don't write to a single file, simple always append to a file
def writeOneFile(output, outName, firstname):
    """input is the formated list from process() function. then append to a file."""
    g=open(outName,"a")
    header="\n# begin document "+ firstname +"\n"
    g.write(header)
    for line in output:
        g.write(line+'\n')
    g.close()

#single file mode, print to console, or use shell to redirect to a file
if os.path.isfile(inputname):
    firstname=inputname.split(".")[0]
    outlist=process(inputname)
    if mode=="-p":
        print '\n'
        print "# begin document "+ firstname +"\n"
        for i in outlist:
            print i
    elif mode=="-w":
        writeOneFile(outlist,firstname+'_gold.response')

    
#directory mode main: append all outputs to one file    
if os.path.isdir(inputname):
    onlyfiles = [ f for f in listdir(inputname) if f.endswith(".coref")]
    for file in onlyfiles:
        firstname=file.split(".")[0]
        tfile=inputname+file
        outlist=process(tfile)
        writeOneFile(outlist,newfile,firstname)