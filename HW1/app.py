from flask import Flask, request, render_template, redirect, url_for
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

db_config = {
    'user': 'root',
    'password': '', #your mysql server password
    'host': 'localhost',
    'database': 'dbsys'
}

def get_student_attendance():
    try:
        db_conn = mysql.connector.connect(**db_config)
        cur = db_conn.cursor(dictionary=True)

        get_query = 'SELECT id, student_id, name, created_at FROM student_attendance'
        cur.execute(get_query)
        student_attendances = cur.fetchall()

        return student_attendances
    except Error as err:
        print("get_student_attendance error: ", err)
        return None
    finally:
        if db_conn.is_connected():
            cur.close()
            db_conn.close()
    
def add_student_attendance(student_id, name):
    try:
        db_conn = mysql.connector.connect(**db_config)
        cur = db_conn.cursor()

        post_query = 'INSERT INTO student_attendance (student_id, name) VALUES (%s, %s)'
        cur.execute(post_query, (student_id, name))

        db_conn.commit()
        return True
    except Error as err:
        print("get_student_attendance error: ", err)
        return False
    finally:
        if db_conn.is_connected():
            cur.close()
            db_conn.close()

def update_student_attendance(id, student_id, name):
    try:
        db_conn = mysql.connector.connect(**db_config)
        cur = db_conn.cursor()

        update_query = 'UPDATE student_attendance SET student_id = %s, name = %s WHERE id = %s'
        cur.execute(update_query, (student_id, name, id))

        db_conn.commit()
        return True
    except Error as err:
        print("get_student_attendance error: ", err)
        return False
    finally:
        if db_conn.is_connected():
            cur.close()
            db_conn.close()

def delete_student_attendance(id):
    try:
        db_conn = mysql.connector.connect(**db_config)
        cur = db_conn.cursor()

        delete_query = 'DELETE FROM student_attendance WHERE id = %s'

        cur.execute(delete_query, (id,))
        db_conn.commit()
        return True
    except Error as err:
        print("delete_student_attendance_error", err)
        return False
    finally:
        if db_conn.is_connected():
            cur.close()
            db_conn.close()

@app.route("/")
def home():
    student_attendances = get_student_attendance()
    return render_template('homepage.html', student_attendances=student_attendances)

@app.route("/", methods=['POST'])
def add_student_attendance_route():
    req = request.form

    student_id = req['student_id']
    name = req['name']

    res = add_student_attendance(student_id, name)
    if res:
        return redirect(url_for('home'))
    
    return None

@app.route("/update/<id>", methods=['PUT'])
def update_student_attendance_route(id):
    req = request.get_json()
    student_id = req['student_id']
    name = req['name']

    res = update_student_attendance(id, student_id, name)
    if res:
        return {}, 204
    else:
        return {}, 400

@app.route("/delete/<id>", methods=['DELETE'])
def delete_student_attendance_route(id):
    res = delete_student_attendance(id)
    if res:
        return {}, 204
    else:
        return {}, 400

if __name__ == '__name__':
    app.run(debug=True)