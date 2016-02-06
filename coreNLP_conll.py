from xml.dom import minidom
import sys
from collections import defaultdict
from ontoConvertConll import mergeLabels

def get_start_dict(coref_info):
    start_dict=defaultdict(str)
    start_dict_dup=defaultdict(str)
    for coref_line in coref_info:
        tup=(coref_line[1],coref_line[2])
        if start_dict[tup]=='':
            start_dict[tup]=coref_line[0]
        else:
            start_dict_dup[tup]=coref_line[0]
            #print 'duplicate position',tup
    return start_dict,start_dict_dup
    

def get_end_dict(coref_info):
    end_dict=defaultdict(str)
    end_dict_dup=defaultdict(str)
    for coref_line in coref_info:
        tup=(coref_line[1],str(int(coref_line[3])-1))
        if end_dict[tup]=='':
            end_dict[tup]=coref_line[0]
        else:
            end_dict_dup[tup]=coref_line[0]
            #print 'duplicate position',tup
    return end_dict,end_dict_dup
    
    
    
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


def get_symbols(start_dict,start_dict_dup,end_dict,end_dict_dup,tup):
    if start_dict[tup]!='' and start_dict_dup[tup]!='':
        start_sym=('('+start_dict[tup]+'('+start_dict_dup[tup])
    elif start_dict[tup]!='':
        start_sym=('('+start_dict[tup])
    elif start_dict_dup[tup]!='':
        start_sym=('('+start_dict_dup[tup])
    else:
        start_sym=('_')
        
    if end_dict[tup]!='' and end_dict_dup[tup]!='':
        end_sym=(end_dict[tup]+')'+end_dict_dup[tup]+')')
    elif end_dict[tup]!='':
        end_sym=(end_dict[tup]+')')
    elif end_dict_dup[tup]!='':
        end_sym=(end_dict_dup[tup]+')')
    else:
        end_sym=('_')
    return start_sym,end_sym
    
    
    
    
    
#####################################main usage
coreNLP_conll_file=sys.argv[1]
dcoref_xml_file=sys.argv[2]

#process coreNLP output conll file without coref info
#f=open('wsj_2320_coreNLP.conll','r')
#name: wsj_2320_cnlp.conll, wsj_2320_cnlp.xml
f=open(coreNLP_conll_file,'r')
out=f.read()
outline=out.split('\n')
doc_conll=get_doc_conll(outline)

#process coref info from coreNLP xml output
#xmlfile="coreNLP_out.xml"
xmlfile=dcoref_xml_file
xmldoc = minidom.parse(xmlfile)
coref_list=xmldoc.getElementsByTagName('coreference')
coref_info=get_coref_info(coref_list)

#putting them together
start_dict,start_dict_dup=get_start_dict(coref_info)
end_dict,end_dict_dup=get_end_dict(coref_info)

print '#begin document ' + coreNLP_conll_file.split('.')[0]
for row in doc_conll:
    row_list=row.split('\t')
    tup=(row_list[0],row_list[2])
    start,end=get_symbols(start_dict,start_dict_dup,end_dict,end_dict_dup,tup)
    #turn this on to debug and see if labels are merged right
    #print start,end 
    coref_col=mergeLabels(start,end)
    row_list.append(coref_col)
    conll_list=[row_list[1],row_list[3],row_list[4]]
    print '\t'.join(conll_list)
print '#end document ' + coreNLP_conll_file.split('.')[0]
print '\n'