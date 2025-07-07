# test/test_records_handler.py
import tornado.web
from tornado.testing import AsyncHTTPTestCase, gen_test
import logging
from backend.api.handlers.records_handler import RecordsHandler
from backend.api.main import make_app

logger = logging.getLogger(__name__)

class TestRecordsHandler(AsyncHTTPTestCase):
    def get_app(self):
                return make_app() 

    @gen_test
    async def test_get_records(self):
        response = await self.http_client.fetch(self.get_url("/user/1/records"))
        assert response.code == 200
        body = response.body.decode("utf-8")
        logger.info(f"Response body: {body}")
