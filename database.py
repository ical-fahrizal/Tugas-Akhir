import pyrebase
from datetime import datetime

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
storage = firebase.storage()
filename = datetime.now().strftime('data logger-%Y-%m-%d.csv')

path_on_cloud = "data_log/test.csv"
path_local = "data_log/data logger-2022-06-30.csv"

storage.child(path_on_cloud).put(path_local)

#kirim file 
# def kirim_file():
#     storage.child(path_on_cloud).put(path_local)

#kirim data pelanggar masker 
def kirim_masker(masker):
    db.child(ruang).update({'pelanggar masker' : masker}) #mengupdate value pelanggar masker

#kirim data jumlah orang 
def kirim_orang(orang):
    db.child(ruang).update({'jumlah orang' : orang })

#mendapatkan data batas orang
def batas_orang():
    batas = db.child(ruang).child('batas orang').get() #mendapatkan data dari batas orang
    return batas.val()

#mendapatkan data jumlah orang dari database 
def jumlah_orang():
    batas = db.child(ruang).child('jumlah orang').get() #mendapatkan data dari batas orang
    return batas.val()

#mendapatkan data pelanggar masker 
def pelanggar_masker():
    pelaggar = db.child(ruang).child('pelanggar masker').get()
    return pelaggar.val()
