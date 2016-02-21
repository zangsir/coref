# encoding=utf8

from xml.dom import minidom
import sys
from itertools import groupby
from operator import itemgetter
import re
#import xml.dom.minidom

#modified from print_node
def traverse_node_entity(root):
    """traverse the entire xml file recursively and output all tokens in order into a list"""
    output=[]
    if root.childNodes:
        for node in root.childNodes:
            if node.nodeType == node.ELEMENT_NODE:
                cid=node.attributes['ENTITY'].value
                output.append("("+cid)
            text=node.nodeValue
            if text:
                tokens=text.strip().split(" ")
                for tok in tokens:
                    if tok!=" " and tok!="":
                        output.append(tok)
            output.extend(traverse_node_entity(node)[:])
            if node.nodeType == node.ELEMENT_NODE:
                output.append(cid+")")
    return output
    
    
def groupPos(data):
    t=[]
    for k, g in groupby(enumerate(data), lambda (i, x): i-x):
        t.append(map(itemgetter(1), g))
    return t

def generateLabels(positions,mode,nlist):
    """given a list of positions (starts or ends) of all the tags of form '(123' or '123)', and mode=1 for starts, else for ends, return a list of labels to be inserted for all tokens the same length of nlist, the print out from xml"""
    posp=groupPos(positions)
    posp_item=[]
    for poss in posp:
        if len(poss)==1:
            posp_item.append(nlist[poss[0]])
        elif len(poss)>1:
            item="".join(nlist[i] for i in poss)
            posp_item.append(item)
    starts_tok=[]
    for pos in posp:
        if mode==1:
            ins=pos[-1]+1
        else:
            ins=pos[0]-1
        starts_tok.append(ins)    
    newlist=[[starts_tok[i],posp_item[i]] for i in range(len(posp))]
    stags=['_']*len(nlist)
    for i in newlist:
        stags[i[0]]=i[1]    
    return stags
    
    
    
#merge_entity_labels: one NE per line. 
def merge_entity_labels(x,y):
    if x=="_" and y=="_":
        newlabel="*"
    elif x=="_" and y!="_":
        newlabel='*' + ")"*y.count(')')
    elif x!="_" and y=="_":
        #mod_x=proc_slabel(x)
        #newlabel=''.join(mod_x)
        newlabel=x+'*'
    else:
        #both x and y has some label
        #y is not '_', so it must have some blah) form, so m is not None
        m=re.search(r'([a-zA-Z]+)(\).*)',y)
        n=re.search(r'(.*\()([a-zA-Z]+)',x)
        
        ele_x=set(x.split('('))
        ele_y=set(y.split(')'))
        if ele_x==ele_y and len(x)==len(y):
            #exactly one entity on this tok and of same length
            newlabel='('+x.split('(')[-1]+'*)'
        
        if len(x)>len(y):
            #likely: (animal(person  person) or (animal animal)person)
            if m.group(1)==n.group(2):
                #mod_x=proc_slabel(x)
                newlabel= x+ '*' + ")" * y.count(')')
            else:
                #(animal(object(person abstract)plant)
                newlabel=x + '*' + ")"*y.count(')')
        elif len(x)<len(y):
            if m.group(1)!=n.group(2):
                newlabel=x + '*' + ")"*y.count(')')
            else:
                #(animal animal)person)
                newlabel=x + '*' + ")" * y.count(')')
    return newlabel
    


def proc_slabel(l):
    """take a start label like (animal(object and return a list in a form of (animal*(object*"""
    ele=l.split('(')[1:]
    elements = ['('+element+'*' for element in ele]
    #final=''.join(elements)
    return elements





if __name__ == "__main__":
    xmlFile=sys.argv[1]
    xmlcon = minidom.parse(xmlFile) 
    root=xmlcon.childNodes[0]
    rootn=root.childNodes[1]
    rootn.childNodes[1].toxml()
    nlist=traverse_node_entity(rootn)
    outputFormat=[]
    starts=[]
    for i in range(len(nlist)):
        if re.search(r'\([a-zA-Z]+[^\)]',nlist[i]):
            starts.append(i)
    ends=[]
    for i in range(len(nlist)):
        if re.search(r'[^\(][a-zA-Z]+\)',nlist[i]):
            ends.append(i)
    st=generateLabels(starts,1,nlist)
    ed=generateLabels(ends,-1,nlist)
    

    #debug
    #print nlist
    #for i in range(len(st)):
    #    print i,nlist[i], st[i],"|",ed[i],"|",merge_entity_labels(st[i],ed[i])
    #print "="*20
    
    counter=0
    stack=[]
    outputFormat=[]

    for i in range(len(nlist)):
        no_output=re.search(r'\([a-zA-Z]+[^\)]|[^\(][a-zA-Z]+\)',nlist[i])
        if not no_output:
            merged=merge_entity_labels(st[i],ed[i])
            #print nlist[i],st[i],ed[i],merged
            tok=str(counter)+"\t"+nlist[i]+"\t"+merged
            outputFormat.append(tok)
            counter+=1
        
    for i in outputFormat:print i.encode('utf-8')

    #print starts
