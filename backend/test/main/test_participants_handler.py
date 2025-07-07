# test/test_participants_handler.py
import tornado.web
from backend.api.handlers.participants_handler import ParticipantsHandler
from tornado.testing import AsyncHTTPTestCase, gen_test
import logging

from backend.api.main import make_app

logger = logging.getLogger(__name__)

class TestParticipantsHandler(AsyncHTTPTestCase):
    def get_app(self):
                return make_app() 

    @gen_test
    async def test_get_participants(self):
        response = await self.http_client.fetch(self.get_url("/participants"))
        assert response.code == 200