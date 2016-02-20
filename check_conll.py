import sys,re,glob



def read_files(file):
    f=open(file,'r')
    doc=f.read()
    doc_all=doc.split('\n')
    return doc_all
    
    


def check_conll(doc_a,doc_b):
    min_len=min(len(doc_a),len(doc_b))
    for i in range(1,min_len):
        line_a=doc_a[i].split('\t')
        line_b=doc_b[i].split('\t')
        #print line_a[0],line_b[0]
        if len(line_a)>1 and len(line_b)>1:
            if line_a[1]!=line_b[1]:
                print i,line_a,line_b
            
  
  
conlls=glob.glob('*.conll')
gconlls=glob.glob('*.gold_conll')

for file in conlls:
    first_name=file.split('.')[0]
    gc=first_name+'.gold_conll'
    if gc in gconlls:
        print file
        doc_a=read_files(file)
        doc_b=read_files(gc)
        check_conll(doc_a,doc_b)
    print '========================'
    
    

