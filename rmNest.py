import processGold as prep
from xml.dom import minidom
import sys

def process(file):
    cf=prep.mainPreprocess(file)
    return cf

def getTags(node):
    #get tag name, list of attributes
    tagName=node.tagName
    attrs=sorted(node.attributes.keys())
    #node.attributes[attr[1]].value
    print_attrs=''
    for attr in attrs:
        addon=attr+'="'+node.attributes[attr].value+'"'
        print_attrs = print_attrs+addon+" "
    begin_tag="<" + tagName + " " + print_attrs + ">"
    end_tag="</" + tagName + ">"
    return begin_tag,end_tag

def print_node_NestRM(root):
    """traverse the entire xml DOM and print out without nested inner element tags with same IDs"""
    if root.childNodes:
        
        for node in root.childNodes:
            nest_node=False
            #node is a tag with attribute
            if node.nodeType == node.ELEMENT_NODE:
                begin_tag,end_tag=getTags(node)
                #print "begin_tag:",begin_tag
                #print node.toxml()+">>>>>>>>>>"
                if root.hasAttribute('ID') and node.attributes['ID'].value == root.attributes['ID'].value:
                    nest_node=True
                    #print 'found nested markable------------------------'
                    #print node.firstChild.data

                else:
                    print begin_tag
                
            #node is plain text
            text=node.nodeValue
            if text:
                print text.strip()

            print_node_NestRM(node)
            if nest_node==False:
                if node.nodeType == node.ELEMENT_NODE:
                    #cid=node.attributes['ID'].value
                    print end_tag
                    



#parse and print the body of html
xmlfile=sys.argv[1]
#xmldoc = minidom.parse(xmlfile)
xmldoc=process(xmlfile)
#get root tags and child of root tags
root = xmldoc.documentElement
rootn=root.childNodes[1]
root_begin,root_end=getTags(root)    
rootn_begin,rootn_end=getTags(rootn)

print root_begin
print rootn_begin
print_node_NestRM(rootn)
print rootn_end
print root_end