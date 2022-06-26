from playsound import playsound
import database as db
import os
import time

#os.system(./run.sh) #nanti di aktivin ketika di raspi

batas_orang = db.batas_orang()
jumlah_orang = db.jumlah_orang()
pelanggar_masker = db.pelanggar_masker()

while True:
    #status pada jumlah orang 
    if jumlah_orang >= batas_orang:
        print('melebihi batas')
    else:
        print('aman')

    #peringatan pelanggar masker 
    if pelanggar_masker >= 1:
        print('terdapat pelanggar masker')
        # playsound('masker.mp3')
    else:
        print('tidak ada pelanggar masker')
    
    time.sleep(.5)
    
