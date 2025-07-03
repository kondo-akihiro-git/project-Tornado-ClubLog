# api/handlers/user_handler.py
import tornado.web
from backend.db.connection.connection import get_connection

class UsersHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")

    async def get(self):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, username, mail_address, user_role, updated_at
                FROM users
                ORDER BY id;
            """)
            rows = cursor.fetchall()
            result = [
                {
                    "id": row[0],
                    "username": row[1],
                    "mail_address": row[2],
                    "user_role": row[3],
                    "updated_at": row[4].isoformat()
                }
                for row in rows
            ]
            self.write({"users": result})
        except Exception as e:
            self.set_status(500)
            self.write({"error": str(e)})
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
