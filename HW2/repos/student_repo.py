def get_all_student(db_conn):
    try:
        cur = db_conn.cursor(dictionary=True)

        get_query = 'SELECT id, student_id, name, dept_id, dob FROM student_info'
        cur.execute(get_query)
        students = cur.fetchall()

        return students
    except Exception as err:
        print("get_all_student_error: ", err)
        return None
    finally:
        if db_conn.is_connected():
            cur.close()
            db_conn.close()
    
def add_student(db_conn, student_id, name, dept_id, dob):
    try:
        cur = db_conn.cursor(buffered=True)

        check_student_query_for_student_id = 'SELECT id FROM student_info WHERE student_id = %s'
        cur.execute(check_student_query_for_student_id, (student_id,))
        if cur.fetchone():
            return False, "Student ID already exists."

        post_query = 'INSERT INTO student_info (student_id, name, dept_id, dob) VALUES (%s, %s, %s, %s)'
        cur.execute(post_query, (student_id, name, dept_id, dob))

        db_conn.commit()
        return True, None
    except Exception as err:
        print("add_student_error: ", err)
        return False, err
    finally:
        if db_conn.is_connected():
            cur.close()
            db_conn.close()

def update_student(db_conn, id, student_id, name, dept_id, dob):
    try:
        cur = db_conn.cursor(buffered=True)

        check_student_query_for_student_id = 'SELECT id FROM student_info WHERE id != %s AND student_id = %s'
        cur.execute(check_student_query_for_student_id, (id, student_id,))
        if cur.fetchone():
            return False, "Student ID already exists."

        update_query = 'UPDATE student_info SET dept_id = %s, name = %s, dob=%s WHERE id = %s'
        cur.execute(update_query, (dept_id, name, dob, id))

        db_conn.commit()
        return True, None
    except Exception as err:
        print("update_student_error: ", err)
        return False, err
    finally:
        if db_conn.is_connected():
            cur.close()
            db_conn.close()

def delete_student(db_conn, id):
    try:
        cur = db_conn.cursor()

        delete_query = 'DELETE FROM student_info WHERE id = %s'

        cur.execute(delete_query, (id,))
        db_conn.commit()
        return True
    except Exception as err:
        print("delete_student_error", err)
        return False
    finally:
        if db_conn.is_connected():
            cur.close()
            db_conn.close()