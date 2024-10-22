from flask import Flask

from HW2.routes.attendance_route import attendance_routes
from HW2.routes.dept_route import dept_routes
from HW2.routes.student_route import student_routes

app = Flask(__name__)
app.register_blueprint(attendance_routes)
app.register_blueprint(dept_routes)
app.register_blueprint(student_routes)

if __name__ == '__name__':
    app.run(debug=True)