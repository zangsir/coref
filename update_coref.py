import glob





def read_files(file):
    f=open(file,'r')
    doc=f.read()
    doc_all=doc.split('\n')
    return doc_all

def doc_clean(pred,coref):
    count_pred=0
    pred_clean=[]
    for line in pred:
        if line!='' and not line.startswith('#'):
            pred_clean.append(line)
            count_pred+=1
    
    
    count_coref=0
    coref_clean=[]
    for line in coref:
        if line!='' and not line.startswith('#'):
            coref_clean.append(line)
            count_coref+=1
    #print count_pred,count_coref
    return count_pred,count_coref,pred_clean,coref_clean


def update_coref(pred,coref):
    a,b,cpred,ccoref=doc_clean(pred,coref)
    count=0
    new_doc=[]
    if a==b:
        for i in range(len(cpred)):
            l=cpred[i].split('\t')
            lc=ccoref[i].split('\t')
            l[-1]=lc[-1]
            #print count,l
            t=[str(count)]
            t.extend(l[:])
            new_doc.append(t)
            count+=1
    return new_doc
    

def update_ner(pred,ner):
    a,b,cpred,cner=doc_clean(pred,ner)
    count=0
    new_doc=[]
    if a==b:
        for i in range(len(cpred)):
            l=cpred[i].split('\t')
            lc=cner[i].split('\t')
            l[-2]=lc[-1]
            
            #print count,l
            t=[str(count)]
            t.extend(l[:])
            new_doc.append(t)
            count+=1
    return new_doc

def write_file(output_list,fname,mode):
    """mode==gold or auto"""
    out_dic={'gold':'.gold_conll','auto':'.auto_conll'}
    extname=out_dic[mode]
    outname=fname + extname
    f=open(outname,'w')
    begin= "#begin document (" + outname + ".txt); part 000"
    end="#end document"
    f.write('\n' + begin + '\n')
    f.close()

    for line in output_list:
        str_line='\t'.join(line)
        f=open(outname,'a')
        f.write(str_line+'\n')
        f.close()
    f=open(outname,'a')
    f.write(end)
    f.close()

def update_gold_coref(auto_output,gold_output_tmp):
    for i in range(len(auto_output)):
        line_auto=auto_output[i]#gold coref 
        line_gtmp=gold_output_tmp[i]#gold ner
        #want gold_ner+gold_coref
        line_gtmp[-1]=line_auto[-1]
    return gold_output_tmp
    

if __name__ == "__main__":
    pred_conlls=glob.glob('gum-coref/*.pred_conll')
    #gconlls=glob.glob('*.gold_conll')
    test_files=[]
    for name in pred_conlls:
        f=name.split('.')[0].split('/')[1]
        test_files.append(f)
    
    for i in range(len(pred_conlls)):
        fname=test_files[i]
        print fname
        pred_file=pred_conlls[i]
        ner_file='gum-ner-gold/'+ fname +'.gold_conll'
        coref_file='gum-ner-gold/' + fname + '.conll'
        pred=read_files(pred_file)
        coref=read_files(coref_file)
        ner=read_files(ner_file)
        auto_output=update_coref(pred,coref)
        #add update_ner function
        gold_output_tmp=update_ner(pred,ner)
        gold_output=update_gold_coref(auto_output,gold_output_tmp)
        #write auto,gold outputs for this parse file
        write_file(gold_output,fname,'gold')
        write_file(auto_output,fname,'auto')
    
    
    
    
    