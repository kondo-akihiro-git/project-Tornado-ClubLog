import tornado.web
from tornado.testing import AsyncHTTPTestCase, gen_test
import json
import psycopg2
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
        url = "https://example.com/test_event_link"

        # 🔁 前処理：リンクを削除（同じevent_idが残っていないように）
        self.delete_link(event_id)

        # 📤 登録
        payload = {
            "url": url,
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
        assert body["url"] == url
        assert body["event_id"] == event_id

        # 🔁 後処理：登録したリンクを削除（テスト汚染防止）
        self.delete_link(event_id)
