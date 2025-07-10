import tornado
from tornado.testing import AsyncHTTPTestCase, gen_test
import json
from backend.api.main import make_app
from backend.db.connection.connection import get_connection

class TestEventsHandler(AsyncHTTPTestCase):
    def get_app(self):
        return make_app()

    def delete_event_by_title(self, title):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM events WHERE title = %s;", (title,))
        conn.commit()
        cursor.close()
        conn.close()


    @gen_test
    async def test_create_event(self):
        print("=== test_create_event start ===")
        conn = get_connection()
        cursor = conn.cursor()

        user_id = 99997
        club_id = 99987
        test_title = "テストイベント"
        test_scheduled_at = "2025-08-01 18:00:00"

        try:
            # ユーザー削除＆作成
            cursor.execute("DELETE FROM users WHERE id = %s;", (user_id,))
            cursor.execute("""
                INSERT INTO users (id, username, mail_address, password)
                VALUES (%s, 'eventcreateuser', 'eventcreate@example.com', 'dummy')
            """, (user_id,))

            # クラブ削除＆作成
            cursor.execute("DELETE FROM clubs WHERE id = %s;", (club_id,))
            cursor.execute("""
                INSERT INTO clubs (id, name, owner_id)
                VALUES (%s, 'イベント作成クラブ', %s)
            """, (club_id, user_id))

            # 同タイトルのイベント削除
            cursor.execute("DELETE FROM events WHERE title = %s AND club_id = %s;", (test_title, club_id))

            # シーケンスのリセット（最大IDを取得してセット）
            cursor.execute("SELECT setval('events_id_seq', (SELECT COALESCE(MAX(id), 1) FROM events));")

            conn.commit()

            print("Calling POST /events...")
            payload = {
                "title": test_title,
                "club_id": club_id,
                "scheduled_at": test_scheduled_at
            }

            try:
                response = await self.http_client.fetch(
                    self.get_url("/events"),
                    method="POST",
                    headers={"Content-Type": "application/json"},
                    body=json.dumps(payload)
                )
                print(f"Response code: {response.code}")
                body = json.loads(response.body.decode("utf-8"))
                print(f"Response body: {body}")

                assert response.code == 201
                assert body["title"] == test_title
                assert body["club_id"] == club_id
                assert body["scheduled_at"] == "2025-08-01T18:00:00"

                event_id = body["id"]

            except tornado.httpclient.HTTPClientError as e:
                if e.response:
                    error_body = e.response.body.decode("utf-8")
                    print(f"HTTP Error response body: {error_body}")
                else:
                    print(f"HTTP Error without response body: {str(e)}")
                raise

        finally:
            print("Cleaning up...")
            cursor.execute("DELETE FROM events WHERE title = %s AND club_id = %s;", (test_title, club_id))
            cursor.execute("DELETE FROM clubs WHERE id = %s;", (club_id,))
            cursor.execute("DELETE FROM users WHERE id = %s;", (user_id,))
            conn.commit()
            cursor.close()
            conn.close()
            print("=== test_create_event end ===")



    @gen_test
    async def test_get_event(self):
        conn = get_connection()
        cursor = conn.cursor()

        user_id = 99998
        club_id = 99988
        event_id = 99978

        try:
            # ユーザー作成
            cursor.execute("DELETE FROM users WHERE id = %s;", (user_id,))
            cursor.execute("""
                INSERT INTO users (id, username, mail_address, password)
                VALUES (%s, 'eventgetuser', 'eventget@example.com', 'dummy')
            """, (user_id,))

            # クラブ作成
            cursor.execute("DELETE FROM clubs WHERE id = %s;", (club_id,))
            cursor.execute("""
                INSERT INTO clubs (id, name, owner_id)
                VALUES (%s, 'イベント取得クラブ', %s)
            """, (club_id, user_id))

            # イベント作成
            cursor.execute("DELETE FROM events WHERE id = %s;", (event_id,))
            cursor.execute("""
                INSERT INTO events (id, title, club_id)
                VALUES (%s, 'イベントGETテスト', %s)
            """, (event_id, club_id))

            # リンク作成
            cursor.execute("DELETE FROM links WHERE event_id = %s;", (event_id,))
            cursor.execute("""
                INSERT INTO links (url_token, event_id)
                VALUES ('test-token', %s);
            """, (event_id,))

            conn.commit()

            # テスト実行
            response = await self.http_client.fetch(self.get_url("/events?token=test-token"))
            assert response.code == 200
            body = json.loads(response.body.decode("utf-8"))
            assert body["event_id"] == event_id
            assert body["title"] == "イベントGETテスト"

        finally:
            # 後片付け（順番に注意）
            cursor.execute("DELETE FROM links WHERE event_id = %s;", (event_id,))
            cursor.execute("DELETE FROM events WHERE id = %s;", (event_id,))
            cursor.execute("DELETE FROM clubs WHERE id = %s;", (club_id,))
            cursor.execute("DELETE FROM users WHERE id = %s;", (user_id,))
            conn.commit()
            cursor.close()
            conn.close()
