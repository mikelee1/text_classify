import os,time
for i in range(0,8):
    os.system('python3 predict.py split result'+str(i)+'.csv result'+str(i)+'.txt')
    time.sleep(10)
