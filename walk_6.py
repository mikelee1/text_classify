
import os

files = os.listdir('.')
a = []
for i in files:
    b = i.split('_')
    if os.path.isdir(i) and len(b)==3 and int(b[-1])>=9:
        a.append(b[-1])
print(a)
for i in a:
    print(i)
    os.chdir('text_classify_'+i)
    c = os.listdir('.')
    if 'result0.csv' in c:
        os.system('python3 line.py')
    else:
        os.system('python3 predict.py split result.csv result.txt')
    os.chdir('../')
