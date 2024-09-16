from flask import Flask, request, render_template, redirect, url_for
import mysql.connector

app = Flask(__name__)

db_config = {
    'user': 'root',
    'password': '', #your mysql server password
    'host': 'localhost',
    'database': 'dbsys'
}

@app.route("/", methods=['GET', 'POST'])
def home():
    db_conn = mysql.connector.connect(**db_config)
    cur = db_conn.cursor(dictionary=True)

    if request.method == 'POST':
        req = request.form
        
        post_query = 'INSERT INTO student_attendance (student_id, name) VALUES (%s, %s)'
        cur.execute(post_query, (req['student_id'], req['name'], ))
        db_conn.commit()
        
        cur.close()
        db_conn.close()
        return redirect(url_for('home'))
        
    get_query = 'SELECT id, student_id, name, created_at FROM student_attendance'
    cur.execute(get_query)
    student_attendances = cur.fetchall()
    
    cur.close()
    db_conn.close()
    return render_template('homepage.html', student_attendances=student_attendances)

if __name__ == '__name__':
    app.run(debug=True)