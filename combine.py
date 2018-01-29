
import pandas as pd
import os
import numpy as np
def handler(dirname):
    filelist = os.listdir(dirname)
    tmpdf = pd.DataFrame(columns = ['album_id','category_id','title','sub_category'])
    for i in filelist:
        if 'txt' in i:
            print(i)
            a = pd.read_table(dirname+'/'+i,sep = ',')
            tmpdf = tmpdf.append(a)
    return tmpdf
    #os.system('cd '+dirname+' && python3 predict.py split result.csv result.txt')




index = os.listdir('.')
indexlist = []
for i in index:
    tmp = i.split('_')
    if os.path.isdir(i) and len(tmp)==3:
        indexlist.append(int(tmp[-1]))
tmpdf = pd.DataFrame(columns = ['album_id','category_id','title','sub_category'])
for j in indexlist:
    handlerdir = 'text_classify_'+str(j)
    tmpdf=tmpdf.append( handler(handlerdir))
print(tmpdf.dtypes)
tmpdf.album_id = tmpdf.album_id.astype(int)
tmpdf.category_id = tmpdf.category_id.astype(int)

tmpdf.to_csv('result.txt',index = False)
