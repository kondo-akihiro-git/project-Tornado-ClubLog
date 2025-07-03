# api/handlers/participants_handler.py
import tornado.web
from backend.db.connection.connection import get_connection

class ParticipantsHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")

    async def get(self):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT participants.id, users.username, 
                clubs.event_name, participants.joined_at
                FROM participants
                JOIN users ON participants.user_id = users.id
                JOIN clubs ON participants.club_id = clubs.id
                ORDER BY participants.id;
            """)
            rows = cursor.fetchall()
            result = [
                {
                    "id": row[0],
                    "username": row[1],
                    "event_name": row[2],
                    "joined_at": row[3].isoformat()
                }
                for row in rows
            ]
            self.write({"participants": result})
        except Exception as e:
            self.set_status(500)
            self.write({"error": str(e)})
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
