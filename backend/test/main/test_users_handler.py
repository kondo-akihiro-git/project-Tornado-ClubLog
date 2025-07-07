# test/test_user_handler.py
import tornado.web
from tornado.testing import AsyncHTTPTestCase, gen_test
import tornado.escape
import logging
from backend.api.handlers.users_handler import UsersHandler
from backend.api.main import make_app

logger = logging.getLogger(__name__)

class TestUsersHandler(AsyncHTTPTestCase):
    def get_app(self):
        return make_app() 

    @gen_test
    async def test_get_users(self):
        response = await self.http_client.fetch(self.get_url("/users"))
        assert response.code == 200
