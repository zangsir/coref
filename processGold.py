import re,sys
import xml.dom.minidom

def printToFile(content,filename):
    firstname=filename.split(".")[0]
    newname=firstname+"_cl.coref"
    f = open(newname, 'w')
    f.write(content)
    f.close()


def removeEmptyCat(filename):
 	
    f = open(filename, 'r')
    raw=f.read()
    insBefore=addNewlineBefore(raw)
    insAfter=addNewlineAfter(insBefore)
        
    tokens = re.split(' |\n',insAfter)   
    new=""
    for tok in tokens:
        star=re.search(r"(^|[^\\])\*",tok)
        if not star and tok!="0":
            new=new+" "+tok
            
    return new


def addNewlineBefore(text):
    tokens=text.split("<")
    new=""
    for tok in tokens[1:]:
        new=new+"\n"+"<"+tok
    return new

def addNewlineAfter(text):
    #same approach to add a \n after >
    tokens=text.split(">")
    new=""
    for tok in tokens:
        new=new+tok+">"+"\n"
    return new

def mainPreprocess(filen):
    """preprocess OntoNotes gold files by cleaning up the empty categories and more"""
    #filen=sys.argv[1]
    noemp=removeEmptyCat(filen)
    noempi=noemp[:-2]
    a=xml.dom.minidom.parseString(noempi)
    #to use this module to output a formatted xml for viewing, do:
    #pretty_xml_as_string = a.toprettyxml()
    #print pretty_xml_as_string
    return a
