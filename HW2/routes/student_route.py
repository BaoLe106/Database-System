from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from db.db import get_db_connection
from repos.student_repo import get_all_student, add_student, update_student, delete_student

student_routes = Blueprint('student_routes', __name__, url_prefix='/student')

@student_routes.route('/', methods=['GET'])
def get_all_student_route():
	db_conn = get_db_connection()
	students = get_all_student(db_conn)
	return render_template('student.html', students=students)

@student_routes.route("/", methods=['POST'])
def add_student_route():
    db_conn = get_db_connection()
    req = request.form

    student_id = req['student_id']
    name = req['name']
    dept_id = req['dept_id']
    dob = req['dob']

    res, error_message = add_student(db_conn, student_id, name, dept_id, dob)
    if res:
        return jsonify({"message": "Add OK"}), 201
    
    return jsonify({"error": error_message}), 400

@student_routes.route("/update/<id>", methods=['PUT'])
def update_student_route(id):
    db_conn = get_db_connection()
    req = request.get_json()
    print("debug req", req)

    student_id = req['student_id']
    name = req['name']
    dept_id = req['dept_id']
    dob = req['dob']
    
    res, error_message = update_student(db_conn, id, student_id, name, dept_id, dob)
    if res:
        return jsonify({"message": "Update OK"}), 204

    return jsonify({"error": error_message}), 400

@student_routes.route("/delete/<id>", methods=['DELETE'])
def delete_student_route(id):
    db_conn = get_db_connection()
    res = delete_student(db_conn, id)
    if res:
        return jsonify({"message": "Delete OK"}), 204
    
    return {}, 400
