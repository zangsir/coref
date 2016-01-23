import processGold as prep
from xml.dom import minidom
import sys,re

#this module contains several methods with slight variations, as utilities

def getTags(node):
    #get tag name, list of attributes
    tagName=node.tagName
    attrs=sorted(node.attributes.keys())
    if 'ID' in attrs:
        cid=node.attributes['ID'].value
        newcid=re.sub(r'wsj_([0-9]+).*-[A-Z]([0-9])',r'\1\2',cid)
        node.setAttribute('ID',newcid)
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
                    

def NestRM(root):
    """traverse the entire xml DOM and return the xml without nested elements with same IDs as a list"""
    output=[]
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
                    output.append(begin_tag)
                
            #node is plain text
            text=node.nodeValue
            if text:
                output.append(text.strip())

            output.extend(NestRM(node)[:])
            if nest_node==False:
                if node.nodeType == node.ELEMENT_NODE:
                    #cid=node.attributes['ID'].value
                    output.append(end_tag)
    return output
    
    
#simply output everything (including tags) generically
def print_node_NestRM(root):
    """traverse the entire xml DOM and print out everything in order  (including tags)"""
    if root.childNodes:
        
        for node in root.childNodes:
            #node is a tag with attribute
            if node.nodeType == node.ELEMENT_NODE:
                begin_tag,end_tag=getTags(node)
                print begin_tag
                
            text=node.nodeValue
            #node is plain text
            if text:
                print text.strip()
            print_node_NestRM(node)
            if node.nodeType == node.ELEMENT_NODE:
                #cid=node.attributes['ID'].value
                print end_tag
    

