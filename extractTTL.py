import sys,os
from os import listdir
import re


mode=sys.argv[1]
inputname=sys.argv[2]


def preprocPTB(out):
    out=out.replace("  ", "")
    out=out.replace("\n", " ")
    return out


def parseParen(string):
    """#use a stack to parse matching brackets"""
    stack = []
    for i, c in enumerate(string):
        if c == '(':
            stack.append(i)
        elif c == ')' and stack:
            start = stack.pop()
            yield (len(stack), string[start + 1: i])




def findTitle(string):
    """find the end; input is the string that starts at the first parenthesis before the TTL till the end of the file """
    stack = []
    for i, c in enumerate(string):
        if c == '(':
            stack.append(i)
        elif c == ')' and stack:
            start = stack.pop()
            if len(stack) == 0:
                return string[start + 1: i]
            

def findLastParen(fp):
    parens=[(m.start(0), m.end(0)) for m in re.finditer("\(", fp)]
    return parens[-1][0]


def outputTitle(truelist):
    """given the list of """
    output=[]
    for unit in truelist:
        #unit is of format (2, 'NNP Wild'),where 2 is the len(stack)
        core=unit[1]
        tokpos=core.split()
        #tokpos is of format 'NNP Wild'
        if len(tokpos) == 2:
            tok = tokpos[1]
            output.append(tok)
    final=" ".join(output)        
    return final
    
    
def procTTL(ttl,docp):
    """given the tuple of -TTL position, and the preprocessed doc text, return the final clean title"""
    #ttl holds the position of the "-TTL" pattern in doc, such as (197,201)
    tstart=ttl[0]
    pstart=findLastParen(docp[:tstart])
    title=findTitle(docp[pstart:])
    if not re.search("\*",title):
        titlep="(" + title + ")"
        truelist=parseParen(titlep)
        outTTL=outputTitle(truelist)
        return outTTL


def procFile(fileName):
    f = open(fileName, 'r')
    doc=f.read()
    f.close()
    docp=preprocPTB(doc)
    ttls=[(m.start(0), m.end(0)) for m in re.finditer("-TTL", docp)]
    all_titles=[]
    for ttl in ttls:
        out=procTTL(ttl,docp)
        if out not in all_titles and out!=None:
            all_titles.append(out)
    for ttl in all_titles:
        print ttl        

#main

if mode=="-f" and os.path.isfile(inputname):
    procFile(inputname)
        
if mode=="-d" and os.path.isdir(inputname):
    onlyfiles = [ f for f in listdir(inputname) if f.endswith(".parse")]
    #print onlyfiles
    for fileName in onlyfiles:
        procFile(inputname+fileName)
