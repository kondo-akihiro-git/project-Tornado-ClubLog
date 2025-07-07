# test/test_user_handler.py
import tornado.web
from tornado.testing import AsyncHTTPTestCase, gen_test
from backend.api.handlers.user_handler import UserHandler
import json
import logging

from backend.api.main import make_app

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
