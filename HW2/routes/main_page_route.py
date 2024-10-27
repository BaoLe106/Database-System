from flask import Blueprint, render_template
from db.db import get_db_connection
from repos.main_repo import get_join_data

main_page_routes = Blueprint('main_page_routes', __name__)

@main_page_routes.route('/', methods=['GET'])
def get_student_attendance_route():
	db_conn = get_db_connection()
	join_data = get_join_data(db_conn)

	return render_template('main_page.html', data=join_data)