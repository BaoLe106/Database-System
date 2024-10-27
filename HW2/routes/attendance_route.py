from flask import Blueprint, jsonify, request, render_template, redirect, url_for
from db.db import get_db_connection
from repos.attendance_repo import get_student_attendance, add_student_attendance, update_student_attendance, delete_student_attendance

attendance_routes = Blueprint('attendance_routes', __name__, url_prefix='/attendance')

@attendance_routes.route('/', methods=['GET'])
def get_student_attendance_route():
    db_conn = get_db_connection()
    student_attendances = get_student_attendance(db_conn)
    return render_template('attendance.html', student_attendances=student_attendances)

@attendance_routes.route("/", methods=['POST'])
def add_student_attendance_route():
    db_conn = get_db_connection()
    req = request.form

    student_id = req['student_id']
    name = req['name']

    res = add_student_attendance(db_conn, student_id, name)
    if res:
        return jsonify({"message": "Add OK"}), 201
    
    return jsonify({"error": "Add error"}), 400

@attendance_routes.route("/update/<id>", methods=['PUT'])
def update_student_attendance_route(id):
    db_conn = get_db_connection()
    req = request.get_json()
    student_id = req['student_id']
    name = req['name']

    res = update_student_attendance(db_conn, id, student_id, name)
    if res:
        return jsonify({"message": "Update OK"}), 204

    return jsonify({"error": "Update error"}), 400

@attendance_routes.route("/delete/<id>", methods=['DELETE'])
def delete_student_attendance_route(id):
    db_conn = get_db_connection()
    res = delete_student_attendance(db_conn, id)
    if res:
        return jsonify({"message": "Delete OK"}), 204

    return jsonify({"error": "Delete error"}), 400
