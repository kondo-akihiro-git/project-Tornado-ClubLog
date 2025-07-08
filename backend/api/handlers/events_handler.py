import tornado.web
import json
from backend.db.connection.connection import get_connection

class EventsHandler(tornado.web.RequestHandler):
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
            title = data.get("title")
            club_id = data.get("club_id")
            scheduled_at = data.get("scheduled_at")  # nullable

            if not title or not club_id:
                self.set_status(400)
                self.write({"error": "titleとclub_idは必須です"})
                return

            conn = get_connection()
            cursor = conn.cursor()

            # 既存のイベントを探す（title, club_id, scheduled_at）
            cursor.execute("""
                SELECT id FROM events
                WHERE title = %s AND club_id = %s AND
                      (scheduled_at = %s OR (scheduled_at IS NULL AND %s IS NULL))
            """, (title, club_id, scheduled_at, scheduled_at))

            existing = cursor.fetchone()

            if existing:
                event_id = existing[0]
                # 更新（scheduled_at だけ更新される可能性がある）
                cursor.execute("""
                    UPDATE events
                    SET title = %s, club_id = %s, scheduled_at = %s
                    WHERE id = %s
                    RETURNING id, title, club_id, scheduled_at, created_at;
                """, (title, club_id, scheduled_at, event_id))
                row = cursor.fetchone()
                self.set_status(200)  # OK
            else:
                # 挿入
                cursor.execute("""
                    INSERT INTO events (title, club_id, scheduled_at)
                    VALUES (%s, %s, %s)
                    RETURNING id, title, club_id, scheduled_at, created_at;
                """, (title, club_id, scheduled_at))
                row = cursor.fetchone()
                self.set_status(201)  # Created

            conn.commit()

            self.write({
                "id": row[0],
                "title": row[1],
                "club_id": row[2],
                "scheduled_at": row[3].isoformat() if row[3] else None,
                "created_at": row[4].isoformat()
            })

        except Exception as e:
            self.set_status(500)
            self.write({"error": str(e)})
        finally:
            if cursor: cursor.close()
            if conn: conn.close()
