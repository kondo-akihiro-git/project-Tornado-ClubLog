# test/test_user_handler.py
import tornado.web
from tornado.testing import AsyncHTTPTestCase, gen_test
import tornado.escape
import logging
from backend.api.handlers.users_handler import UsersHandler

logger = logging.getLogger(__name__)

class TestUsersHandler(AsyncHTTPTestCase):
    def get_app(self):
        return tornado.web.Application([
            (r"/users", UsersHandler)
        ])

    @gen_test
    async def test_get_users(self):
        response = await self.http_client.fetch(self.get_url("/users"))
        assert response.code == 200
        json_data = tornado.escape.json_decode(response.body)
        assert "users" in json_data
        assert isinstance(json_data["users"], list)
        logger.info(f"取得したユーザー数: {len(json_data['users'])}")
