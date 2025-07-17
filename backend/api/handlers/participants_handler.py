# backend/api/handlers/participants_handler.py
import tornado.web
import json
from backend.db.connection.connection import get_connection
from collections import defaultdict

class ParticipantsHandler(tornado.web.RequestHandler):
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
            data = json.loads(self.request.body)
            owner_id = data.get("owner_id")
            if not owner_id:
                self.set_status(400)
                self.write({"error": "owner_id は必須です"})
                return

            conn = get_connection()
            cursor = conn.cursor()

            # owner_id で制限をかけて取得
            cursor.execute("""
                SELECT
                    c.id AS club_id,
                    c.name AS club_name,
                    e.id AS event_id,
                    e.title AS event_title,
                    u.id AS user_id,
                    u.username,
                    u.mail_address
                FROM clubs c
                JOIN events e ON c.id = e.club_id
                LEFT JOIN participants p ON e.id = p.event_id
                LEFT JOIN users u ON p.user_id = u.id
                WHERE c.owner_id = %s
                ORDER BY c.id, e.id;
            """, (owner_id,))

            rows = cursor.fetchall()

            clubs_dict = defaultdict(lambda: {"club_name": "", "events": {}})
            for row in rows:
                club_id, club_name, event_id, event_title, user_id, username, mail_address = row
                club = clubs_dict[club_id]
                club["club_name"] = club_name
                event = club["events"].setdefault(event_id, {
                    "event_id": event_id,
                    "title": event_title,
                    "participants": []
                })
                if username and mail_address:
                    event["participants"].append({
                        "user_id": user_id,
                        "username": username,
                        "mail_address": mail_address
                    })

            result = [{
                "club_name": club["club_name"],
                "events": list(club["events"].values())
            } for club in clubs_dict.values()]

            self.write({"clubs": result})

        except Exception as e:
            self.set_status(500)
            self.write({"error": str(e)})
        finally:
            if 'cursor' in locals(): cursor.close()
            if 'conn' in locals(): conn.close()
