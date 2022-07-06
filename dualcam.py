import time
import database as db
i = 0
def haha():
    while True:
        global i
        i+=1
        time.sleep(.5)
haha()
while True:
    print(i)
    db.kirim_masker(i)
    db.kirim_orang(i)

