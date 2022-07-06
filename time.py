from time import time, sleep
from datetime import datetime

while True:
    waktu = datetime.now().strftime('%S')
    print(waktu)
    if (datetime.now().minute % 1 == 0):
        print("10 detik berlalu")
    sleep(1)
    