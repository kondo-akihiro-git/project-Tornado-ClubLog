# /backend/api/handlers/events_handler.py
import datetime
import tornado.web
import json
from backend.db.connection.connection import get_connection

class EventsHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Content-Type", "application/json")
        self.set_header("Access-Control-Allow-Headers", "content-type")
        self.set_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")

    async def options(self):
        self.set_status(204)
        self.finish()

    async def post(self):
        try:
            data = json.loads(self.request.body.decode("utf-8"))
            title = data.get("title")
            club_id = data.get("club_id")
            scheduled_at_str = data.get("scheduled_at")
            scheduled_at = None

            if not title or not club_id:
                self.set_status(400)
                self.write({"error": "titleとclub_idは必須です"})
                return

            if scheduled_at_str:
                try:
                    scheduled_at = datetime.datetime.strptime(scheduled_at_str, "%Y-%m-%d %H:%M:%S")
                except ValueError:
                    try:
                        scheduled_at = datetime.datetime.fromisoformat(scheduled_at_str)
                    except Exception:
                        self.set_status(400)
                        self.write({"error": f"scheduled_atの形式が不正です: {scheduled_at_str}"})
                        return

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT id FROM events
                WHERE title = %s AND club_id = %s AND
                    (scheduled_at = %s OR (scheduled_at IS NULL AND %s IS NULL))
            """, (title, club_id, scheduled_at, scheduled_at))

            existing = cursor.fetchone()

            if existing:
                event_id = existing[0]
                cursor.execute("""
                    UPDATE events
                    SET title = %s, club_id = %s, scheduled_at = %s
                    WHERE id = %s
                    RETURNING id, title, club_id, scheduled_at, created_at;
                """, (title, club_id, scheduled_at, event_id))
                row = cursor.fetchone()
                self.set_status(200)
            else:
                cursor.execute("""
                    INSERT INTO events (title, club_id, scheduled_at)
                    VALUES (%s, %s, %s)
                    RETURNING id, title, club_id, scheduled_at, created_at;
                """, (title, club_id, scheduled_at))
                row = cursor.fetchone()
                self.set_status(201)

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



    async def get(self):
        token = self.get_argument("token", None)
        if not token:
            self.set_status(400)
            self.write({"error": "tokenパラメータが必要です"})
            return

        try:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT e.id, e.title, e.scheduled_at
                FROM links l
                JOIN events e ON l.event_id = e.id
                WHERE l.url_token = %s;
            """, (token,))

            row = cursor.fetchone()
            if row:
                self.write({
                    "event_id": row[0],
                    "title": row[1],
                    "scheduled_at": row[2].isoformat() if row[2] else None
                })
            else:
                self.set_status(404)
                self.write({"error": "該当するイベントが見つかりません"})

        except Exception as e:
            self.set_status(500)
            self.write({"error": str(e)})
        finally:
            if cursor: cursor.close()
            if conn: conn.close()
