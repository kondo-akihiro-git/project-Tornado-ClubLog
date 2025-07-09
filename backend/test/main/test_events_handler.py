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

        try:
            # ① ユーザー存在確認または作成
            print("Checking or creating user...")
            cursor.execute("SELECT id FROM users WHERE mail_address = %s;", ("eventcreate@example.com",))
            user_row = cursor.fetchone()
            if user_row:
                user_id = user_row[0]
                print(f"User exists with id={user_id}")
            else:
                cursor.execute("""
                    INSERT INTO users (username, mail_address, password)
                    VALUES ('eventcreateuser', 'eventcreate@example.com', 'dummy')
                    RETURNING id;
                """)
                user_id = cursor.fetchone()[0]
                conn.commit()
                print(f"Created new user with id={user_id}")

            # ② クラブ作成
            print("Creating club...")
            cursor.execute("""
                INSERT INTO clubs (name, owner_id)
                VALUES ('イベント作成クラブ', %s)
                RETURNING id;
            """, (user_id,))
            club_id = cursor.fetchone()[0]
            conn.commit()
            print(f"Created club with id={club_id}")

            # 事前に同じタイトルのイベントがあれば削除
            test_title = "テストイベント"
            print(f"Deleting existing events titled '{test_title}' if any...")
            self.delete_event_by_title(test_title)

            test_scheduled_at = "2025-08-01 18:00:00"

            # ③ API呼び出し
            print("Calling POST /events...")
            payload = {
                "title": test_title,
                "club_id": club_id,
                "scheduled_at": test_scheduled_at
            }
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

        finally:
            # 後片付け：追加したイベント、クラブ、ユーザーを削除（ユーザーは既存の場合は削除しない）
            print("Cleaning up...")
            cursor.execute("DELETE FROM events WHERE id = %s;", (body.get("id"),))
            cursor.execute("DELETE FROM clubs WHERE id = %s;", (club_id,))

            # ユーザーは既存か新規か判定して削除
            cursor.execute("SELECT id FROM users WHERE mail_address = %s;", ("eventcreate@example.com",))
            user_row = cursor.fetchone()
            if user_row and user_row[0] == user_id:
                print(f"Deleting test user id={user_id}")
                cursor.execute("DELETE FROM users WHERE id = %s;", (user_id,))

            conn.commit()
            cursor.close()
            conn.close()
            print("=== test_create_event end ===")


    @gen_test
    async def test_get_event(self):
        conn = get_connection()
        cursor = conn.cursor()

        try:
            # ① ユーザー作成
            cursor.execute("""
                INSERT INTO users (username, mail_address, password)
                VALUES ('eventgetuser', 'eventget@example.com', 'dummy')
                RETURNING id;
            """)
            user_id = cursor.fetchone()[0]

            # ② クラブ作成
            cursor.execute("""
                INSERT INTO clubs (name, owner_id)
                VALUES ('イベント取得クラブ', %s)
                RETURNING id;
            """, (user_id,))
            club_id = cursor.fetchone()[0]

            # ③ イベント作成
            cursor.execute("""
                INSERT INTO events (title, club_id)
                VALUES ('イベントGETテスト', %s)
                RETURNING id;
            """, (club_id,))
            event_id = cursor.fetchone()[0]

            # ④ リンク作成
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
            # 後片付け
            cursor.execute("DELETE FROM links WHERE event_id = %s;", (event_id,))
            cursor.execute("DELETE FROM events WHERE id = %s;", (event_id,))
            cursor.execute("DELETE FROM clubs WHERE id = %s;", (club_id,))
            cursor.execute("DELETE FROM users WHERE id = %s;", (user_id,))
            conn.commit()
            cursor.close()
            conn.close()
