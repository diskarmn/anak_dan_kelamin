import os
from os.path import join, dirname
from dotenv import load_dotenv
from flask import Flask ,render_template,request,jsonify
from pymongo import MongoClient

app=Flask(__name__)
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGODB_URI = os.environ.get("MONGODB_URI")
DB_NAME =  os.environ.get("DB_NAME")
client = MongoClient(MONGODB_URI)
db=client[DB_NAME]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tambah',methods=['POST'])
def tambah():
    depan=request.form['kunci_depan']
    belakang=request.form['kunci_belakang']
    kelamin=request.form['kunci_kelamin']
    count=db.daftar.count_documents({})
    nomor=count +1
    doc={
        'nama_depan':depan,
        'nama_belakang':belakang,
        'jenis_kelamin':kelamin,
        'nomor':nomor,
        'coret':0
    }
    db.daftar.insert_one(doc)
    return jsonify({"pesan":"berhasil menamba anak"})
@app.route("/tampil",methods=['GET'])
def tampil():
    isi=list(db.daftar.find({},{'_id':False}))
    return jsonify({'semua':isi})
@app.route('/hapus',methods=['POST'])
def hapus():
    nomornya=request.form['kunci_nomor']
    db.daftar.delete_one({'nomor':int(nomornya)})
    return jsonify({'pesan':'berhasil hapus data'})

if __name__=='__main__':
    app.run(debug=True)