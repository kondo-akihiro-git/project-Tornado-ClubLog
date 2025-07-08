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
        self.set_status(204)
        self.finish()

    async def post(self):
        try:
            data = json.loads(self.request.body.decode("utf-8"))
            url_token = data.get("url_token")
            event_id = data.get("event_id")

            if not url_token or not event_id:
                self.set_status(400)
                self.write({"error": "url_tokenとevent_idは必須です"})
                return

            conn = get_connection()
            cursor = conn.cursor()

            # 既存リンクをチェック
            cursor.execute("SELECT id FROM links WHERE event_id = %s;", (event_id,))
            existing = cursor.fetchone()

            if existing:
                # 更新
                cursor.execute("""
                    UPDATE links
                    SET url_token = %s, created_at = CURRENT_TIMESTAMP AT TIME ZONE 'Asia/Tokyo'
                    WHERE event_id = %s
                    RETURNING id, url_token, event_id, created_at;
                """, (url_token, event_id))
                result = cursor.fetchone()
                self.set_status(200)
            else:
                # 新規登録
                cursor.execute("""
                    INSERT INTO links (url_token, event_id)
                    VALUES (%s, %s)
                    RETURNING id, url_token, event_id, created_at;
                """, (url_token, event_id))
                result = cursor.fetchone()
                self.set_status(201)

            conn.commit()

            self.write({
                "id": result[0],
                "url_token": result[1],
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
