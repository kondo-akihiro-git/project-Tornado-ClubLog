# backend/api/handlers/records_handler.py
import tornado.web
from backend.db.connection.connection import get_connection

class RecordsHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")

    async def get(self, user_id):
        
        try:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT
                    c.name AS club_name,
                    p.joined_at
                FROM participants p
                JOIN events e ON p.event_id = e.id
                JOIN clubs c ON e.club_id = c.id
                WHERE p.user_id = %s
                ORDER BY p.joined_at DESC;
            """, (user_id,))

            rows = cursor.fetchall()
            result = [
                {
                    "club_name": row[0],
                    "joined_at": row[1].isoformat()
                }
                for row in rows
            ]

            self.write({"records": result})

        except Exception as e:
            self.set_status(500)
            self.write({"error": str(e)})
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()