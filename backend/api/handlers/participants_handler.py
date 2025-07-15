# api/handlers/participants_handler.py
import tornado.web
from backend.db.connection.connection import get_connection
from collections import defaultdict

class ParticipantsHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")

    async def get(self):
        try:
            conn = get_connection()
            cursor = conn.cursor()

            # JOIN: clubs → events → participants → users
            cursor.execute("""
                SELECT
                    c.id AS club_id,
                    c.name AS club_name,
                    e.id AS event_id,
                    e.title AS event_title,
                    u.id AS user_id, 
                    u.username,
                    u.mail_address
                FROM events e
                JOIN clubs c ON e.club_id = c.id
                LEFT JOIN participants p ON e.id = p.event_id
                LEFT JOIN users u ON p.user_id = u.id
                ORDER BY c.id, e.id;
            """)

            rows = cursor.fetchall()

            # ネスト構造を生成
            clubs_dict = defaultdict(lambda: {"club_name": "", "events": {}})
            for row in rows:
                club_id = row[0]
                club_name = row[1]
                event_id = row[2]
                event_title = row[3]
                user_id = row[4]
                username = row[5]
                mail_address = row[6]

                club = clubs_dict[club_id]
                club["club_name"] = club_name
                event = club["events"].setdefault(event_id, {
                    "event_id": event_id,
                    "title": event_title,
                    "participants": []
                })

                if username and mail_address:  # NULL参加者を除く
                    event["participants"].append({
                        "user_id": user_id,   
                        "username": username,
                        "mail_address": mail_address
                    })

            # dict → list形式に変換
            result = []
            for club in clubs_dict.values():
                result.append({
                    "club_name": club["club_name"],
                    "events": list(club["events"].values())
                })

            self.write({"clubs": result})

        except Exception as e:
            self.set_status(500)
            self.write({"error": str(e)})
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
