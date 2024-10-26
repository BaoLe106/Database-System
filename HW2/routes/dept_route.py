from flask import Blueprint, jsonify, request, render_template, redirect, url_for
from db.db import get_db_connection
from repos.dept_repo import get_all_dept, add_dept, update_dept, delete_dept

dept_routes = Blueprint('dept_routes', __name__, url_prefix='/dept')

@dept_routes.route('/', methods=['GET'])
def get_all_dept_route():
	db_conn = get_db_connection()
	depts = get_all_dept(db_conn)
	return render_template('department.html', depts=depts)

@dept_routes.route("/", methods=['POST'])
def add_dept_route():
    db_conn = get_db_connection()
    req = request.form

    dept_id = req['dept_id']
    name = req['name']
    num_of_faculty = req['num_of_faculty']

    res, error_message = add_dept(db_conn, dept_id, name, num_of_faculty)
    if res:
        return redirect(url_for('dept_routes.get_all_dept_route'))
    
    return jsonify({"error": error_message}), 400

@dept_routes.route("/update/<id>", methods=['PUT'])
def update_dept_route(id):
    db_conn = get_db_connection()
    req = request.get_json()
    dept_id = req['dept_id']
    name = req['name']
    num_of_faculty = req['num_of_faculty']

    res, error_message = update_dept(db_conn, id, dept_id, name, num_of_faculty)
    if res:
        return {}, 204
    return jsonify({"error": error_message}), 400

@dept_routes.route("/delete/<id>", methods=['DELETE'])
def delete_dept_route(id):
    db_conn = get_db_connection()
    res = delete_dept(db_conn, id)
    if res:
        return {}, 204
    else:
        return {}, 400
