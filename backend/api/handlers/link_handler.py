# api/handlers/link_handler.py
import tornado.web
import json
from backend.db.connection.connection import get_connection

class LinkHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Content-Type", "application/json")
        self.set_header("Access-Control-Allow-Headers", "content-type")
        self.set_header("Access-Control-Allow-Methods", "POST, OPTIONS")

    async def options(self):
        # CORSプリフライト用の空レスポンス
        self.set_status(204)
        self.finish()

    async def post(self):
        try:
            data = json.loads(self.request.body.decode("utf-8"))
            url = data.get("url")
            event_id = data.get("event_id")

            if not url or not event_id:
                self.set_status(400)
                self.write({"error": "urlとevent_idは必須です"})
                return

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT id FROM links WHERE event_id = %s;", (event_id,))
            if cursor.fetchone():
                self.set_status(409)
                self.write({"error": "このイベントには既にリンクが存在します"})
                return

            cursor.execute("""
                INSERT INTO links (url, event_id)
                VALUES (%s, %s)
                RETURNING id, url, event_id, created_at;
            """, (url, event_id))
            result = cursor.fetchone()
            conn.commit()

            self.set_status(201)
            self.write({
                "id": result[0],
                "url": result[1],
                "event_id": result[2],
                "created_at": result[3].isoformat()
            })

        except Exception as e:
            self.set_status(500)
            self.write({"error": str(e)})

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
