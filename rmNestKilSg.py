from collections import defaultdict
import rmNest
import processGold as prep
from xml.dom import minidom
import sys
import xml.dom.minidom


def process(file):
    cf=prep.mainPreprocess(file)
    return cf

def kill_singleton(root,d):
    if root.childNodes:
        for node in root.childNodes:
            if node.nodeType == node.ELEMENT_NODE:
                key=node.attributes['ID'].value
                d[key]+=1
                #print key,d[key]
            kill_singleton(node,d)




def print_node_NoSgton(root,d):
    """traverse the entire xml DOM and print out without nested inner element tags with same IDs"""
    if root.childNodes:
        
        for node in root.childNodes:
            singleton=False
            #node is a tag with attribute
            if node.nodeType == node.ELEMENT_NODE:
                begin_tag,end_tag=rmNest.getTags(node)
                key=node.attributes['ID'].value
                if d[key]==1:
                    singleton=True
                else:
                    print begin_tag
                
            #node is plain text
            text=node.nodeValue
            if text:
                print text.strip()

            print_node_NoSgton(node,d)
            if singleton==False:
                if node.nodeType == node.ELEMENT_NODE:
                    #cid=node.attributes['ID'].value
                    print end_tag
                    
                    
def processRmNest(xmlfile):
    #xmldoc = minidom.parse(xmlfile)
    xmldoc=process(xmlfile)
    #get root tags and child of root tags
    root = xmldoc.documentElement
    rootn=root.childNodes[1]
    root_begin,root_end=rmNest.getTags(root)    
    rootn_begin,rootn_end=rmNest.getTags(rootn)
    a=" ".join(rmNest.NestRM(rootn))
    xml_rmNest="<doc>" + a + "</doc>"
    root_rmNest=xml.dom.minidom.parseString(xml_rmNest)
    rootn_rmNest=root_rmNest.firstChild
    return rootn_rmNest,root_begin,root_end,rootn_begin,rootn_end



#parse and print the body of html
xmlfile=sys.argv[1]
rootn_rmN,root_begin,root_end,rootn_begin,rootn_end=processRmNest(xmlfile)
d = {}
d = defaultdict(lambda: 0, d)
#update the dictionary of occurrences of IDs
kill_singleton(rootn_rmN,d)
#output without singletons
print root_begin
print rootn_begin
print_node_NoSgton(rootn_rmN,d)
print rootn_end
print root_end


