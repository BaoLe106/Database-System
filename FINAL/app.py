from flask import Flask, session, render_template, request, Response, jsonify, redirect, url_for, abort
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from datetime import timedelta
from gridfs import GridFS
from bson import ObjectId
import uuid
import os
from datetime import datetime
import tempfile
from db.db import get_db_connection
from repos.auth_repo import register, login
from repos.song_repo import add_new_song, get_songs_by_user_id

CACHE_DIR = tempfile.mkdtemp()
print(f"Temporary cache directory: {CACHE_DIR}")

uri = "mongodb+srv://lgbaoo106:<password>@dbsys-nosql.uur7i.mongodb.net/?retryWrites=true&w=majority&appName=dbsys-nosql"

app = Flask(__name__)
app.config['SECRET_KEY'] = '39408tyr89weasd9q08ghgfxma0882'
app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(minutes=5)
client = MongoClient(uri, server_api=ServerApi('1'))
db = client['local_dbsys']  # The database name
fs = GridFS(db, collection="songs")


@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/register')
def register_page():
    return render_template('register.html')

@app.route('/api/register', methods=['POST'])
def apiRegiser():
    db_conn = get_db_connection()

    req = request.get_json()
    user_id = uuid.uuid4()
    username = req['username']
    password = req['password']

    res, error_msg = register(db_conn, user_id, username, password)
    
    if res:
        return jsonify({"message": "Register user OK"}), 201
    
    return jsonify({"error": error_msg}), 400

@app.route('/api/login', methods=['POST'])
def apiLogin():
    db_conn = get_db_connection()

    req = request.get_json()
    username = req['username']
    password = req['password']

    user = login(db_conn, username, password)
    if user:
        session.permanent = True
        session['user'] = {"id": user['id'], "username": user['username']}
        return '', 201
        
    
    return jsonify({"error": "Wrong username or password"}), 400

@app.route('/')
def index():
    user = session.get('user')
    if not user:
        return redirect('/login') 

    db_conn = get_db_connection()
    songs = get_songs_by_user_id(db_conn, user['id'])
    files = []

    for song in songs:
        song_uuid =  uuid.UUID(song['id'])

        file =  db.songs.files.find_one({"_id": ObjectId(song_uuid.bytes[:12])})
        files.append({
            "_id": str(file["_id"]), 
            "filename": file["filename"],
            "length": f"{int(((file["length"] * 8) / (256 * 1000)) // 60)}:{int(((file["length"] * 8) / (256 * 1000)) % 60):02d}",
            "lengthFloat": ((file["length"] * 8) / (256 * 1000)) / 60,
            "uploadDate": datetime.fromisoformat(str(file["uploadDate"])).strftime("%Y-%m-%d"),
            "audioUrl": f"/stream/{file['_id']}"
        })

    return render_template('index.html', files=files, user=user)

@app.route('/upload', methods=['POST'])
def upload():
    db_conn = get_db_connection()
    user = session.get('user')
    try: 
        for file in request.files.getlist('files'):
            if file and file.filename:
                file_id = fs.put(file, filename=file.filename)
                file_uuid = uuid.UUID(bytes=file_id.binary + b'\x00\x00\x00\x00')
                
                res, error_msg = add_new_song(db_conn, file_uuid, user['id'])
                if (res != True):
                    raise Exception(error_msg)
    except Exception as err:
        print("debug err in upload song", err)
        abort(400, description="File cannot upload")

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