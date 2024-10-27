def get_join_data(db_conn):
    try:
        cur = db_conn.cursor(dictionary=True)

        join_query = """
			SELECT 
				student.student_id AS student_id, 
				student.name AS student_name, 
				student.dept_id AS dept_id,
				department.name AS department_name,
				COUNT(attendance.student_id) AS attendance_count, 
				MAX(attendance.created_at) AS latest_attendance
			FROM 
				student_info AS student
			LEFT JOIN 
				student_attendance AS attendance
				ON attendance.student_id = student.student_id
			JOIN 
				department
				ON department.dept_id = student.dept_id
			GROUP BY 
				student.student_id, 
				student.name
			;
        """
        cur.execute(join_query)
        join_data = cur.fetchall()

        return join_data
    except Exception as err:
        print("get_all_student_error: ", err)
        return None
    finally:
        if db_conn.is_connected():
            cur.close()
            db_conn.close()