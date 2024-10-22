from flask import Blueprint, request, render_template, redirect, url_for
from HW2.db.db import get_db_connection
from HW2.repos.dept_repo import get_all_dept, add_dept, update_dept, delete_dept

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

    res = add_dept(db_conn, dept_id, name)
    if res:
        return redirect(url_for('get_all_dept_route'))
    
    return None

@dept_routes.route("/update/<id>", methods=['PUT'])
def update_dept_route(id):
    db_conn = get_db_connection()
    req = request.get_json()
    dept_id = req['dept_id']
    name = req['name']

    res = update_dept(db_conn, id, dept_id, name)
    if res:
        return {}, 204
    else:
        return {}, 400

@dept_routes.route("/delete/<id>", methods=['DELETE'])
def delete_dept_route(id):
    db_conn = get_db_connection()
    res = delete_dept(db_conn, id)
    if res:
        return {}, 204
    else:
        return {}, 400
