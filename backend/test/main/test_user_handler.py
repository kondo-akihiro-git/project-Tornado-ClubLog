# test/test_user_handler.py
import tornado.web
from tornado.testing import AsyncHTTPTestCase, gen_test
from backend.api.handlers.user_handler import UserHandler
import json
import logging

from backend.api.main import make_app
from backend.db.connection.connection import get_connection

logger = logging.getLogger(__name__)

class TestUserHandler(AsyncHTTPTestCase):
    def get_app(self):
        return make_app() 

    @gen_test
    async def test_get_existing_user(self):
        # NOTE: DBに実際に user_id=1 のユーザーが存在する必要があります。
        response = await self.http_client.fetch(self.get_url("/user/1/info"))
        assert response.code == 200

        data = json.loads(response.body)
        assert "id" in data
        assert data["id"] == 1
        assert "username" in data
        assert "mail_address" in data

    @gen_test
    async def test_get_nonexistent_user(self):
        # 存在しないユーザーIDを指定（例: 99999）
        try:
            await self.http_client.fetch(self.get_url("/user/99999/info"))
        except Exception as e:
            response = e.response
            assert response.code == 404
            data = json.loads(response.body)
            assert data["error"] == "User not found"

    def create_user_for_test(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO users (username, mail_address, password)
            VALUES ('テストユーザー', 'test@example.com', 'oldpass')
            RETURNING id;
        """)
        user_id = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        conn.close()
        return user_id

    def delete_user_by_id(self, user_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE id = %s;", (user_id,))
        conn.commit()
        cursor.close()
        conn.close()

    @gen_test
    async def test_update_user_settings(self):
        user_id = self.create_user_for_test()

        payload = {
            "username": "新しい名前",
            "password": "newpass"
        }

        response = await self.http_client.fetch(
            self.get_url(f"/user/{user_id}"),
            method="POST",
            headers={"Content-Type": "application/json"},
            body=json.dumps(payload)
        )

        assert response.code == 200
        data = json.loads(response.body)
        assert data["message"] == "ユーザー情報を更新しました"

        # 内容確認
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT username, password FROM users WHERE id = %s;", (user_id,))
        row = cursor.fetchone()
        assert row[0] == "新しい名前"
        assert row[1] == "newpass"

        cursor.close()
        conn.close()

        self.delete_user_by_id(user_id)