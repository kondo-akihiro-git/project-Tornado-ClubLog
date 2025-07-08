from tornado.testing import AsyncHTTPTestCase, gen_test
import json
from backend.api.main import make_app
from backend.db.connection.connection import get_connection

class TestEventsHandler(AsyncHTTPTestCase):
    def get_app(self):
        return make_app()

    def delete_event_by_title(self, title):
        """指定されたタイトルのイベントを削除（主にテスト前後で使用）"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM events WHERE title = %s;", (title,))
        conn.commit()
        cursor.close()
        conn.close()

    @gen_test
    async def test_create_event(self):
        test_title = "テストイベント"
        test_club_id = 1
        test_scheduled_at = "2025-08-01T18:00:00"

        self.delete_event_by_title(test_title)

        payload = {
            "title": test_title,
            "club_id": test_club_id,
            "scheduled_at": test_scheduled_at
        }
        response = await self.http_client.fetch(
            self.get_url("/events"),
            method="POST",
            headers={"Content-Type": "application/json"},
            body=json.dumps(payload)
        )

        assert response.code == 201
        body = json.loads(response.body.decode("utf-8"))
        assert body["title"] == test_title
        assert body["club_id"] == test_club_id
        assert body["scheduled_at"] == test_scheduled_at

        self.delete_event_by_title(test_title)
