import sys,re

def onf2plain(onf):
    """takes a ptb onf file as input and outputs plain text"""
    pattern="""Plain sentence:\n---------------"""
    nextpat="""Treebanked sentence:"""
    plain_sect=[(m.start(0), m.end(0)) for m in re.finditer(pattern, onf)]
    next_sect=[(m.start(0), m.end(0)) for m in re.finditer(nextpat, onf)]
    for i in range(len(plain_sect)):
        start=plain_sect[i][1]
        end=next_sect[i][0]
        print onf[start:end].replace("\n",""),
        
        
onf_file=sys.argv[1]
f=open(onf_file,"r")
input_text=f.read()
onf2plain(input_text)