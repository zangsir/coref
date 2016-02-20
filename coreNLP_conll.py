import sys
from coreNLP_modules import *
from xml.dom import minidom
from collections import defaultdict
from ontoConvertConll import mergeLabels
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
start_dict=get_start_dict(coref_info)
end_dict=get_end_dict(coref_info)

print '#begin document ' + coreNLP_conll_file.split('.')[0]
for row in doc_conll:
    row_list=row.split('\t')
    tup=(row_list[0],row_list[2])
    start,end=get_symbols(start_dict,end_dict,tup)
    #turn this on to debug and see if labels are merged right
    #print start,end
    coref_col=mergeLabels(start,end)
    row_list.append(coref_col)
    conll_list=[row_list[1],row_list[3],row_list[4]]
    print '\t'.join(conll_list)
print '#end document ' + coreNLP_conll_file.split('.')[0]
print '\n'
