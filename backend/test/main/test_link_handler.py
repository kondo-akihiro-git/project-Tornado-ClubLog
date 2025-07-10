import tornado.web
from tornado.testing import AsyncHTTPTestCase, gen_test
import json
import uuid
from backend.api.main import make_app
from backend.db.connection.connection import get_connection

class TestLinkHandler(AsyncHTTPTestCase):
	def get_app(self):
		return make_app()

	@gen_test
	async def test_create_link(self):
		conn = get_connection()
		cursor = conn.cursor()

		try:
			# ユーザー取得 or 作成
			cursor.execute("SELECT id FROM users WHERE mail_address = 'linktest@example.com';")
			row = cursor.fetchone()
			if row:
				user_id = row[0]
			else:
				cursor.execute("""
					INSERT INTO users (username, mail_address, password)
					VALUES ('linktestuser', 'linktest@example.com', 'dummy')
					RETURNING id;
				""")
				user_id = cursor.fetchone()[0]

			# クラブ作成
			cursor.execute("""
				INSERT INTO clubs (name, owner_id)
				VALUES ('リンクテストクラブ', %s)
				RETURNING id;
			""", (user_id,))
			club_id = cursor.fetchone()[0]

			# イベント作成
			cursor.execute("""
				INSERT INTO events (title, club_id)
				VALUES ('リンクテストイベント', %s)
				RETURNING id;
			""", (club_id,))
			event_id = cursor.fetchone()[0]

			# eventsのIDシーケンスリセット（万が一に備えて）
			cursor.execute("SELECT setval('events_id_seq', (SELECT COALESCE(MAX(id), 1) FROM events));")

			conn.commit()

			# リンク作成テスト
			url_token = str(uuid.uuid4())
			payload = {
				"url_token": url_token,
				"event_id": event_id
			}

			response = await self.http_client.fetch(
				self.get_url("/link"),
				method="POST",
				headers={"Content-Type": "application/json"},
				body=json.dumps(payload)
			)

			assert response.code == 201
			body = json.loads(response.body.decode("utf-8"))
			assert body["url_token"] == url_token
			assert body["event_id"] == event_id

		finally:
			# 後片付け
			cursor.execute("DELETE FROM links WHERE event_id = %s;", (event_id,))
			cursor.execute("DELETE FROM events WHERE id = %s;", (event_id,))
			cursor.execute("DELETE FROM clubs WHERE id = %s;", (club_id,))
			cursor.execute("DELETE FROM users WHERE id = %s AND mail_address = 'linktest@example.com';", (user_id,))
			conn.commit()
			cursor.close()
			conn.close()
