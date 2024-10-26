from flask import Blueprint, render_template
# from repos.attendance_repo import get_student_attendance, add_student_attendance, update_student_attendance, delete_student_attendance

main_page_routes = Blueprint('main_page_routes', __name__)

@main_page_routes.route('/', methods=['GET'])
def get_student_attendance_route():
	return render_template('main_page.html')