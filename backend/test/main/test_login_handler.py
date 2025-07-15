from tornado.testing import AsyncHTTPTestCase, gen_test
from backend.api.main import make_app
from backend.db.connection.connection import get_connection
import json

class TestLoginHandler(AsyncHTTPTestCase):
    def get_app(self):
        return make_app()

    @gen_test
    async def test_login_success_and_failure(self):
        conn = get_connection()
        cursor = conn.cursor()

        try:
            # ユーザー作成
            cursor.execute("""
                INSERT INTO users (username, mail_address, password)
                VALUES ('LoginUser', 'login@example.com', 'password123')
                RETURNING id;
            """)
            user_id = cursor.fetchone()[0]
            conn.commit()

            # 成功ケース
            response = await self.http_client.fetch(
                self.get_url("/login"),
                method="POST",
                headers={"Content-Type": "application/json"},
                body=json.dumps({
                    "mail_address": "login@example.com",
                    "password": "password123"
                })
            )
            assert response.code == 200
            body = json.loads(response.body.decode("utf-8"))
            assert body["user_id"] == user_id
            assert body["username"] == "LoginUser"

            # 失敗ケース
            response = await self.http_client.fetch(
                self.get_url("/login"),
                method="POST",
                headers={"Content-Type": "application/json"},
                body=json.dumps({
                    "mail_address": "login@example.com",
                    "password": "wrongpassword"
                }),
                raise_error=False
            )
            assert response.code == 401

        finally:
            cursor.execute("DELETE FROM users WHERE id = %s;", (user_id,))
            conn.commit()
            cursor.close()
            conn.close()
