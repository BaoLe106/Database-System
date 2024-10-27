def get_student_attendance(db_conn):
    try:
        cur = db_conn.cursor(dictionary=True)

        get_query = 'SELECT id, student_id, name, created_at FROM student_attendance'
        cur.execute(get_query)
        student_attendances = cur.fetchall()

        return student_attendances
    except Exception as err:
        print("get_student_attendance error: ", err)
        return None
    finally:
        if db_conn.is_connected():
            cur.close()
            db_conn.close()
    
def add_student_attendance(db_conn, student_id, name):
    try:
        cur = db_conn.cursor(buffered=True)

        post_query = 'INSERT INTO student_attendance (student_id, name) VALUES (%s, %s)'
        cur.execute(post_query, (student_id, name))

        db_conn.commit()
        return True
    except Exception as err:
        print("get_student_attendance error: ", err)
        return False
    finally:
        if db_conn.is_connected():
            cur.close()
            db_conn.close()

def update_student_attendance(db_conn, id, student_id, name):
    try:
        cur = db_conn.cursor(buffered=True)

        update_query = 'UPDATE student_attendance SET student_id = %s, name = %s WHERE id = %s'
        cur.execute(update_query, (student_id, name, id))

        db_conn.commit()
        return True
    except Exception as err:
        print("get_student_attendance error: ", err)
        return False
    finally:
        if db_conn.is_connected():
            cur.close()
            db_conn.close()

def delete_student_attendance(db_conn, id):
    try:
        cur = db_conn.cursor()

        delete_query = 'DELETE FROM student_attendance WHERE id = %s'

        cur.execute(delete_query, (id,))
        db_conn.commit()
        return True
    except Exception as err:
        print("delete_student_attendance_error", err)
        return False
    finally:
        if db_conn.is_connected():
            cur.close()
            db_conn.close()