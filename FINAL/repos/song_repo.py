def add_new_song(db_conn, records):
	try:
		cur = db_conn.cursor(dictionary=True)

		post_query = 'INSERT INTO songs (id, user_id) VALUES (%s, %s)'
		cur.executemany(post_query, records)
		db_conn.commit()

		return True, None
	except Exception as err:
		return False, err
	finally:
		if db_conn.is_connected():
			cur.close()
			db_conn.close()

def get_songs_by_user_id(db_conn, user_id):
	try:
		cur = db_conn.cursor(dictionary=True)

		songs_query_by_user_id = 'SELECT id FROM songs WHERE user_id = %s'
		cur.execute(songs_query_by_user_id, (user_id,))
		songs = cur.fetchall()
		
		return songs
	except Exception as err:
		return False, err
	finally:
		if db_conn.is_connected():
			cur.close()
			db_conn.close()

def delete_song_by_song_id(db_conn, song_id):
	try:
		cur = db_conn.cursor(dictionary=True)

		delete_song_query_by_song_id = 'DELETE FROM songs WHERE id = %s'
		cur.execute(delete_song_query_by_song_id, (song_id,))
		db_conn.commit()
		
		return True, None
	except Exception as err:
		return False, err
	finally:
		if db_conn.is_connected():
			cur.close()
			db_conn.close()