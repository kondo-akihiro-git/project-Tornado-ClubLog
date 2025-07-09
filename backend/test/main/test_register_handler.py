from tornado.testing import AsyncHTTPTestCase, gen_test
import json
from backend.api.main import make_app
from backend.db.connection.connection import get_connection

class TestRegisterHandler(AsyncHTTPTestCase):
    def get_app(self):
        return make_app()

    @gen_test
    async def test_register_user_and_participant(self):
        conn = get_connection()
        cursor = conn.cursor()

        try:
            # --- 1. ユーザー作成または取得（同じメールが既にあれば使う） ---
            mail_address = "testuser1@example.com"
            cursor.execute("SELECT id FROM users WHERE mail_address = %s;", (mail_address,))
            row = cursor.fetchone()
            if row:
                user_id = row[0]
                is_user_new = False
            else:
                cursor.execute("""
                    INSERT INTO users (username, mail_address, password)
                    VALUES ('testuser1', %s, 'dummy')
                    RETURNING id;
                """, (mail_address,))
                user_id = cursor.fetchone()[0]
                is_user_new = True

            # --- 2. クラブ作成 ---
            cursor.execute("""
                INSERT INTO clubs (name, owner_id)
                VALUES ('テストクラブ', %s)
                RETURNING id;
            """, (user_id,))
            club_id = cursor.fetchone()[0]

            # --- 3. イベント作成 ---
            cursor.execute("""
                INSERT INTO events (title, club_id)
                VALUES ('テストイベント', %s)
                RETURNING id;
            """, (club_id,))
            event_id = cursor.fetchone()[0]

            conn.commit()

            # --- 4. API呼び出し（参加登録） ---
            payload = {
                "mail_address": mail_address,
                "event_id": event_id
            }

            response = await self.http_client.fetch(
                self.get_url("/register"),
                method="POST",
                headers={"Content-Type": "application/json"},
                body=json.dumps(payload)
            )

            assert response.code == 201
            body = json.loads(response.body.decode("utf-8"))
            assert "登録が完了しました" in body["message"]

        finally:
            # --- 後片付け：自分で追加したデータだけ削除 ---
            cursor.execute("DELETE FROM participants WHERE user_id = %s AND event_id = %s;", (user_id, event_id))
            cursor.execute("DELETE FROM events WHERE id = %s;", (event_id,))
            cursor.execute("DELETE FROM clubs WHERE id = %s;", (club_id,))
            if is_user_new:
                cursor.execute("DELETE FROM users WHERE id = %s;", (user_id,))
            conn.commit()
            cursor.close()
            conn.close()
