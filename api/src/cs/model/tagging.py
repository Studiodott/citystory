from flask import g
import psycopg2
import psycopg2.extras
from ulid import ULID
from pprint import pprint as D
from cs import app
from cs.model.setup import key

def list():
	q = """
		SELECT
			ti.id as id,
			ti.handle as handle,
			m.handle as media_handle,
			t.handle as tag_handle,
			u.handle as user_handle,
			ti.position as position,
			ti.comment as comment,
			ti.created_at as created_at
		FROM
			tagging ti
			INNER JOIN media m ON ti.media_id = m.id
			INNER JOIN tag t ON ti.tag_id = t.id
			INNER JOIN "user" u ON ti.user_id = u.id;
		"""

	g.db_cur.execute(q)
	return g.db_cur.fetchall()

def get(handle):
	q = """
		SELECT
			ti.id as id,
			ti.handle as handle,
			m.handle as media_handle,
			t.handle as tag_handle,
			u.handle as user_handle,
			ti.position as position,
			ti.comment as comment,
			ti.created_at as created_at
		FROM
			tagging ti
			INNER JOIN media m ON ti.media_id = m.id
			INNER JOIN tag t ON ti.tag_id = t.id
			INNER JOIN "user" u ON ti.user_id = u.id
		WHERE
			ti.handle=%(handle)s;
		"""

	g.db_cur.execute(q, {
		'handle' : handle,
	})
	return g.db_cur.fetchone()

def create(media_handle, tag_handle, user_handle, position, comment=''):
	handle = key()

	q = """
		INSERT INTO "tagging" (
			"handle",
			"media_id",
			"tag_id",
			"user_id",
			"position",
			"comment",
			"created_at"
		) VALUES (
			%(handle)s,
			(select id from media where handle=%(media_handle)s),
			(select id from tag where handle=%(tag_handle)s),
			(select id from "user" where handle=%(user_handle)s),
			%(position)s,
			%(comment)s,
			NOW()
		);"""

	a = {
		'handle' : handle,
		'media_handle' : media_handle,
		'tag_handle' : tag_handle,
		'user_handle' : user_handle,
		'position' : position,
		'comment' : comment,
	}
	print(f'a={a}')
	g.db_cur.execute(q, a)

	return handle
