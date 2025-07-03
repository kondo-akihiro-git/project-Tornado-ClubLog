# test/test_participants_handler.py
import tornado.web
from backend.api.handlers.participants_handler import ParticipantsHandler
from tornado.testing import AsyncHTTPTestCase, gen_test
import logging

logger = logging.getLogger(__name__)

class TestParticipantsHandler(AsyncHTTPTestCase):
    def get_app(self):
        return tornado.web.Application([
            (r"/participants", ParticipantsHandler)
        ])

    @gen_test
    async def test_get_participants(self):
        response = await self.http_client.fetch(self.get_url("/participants"))
        assert response.code == 200