from tornado.testing import AsyncHTTPTestCase, gen_test
import json
from backend.api.main import make_app
from backend.db.connection.connection import get_connection


class TestVerifyHandler(AsyncHTTPTestCase):
    def get_app(self):
        return make_app()

    def setUp(self):
        super().setUp()
        self.conn = get_connection()
        self.cursor = self.conn.cursor()

        # ユーザー1人作成（検証用）
        self.test_user = {
            "username": "テスト太郎",
            "mail_address": "verifyuser@example.com",
            "password": "password"
        }
        self.cursor.execute("""
            INSERT INTO users (username, mail_address, password)
            VALUES (%s, %s, %s)
            RETURNING id;
        """, (self.test_user["username"], self.test_user["mail_address"], self.test_user["password"]))
        self.user_id = self.cursor.fetchone()[0]
        self.conn.commit()

    def tearDown(self):
        self.cursor.execute("DELETE FROM users WHERE mail_address = %s;", (self.test_user["mail_address"],))
        self.conn.commit()
        self.cursor.close()
        self.conn.close()
        super().tearDown()

    @gen_test
    async def test_verify_existing_user(self):
        """既存ユーザーの照合テスト"""
        payload = {"mail_address": self.test_user["mail_address"]}

        response = await self.http_client.fetch(
            self.get_url("/verify"),
            method="POST",
            headers={"Content-Type": "application/json"},
            body=json.dumps(payload)
        )

        assert response.code == 200
        body = json.loads(response.body.decode("utf-8"))
        assert body["exists"] is True
        assert body["username"] == self.test_user["username"]

    @gen_test
    async def test_verify_nonexistent_user(self):
        """存在しないユーザーの照合テスト"""
        payload = {"mail_address": "nonexistent@example.com"}

        response = await self.http_client.fetch(
            self.get_url("/verify"),
            method="POST",
            headers={"Content-Type": "application/json"},
            body=json.dumps(payload)
        )

        assert response.code == 200
        body = json.loads(response.body.decode("utf-8"))
        assert body["exists"] is False

    @gen_test
    async def test_verify_missing_mail_address(self):
        """必須パラメータがない場合のテスト"""
        payload = {}

        response = await self.http_client.fetch(
            self.get_url("/verify"),
            method="POST",
            headers={"Content-Type": "application/json"},
            body=json.dumps(payload),
            raise_error=False  # 400 を受け取るため
        )

        assert response.code == 400
        body = json.loads(response.body.decode("utf-8"))
        assert "mail_address は必須です" in body["error"]
