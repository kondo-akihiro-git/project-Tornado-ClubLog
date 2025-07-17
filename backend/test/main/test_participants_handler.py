# test/test_participants_handler.py
import tornado.web
from tornado.testing import AsyncHTTPTestCase, gen_test
import json
from backend.api.main import make_app

class TestParticipantsHandler(AsyncHTTPTestCase):
    def get_app(self):
        return make_app()

    @gen_test
    async def test_post_participants(self):
        # テスト用のオーナーID（DBに存在するIDを使う必要あり、例: 1）
        body = json.dumps({ "owner_id": 1 })

        response = await self.http_client.fetch(
            self.get_url("/participants"),
            method="POST",
            headers={"Content-Type": "application/json"},
            body=body
        )

        assert response.code == 200

        # 内容検証（例：clubsが含まれているか）
        data = json.loads(response.body.decode())
        assert "clubs" in data
        assert isinstance(data["clubs"], list)
