from xml.dom import minidom
from collections import defaultdict
from ontoConvertConll import mergeLabels

def get_start_dict(coref_info):
    start_dict=defaultdict(list)
    for coref_line in coref_info:
        tup=(coref_line[1],coref_line[2])
        start_dict[tup].append(coref_line[0])
    return start_dict
    

def get_end_dict(coref_info):
    end_dict=defaultdict(list)
    for coref_line in coref_info:
        tup=(coref_line[1],str(int(coref_line[3])-1))
        end_dict[tup].append(coref_line[0])
    return end_dict
    
    
    
#outline is the original conll file from coreNLP output without coref info
def get_doc_conll(outline):
    count=0
    sent_count=1
    doc_conll=[]
    for line in outline:
        tok_id=str(count)
        if line!="\r" and line!='' and line!=' ':
            this_line=str(sent_count) + "\t" + tok_id + '\t' + line.split('\t')[0] + '\t' + line.split('\t')[1]
            #print this_line
            doc_conll.append(this_line)
            count+=1
            #print count

        #elif line=='\r' or line=='' or line==' ':
        else:
            #this_line=str(sent_count) + '\t' + tok_id + '\t' + line
            #print this_line
            sent_count+=1
            #doc_conll.append(this_line)
        
    return doc_conll
    
    
def get_coref_info(coref_list):
    coref_info=[]
    group_num=0
    for i in range(1,len(coref_list)):
        group=coref_list[i]
        group_num+=1
        marks=group.getElementsByTagName('mention')
        for j in range(len(marks)):
            sentence=group.getElementsByTagName('sentence')[j]
            sent_num=sentence.childNodes[0].toxml()
            start=group.getElementsByTagName('start')[j]
            start_num=start.childNodes[0].toxml()
            end=group.getElementsByTagName('end')[j]
            end_num=end.childNodes[0].toxml()
            #print group_num,sent_num,start_num,end_num
            coref_info.append([str(group_num),str(sent_num),str(start_num),str(end_num)])
    return coref_info


def get_symbols(start_dict,end_dict,tup):
    if start_dict[tup]!=[]:
        groups=start_dict[tup]
        start_sym=''
        for num in groups:
            start_sym = start_sym + '(' + num
    else:
        start_sym=('_')

    if end_dict[tup]!=[]:
        groups=end_dict[tup]
        end_sym=''
        for num in groups:
            end_sym=end_sym+num+')'
    else:
        end_sym=('_')
    return start_sym,end_sym
    
    
    
    
    