# api/handlers/user_handler.py
import tornado.web
from backend.db.connection.connection import get_connection

class UserHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")

    async def get(self, user_id):
        try:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT id, username, mail_address, updated_at
                FROM users
                WHERE id = %s;
            """, (user_id,))

            row = cursor.fetchone()

            if row:
                user = {
                    "id": row[0],
                    "username": row[1],
                    "mail_address": row[2],
                    "updated_at": row[3].isoformat() if row[3] else None
                }
                self.write(user)
            else:
                self.set_status(404)
                self.write({"error": "User not found"})

        except Exception as e:
            self.set_status(500)
            self.write({"error": str(e)})

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()