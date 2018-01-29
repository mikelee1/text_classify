import os,time
for i in range(11,40):
    os.system('python3 predict.py split result'+str(i)+'.csv result'+str(i)+'.txt')
    time.sleep(10)
