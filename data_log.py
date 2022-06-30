import os
import time 
from datetime import datetime

filename = datetime.now().strftime('data logger-%Y-%m-%d.csv')
file = open("data_log/{}".format(filename), "a")
i=0
if os.stat("data_log/{}".format(filename)).st_size == 0:
        file.write("Waktu,Pengunjung,Pelanggar Masker,Keterangan\n")
while True:
    i=i+1
    now = datetime.now()
    if (datetime.now().second % 5 == 0):
        file.write(str(now.strftime("%H:%M:%S"))+","+str(i)+","+str(-i)+","+str(i-10)+"\n")
        file.flush()
        time.sleep(1)

    print(now)
    time.sleep(.2)
