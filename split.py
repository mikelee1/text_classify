
import pandas as pd
import os

def handler(dirname,df):
    df.to_csv(dirname+'/result.csv',index=False)
    #os.system('cd '+dirname+' && python3 predict.py split result.csv result.txt')




df = pd.read_table('sources.csv',sep=',')
index = os.listdir('.')
indexlist = []
for i in index:
    tmp = i.split('_')
    if os.path.isdir(i) and len(tmp)==3:
        indexlist.append(int(tmp[-1]))
print(indexlist)
for j in indexlist:
    handlerdir = 'text_classify_'+str(j)
    handlerdf = df[df.category_id == j]
    if handlerdf.size!=0:
        handler(handlerdir,handlerdf)
        print(j)

