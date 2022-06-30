import os
import time 
from time import sleep
from datetime import datetime

filename = datetime.now().strftime('data logger-%Y-%m-%d.csv')
file = open("data_log/{}".format(filename), "a")
i=0
if os.stat("data_log/{}".format(filename)).st_size == 0:
        file.write("Time,Sensor1,Sensor2,Sensor3,Sensor4,Sensor5\n")
while True:
    i=i+1
    now = datetime.now()
    file.write(str(now)+","+str(i)+","+str(-i)+","+str(i-10)+","+str(i+5)+","+str(i*i)+"\n")
    file.flush()
    time.sleep(5)