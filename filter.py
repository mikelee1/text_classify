import csv
file_in = 'cnews.test.txt'

# ##获取前N列，并将数据写入新的文件

with open(file_in, 'r') as csvfile:

    reader = csv.reader(csvfile)

    rows = [row[:2] for row in reader if row]

    # print rows
lis = []
#writer = csv.writer(open(file_out, 'w'))
f = open('result.txt','w')
for row in rows:
    #if row[0] not in lis:
        #lis.append(row[0])
    if len(row)==2:
        row.insert(1,'\t')
        row.append('\tintroductions\n')
        writer.writerow(row)
        a=''.join(row)
        f.write(a)
#print(lis)
