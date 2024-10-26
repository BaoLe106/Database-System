from flask import Flask
from routes.main_page_route import main_page_routes
from routes.attendance_route import attendance_routes
from routes.dept_route import dept_routes
from routes.student_route import student_routes

app = Flask(__name__)
app.register_blueprint(main_page_routes)
app.register_blueprint(attendance_routes)
app.register_blueprint(dept_routes)
app.register_blueprint(student_routes)

if __name__ == '__name__':
    app.run(debug=True)