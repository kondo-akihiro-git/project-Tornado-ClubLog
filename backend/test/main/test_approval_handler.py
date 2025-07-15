# backend/test/main/test_approval_handler.py
from tornado.testing import AsyncHTTPTestCase, gen_test
from backend.api.main import make_app
from backend.db.connection.connection import get_connection
import json

class TestApprovalHandler(AsyncHTTPTestCase):
	def get_app(self):
		return make_app()

	@gen_test
	async def test_approve_and_reject(self):
		conn = get_connection()
		cursor = conn.cursor()

		try:
			# ユーザー作成
			cursor.execute("""
				INSERT INTO users (username, mail_address, password)
				VALUES ('approvaltestuser', 'approval@example.com', 'dummy')
				RETURNING id;
			""")
			user_id = cursor.fetchone()[0]

			# クラブ作成
			cursor.execute("""
				INSERT INTO clubs (name, owner_id)
				VALUES ('Approval Test Club', %s)
				RETURNING id;
			""", (user_id,))
			club_id = cursor.fetchone()[0]

			# イベント作成
			cursor.execute("""
				INSERT INTO events (title, club_id)
				VALUES ('Approval Event', %s)
				RETURNING id;
			""", (club_id,))
			event_id = cursor.fetchone()[0]

			# 参加者登録
			cursor.execute("""
				INSERT INTO participants (user_id, event_id)
				VALUES (%s, %s);
			""", (user_id, event_id))

			conn.commit()

			# ステータス変更（承認）
			payload_approve = {
				"user_id": user_id,
				"event_id": event_id,
				"status": "approved"
			}
			response = await self.http_client.fetch(
				self.get_url("/approval"),
				method="POST",
				headers={"Content-Type": "application/json"},
				body=json.dumps(payload_approve)
			)
			assert response.code == 200

			# ステータス変更（却下）
			payload_reject = {
				"user_id": user_id,
				"event_id": event_id,
				"status": "rejected"
			}
			response = await self.http_client.fetch(
				self.get_url("/approval"),
				method="POST",
				headers={"Content-Type": "application/json"},
				body=json.dumps(payload_reject)
			)
			assert response.code == 200

			# DB確認（却下されているはず）
			cursor.execute("""
				SELECT approved_status FROM participants WHERE user_id = %s AND event_id = %s;
			""", (user_id, event_id))
			status = cursor.fetchone()[0]
			assert status == "rejected"

		finally:
			cursor.execute("DELETE FROM participants WHERE user_id = %s AND event_id = %s;", (user_id, event_id))
			cursor.execute("DELETE FROM events WHERE id = %s;", (event_id,))
			cursor.execute("DELETE FROM clubs WHERE id = %s;", (club_id,))
			cursor.execute("DELETE FROM users WHERE id = %s;", (user_id,))
			conn.commit()
			cursor.close()
			conn.close()


	@gen_test
	async def test_get_approval_status(self):
		conn = get_connection()
		cursor = conn.cursor()

		try:
			cursor.execute("""
				INSERT INTO users (username, mail_address, password)
				VALUES ('getapprovaluser', 'getapproval@example.com', 'dummy')
				RETURNING id;
			""")
			user_id = cursor.fetchone()[0]

			cursor.execute("""
				INSERT INTO clubs (name, owner_id)
				VALUES ('GetApproval Club', %s)
				RETURNING id;
			""", (user_id,))
			club_id = cursor.fetchone()[0]

			cursor.execute("""
				INSERT INTO events (title, club_id)
				VALUES ('GetApproval Event', %s)
				RETURNING id;
			""", (club_id,))
			event_id = cursor.fetchone()[0]

			cursor.execute("""
				INSERT INTO participants (user_id, event_id, approved_status)
				VALUES (%s, %s, 'approved');
			""", (user_id, event_id))

			conn.commit()

			# GETで承認ステータスを取得
			url = f"/approval?user_id={user_id}&event_id={event_id}"
			response = await self.http_client.fetch(self.get_url(url))
			assert response.code == 200

			body = json.loads(response.body.decode("utf-8"))
			assert body["approved_status"] == "approved"

		finally:
			cursor.execute("DELETE FROM participants WHERE user_id = %s AND event_id = %s;", (user_id, event_id))
			cursor.execute("DELETE FROM events WHERE id = %s;", (event_id,))
			cursor.execute("DELETE FROM clubs WHERE id = %s;", (club_id,))
			cursor.execute("DELETE FROM users WHERE id = %s;", (user_id,))
			conn.commit()
			cursor.close()
			conn.close()
