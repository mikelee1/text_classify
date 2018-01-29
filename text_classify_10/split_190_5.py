import pandas as pd
import math
df = pd.read_table('result.csv',sep=',')
total = int(df.size/4)
num = math.ceil(total/50000)
print(num)
for i in range(num):
    start = 50000*i
    if i == num-1:
        a = df.iloc[start:,:]
    else:
        a = df.iloc[start:min(start+50000,total),:]
    a.to_csv('result'+str(i)+'.csv',index=False)
    #print(a.groupby(a.category_id).size())
