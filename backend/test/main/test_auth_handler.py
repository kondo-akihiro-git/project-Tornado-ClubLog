# test/test_auth_verify_handler.py
import tornado.web
from tornado.testing import AsyncHTTPTestCase, gen_test
import json
import logging
from backend.api.main import make_app

logger = logging.getLogger(__name__)

class TestAuthHandler(AsyncHTTPTestCase):
    def get_app(self):
        return make_app()

    @gen_test
    async def test_valid_user_auth(self):
        # 前提: このIDがテストDBに存在している必要があります
        payload = {"user_id": 1}
        response = await self.http_client.fetch(
            self.get_url("/auth"),
            method="POST",
            headers={"Content-Type": "application/json"},
            body=json.dumps(payload)
        )
        assert response.code == 200
        data = json.loads(response.body)
        assert data["user_id"] == 1
        assert "username" in data
        assert "user_role" in data

    @gen_test
    async def test_invalid_user_id(self):
        payload = {"user_id": 999999}  # 存在しないID
        response = await self.http_client.fetch(
            self.get_url("/auth"),
            method="POST",
            headers={"Content-Type": "application/json"},
            body=json.dumps(payload),
            raise_error=False  # エラーコードでも例外にしない
        )
        assert response.code == 401
        data = json.loads(response.body)
        assert data["error"] == "無効なユーザーIDです"

    @gen_test
    async def test_missing_user_id(self):
        payload = {}  # user_id なし
        response = await self.http_client.fetch(
            self.get_url("/auth"),
            method="POST",
            headers={"Content-Type": "application/json"},
            body=json.dumps(payload),
            raise_error=False
        )
        assert response.code == 400
        data = json.loads(response.body)
        assert data["error"] == "user_id は必須です"
