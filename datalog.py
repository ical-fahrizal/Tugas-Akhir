import pyrebase
from datetime import datetime
import datetime
from time import sleep
import random
import schedule

ruang = 'ruang 2'

firebaseConfig={
    "apiKey": "AIzaSyDJyOXSmlLxdfBxq62roooDuark18dUgIs",
    "authDomain": "tugas-akhir-630e4.firebaseapp.com",
    "databaseURL": "https://tugas-akhir-630e4-default-rtdb.firebaseio.com",
    "projectId": "tugas-akhir-630e4",
    "storageBucket": "tugas-akhir-630e4.appspot.com",
    "messagingSenderId": "923707090227",
    "appId": "1:923707090227:web:9a10e5631c5481a4060a46",
    'measurementId': "G-CVJ765P95K"
}

firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()



while True:
    time = datetime.datetime.now()

    waktu_sekarang = time.strftime("%H:%M")
    tanggal_sekarang = datetime.date.today()
    datalog= {
        "masker":random.randint(0,1), 
        "orang":random.randint(2,5)
    }

    print(waktu_sekarang)
    print(tanggal_sekarang)

    def kirim_log():
        return db.child("datalog").child(tanggal_sekarang).child(waktu_sekarang)
    a = kirim_log()
    a.set(datalog)
    sleep(60)


    