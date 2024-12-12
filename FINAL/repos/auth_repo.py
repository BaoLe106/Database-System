from werkzeug.security import generate_password_hash, check_password_hash

def register(db_conn, user_id, username: str = None, password: str = None):
	try:
		cur = db_conn.cursor(dictionary=True)
		
		check_users_query_by_username = 'SELECT * FROM users WHERE username = %s'
		cur.execute(check_users_query_by_username, (username,))
		if cur.fetchone():
			return False, "Username already exists."
		
		encrypted_password = generate_password_hash(password, "scrypt")
		post_query = 'INSERT INTO users (id, username, password) VALUES (%s, %s, %s)'
		cur.execute(post_query, (str(user_id), username, encrypted_password,))

		db_conn.commit()
		return True, None
	except Exception as err:
		return False, err
	finally:
		if db_conn.is_connected():
			cur.close()
			db_conn.close()


def login(db_conn, username: str = None, password: str = None):
	try:
		cur = db_conn.cursor(dictionary=True)
		
		check_users_query_by_username = 'SELECT * FROM users WHERE username = %s'
		cur.execute(check_users_query_by_username, (username,))
		user = cur.fetchone()
		if not user:
			return None
		
		if not check_password_hash(user['password'], password):
			return None

		return user
	except Exception as err:
		return None
	finally:
		if db_conn.is_connected():
			cur.close()
			db_conn.close()