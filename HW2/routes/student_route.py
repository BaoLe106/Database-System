from flask import Blueprint, request, render_template, redirect, url_for
from HW2.db.db import get_db_connection
from HW2.repos.student_repo import get_all_student, add_student, update_student, delete_student

student_routes = Blueprint('student_routes', __name__, url_prefix='/student')

@student_routes.route('/', methods=['GET'])
def get_all_dept_route():
	db_conn = get_db_connection()
	students = get_all_student(db_conn)
	return render_template('student.html', students=students)

@student_routes.route("/", methods=['POST'])
def add_dept_route():
    db_conn = get_db_connection()
    req = request.form

    student_id = req['student_id']
    name = req['name']
    dept_id = req['dept_id']
    dob = req['dob']

    res = add_student(db_conn, student_id, name, dept_id, dob)
    if res:
        return redirect(url_for('get_all_dept_route'))
    
    return None

@student_routes.route("/update/<id>", methods=['PUT'])
def update_dept_route(id):
    db_conn = get_db_connection()
    req = request.get_json()
    name = req['name']
    dept_id = req['dept_id']
    dob = req['dob']

    res = update_student(db_conn, id, dept_id, name, dob)
    if res:
        return {}, 204
    else:
        return {}, 400

@student_routes.route("/delete/<id>", methods=['DELETE'])
def delete_dept_route(id):
    db_conn = get_db_connection()
    res = delete_student(db_conn, id)
    if res:
        return {}, 204
    else:
        return {}, 400
