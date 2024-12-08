from flask import Flask, render_template, request, Response, redirect, url_for, send_file, abort
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from gridfs import GridFS
from bson import ObjectId
import io
import os
from datetime import datetime
import tempfile

CACHE_DIR = tempfile.mkdtemp()
print(f"Temporary cache directory: {CACHE_DIR}")

uri = "mongodb+srv://lgbaoo106:<password>@dbsys-nosql.uur7i.mongodb.net/?retryWrites=true&w=majority&appName=dbsys-nosql"

app = Flask(__name__)

client = MongoClient(uri, server_api=ServerApi('1'))
db = client['local_dbsys']  # The database name
fs = GridFS(db, collection="songs")


@app.route('/')
def index():
    files = [
        {
            "_id": str(file["_id"]), 
            "filename": file["filename"],
            "length": f"{int(((file["length"] * 8) / (256 * 1000)) // 60)}:{int(((file["length"] * 8) / (256 * 1000)) % 60):02d}",
            "lengthFloat": ((file["length"] * 8) / (256 * 1000)) / 60,
            "uploadDate": datetime.fromisoformat(str(file["uploadDate"])).strftime("%Y-%m-%d"),
            "audioUrl": f"/stream/{file['_id']}"

        } for file in db.songs.files.find()
    ]
    return render_template('index.html', files=files)

@app.route('/upload', methods=['POST'])
def upload():
    for file in request.files.getlist('files'):
        if file and file.filename:
            fs.put(file, filename=file.filename)

    return '', 201


@app.route('/updateSongName/<file_id>', methods=['PUT'])
def updateSongName(file_id):
    req = request.get_json()
    new_song_name = req['new_song_name']

    db.songs.files.update_one({
        "_id": ObjectId(file_id)
    }, {
        "$set": {"filename": new_song_name}
    })

    return '', 201


@app.route('/stream/<file_id>', methods=['GET'])
def stream(file_id):
    cache_path = os.path.join(CACHE_DIR, f"{file_id}.mp3")

    if not os.path.exists(cache_path):
        try:
            file = fs.get(ObjectId(file_id))
            with open(cache_path, 'wb') as f:
                f.write(file.read())

            # Serve the file after writing it to disk cache
            return Response(open(cache_path, 'rb'), mimetype="audio/mpeg", status=200)
        except Exception as e:
            abort(404, description="File not found")
    else:
        return Response(open(cache_path, 'rb'), mimetype="audio/mpeg", status=200)
    
    # return send_file(io.BytesIO(file.read()), mimetype="audio/mpeg", as_attachment=False)

@app.route('/delete/<file_id>', methods=['DELETE'])
def delete_song(file_id):
    try:
        fs.delete(ObjectId(file_id))
        return '', 204
    except Exception as e:
        print("Error deleting file:", e)
        abort(404, description="File not found")

if __name__ == '__main__':
    app.run(debug=True)