def get_all_dept(db_conn):
    try:
        cur = db_conn.cursor(dictionary=True)
        
        get_query = 'SELECT id, dept_id, name, num_of_faculty FROM department'
        cur.execute(get_query)
        depts = cur.fetchall()

        return depts
    except Exception as err:
        print("get_all_dept_error: ", err)
        return None
    finally:
        if db_conn.is_connected():
            cur.close()
            db_conn.close()
    
def add_dept(db_conn, dept_id, name, num_of_faculty):
    try:
        cur = db_conn.cursor()

        check_dept_query_for_id = 'SELECT id FROM department WHERE dept_id = %s'
        cur.execute(check_dept_query_for_id, (dept_id,))
        if cur.fetchone():
            return False, "Department ID already exists."

        check_dept_query_for_name = 'SELECT id FROM department WHERE name = %s'
        cur.execute(check_dept_query_for_name, (name,))
        if cur.fetchone():
            return False, "Department name already exists."

        post_query = 'INSERT INTO department (dept_id, name, num_of_faculty) VALUES (%s, %s, %s)'
        cur.execute(post_query, (dept_id, name, num_of_faculty,))
        
        db_conn.commit()
        return True, None
    except Exception as err:
        print("add_dept_error: ", err)
        return False, err
    finally:
        if db_conn.is_connected():
            cur.close()
            db_conn.close()

def update_dept(db_conn, id, dept_id, name, num_of_faculty):
    try:
        cur = db_conn.cursor()

        check_dept_query_for_id = 'SELECT id FROM department WHERE id != %s AND dept_id = %s'
        cur.execute(check_dept_query_for_id, (id, dept_id,))
        if cur.fetchone():
            return False, "Department ID already exists."

        check_dept_query_for_name = 'SELECT id FROM department WHERE id != %s AND name = %s'
        cur.execute(check_dept_query_for_name, (id, name,))
        if cur.fetchone():
            return False, "Department name already exists."
        
        update_query = 'UPDATE department SET dept_id = %s, name = %s, num_of_faculty = %s WHERE id = %s'
        cur.execute(update_query, (dept_id, name, num_of_faculty, id,))

        db_conn.commit()
        return True, None
    except Exception as err:
        print("update_dept_error: ", err)
        return False, err
    finally:
        if db_conn.is_connected():
            cur.close()
            db_conn.close()

def delete_dept(db_conn, id):
    try:
        cur = db_conn.cursor()

        delete_query = 'DELETE FROM department WHERE id = %s'

        cur.execute(delete_query, (id,))
        db_conn.commit()
        return True
    except Exception as err:
        print("delete_dept_error", err)
        return False
    finally:
        if db_conn.is_connected():
            cur.close()
            db_conn.close()