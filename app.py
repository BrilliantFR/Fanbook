from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient

client = MongoClient('mongodb+srv://Brilliant:sparta@cluster0.avtskzb.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta

app = Flask(__name__)

@app.route('/')
def home():
   return render_template('index.html')

@app.route("/bucket", methods=["POST"])
def bucket_post():
    bucket_receive = request.form['bucket_give']
    count = db.bucket.count_documents({})
    num = count + 1
    doc = {
        'num':num,
        'bucket': bucket_receive,
        'done': 0 #artinya blm selsai, jika 1 artinya sudah selesai
    }
    db.bucket.insert_one(doc)
    return jsonify({'msg': 'Data Saved!'})

@app.route("/bucket/done", methods=["POST"])
def bucket_done():
    num_receive = request.form["num_give"]
    db.bucket.update_one(
        {'num': int(num_receive)},
        {'$set': {'done': 1}}
    )
    return jsonify({'msg': 'Update done!'})

@app.route("/bucket", methods=["GET"])
def bucket_get():
    bucket_list = list(db.bucket.find({}, {'_id': False}))
    return jsonify({'buckets': bucket_list})

@app.route("/bucket/delete", methods=["POST"])
def bucket_delete():
    delete_receive = request.form["delete_give"]
    db.bucket.delete_one(
        {'num': int(delete_receive)}
    )
    return jsonify({'msg': 'Delete done!'})

if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)