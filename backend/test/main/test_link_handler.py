import tornado.web
from tornado.testing import AsyncHTTPTestCase, gen_test
import json
import uuid
from backend.api.main import make_app
from backend.db.connection.connection import get_connection

class TestLinkHandler(AsyncHTTPTestCase):
    def get_app(self):
        return make_app()

    def delete_link(self, event_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM links WHERE event_id = %s;", (event_id,))
        conn.commit()
        cursor.close()
        conn.close()

    @gen_test
    async def test_create_link(self):
        event_id = 1
        url_token = str(uuid.uuid4()) 

        self.delete_link(event_id)

        # 📤 登録
        payload = {
            "url_token": url_token, 
            "event_id": event_id
        }
        response = await self.http_client.fetch(
            self.get_url("/link"),
            method="POST",
            headers={"Content-Type": "application/json"},
            body=json.dumps(payload)
        )

        assert response.code == 201
        body = json.loads(response.body.decode("utf-8"))
        assert body["url_token"] == url_token 
        assert body["event_id"] == event_id

        self.delete_link(event_id)
