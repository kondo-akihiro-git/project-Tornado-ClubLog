# backend/api/handlers/auth_verify_handler.py
import tornado.web
import json
from backend.db.connection.connection import get_connection

class AuthHandler(tornado.web.RequestHandler):
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
            user_id = data.get("user_id")

            if not user_id:
                self.set_status(400)
                self.write({"error": "user_id は必須です"})
                return

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT id, username, user_role FROM users WHERE id = %s", (user_id,))
            user = cursor.fetchone()

            if user:
                self.write({
                    "user_id": user[0],
                    "username": user[1],
                    "user_role": user[2]
                })
            else:
                self.set_status(401)
                self.write({"error": "無効なユーザーIDです"})

        except Exception as e:
            self.set_status(500)
            self.write({"error": str(e)})
        finally:
            if 'cursor' in locals(): cursor.close()
            if 'conn' in locals(): conn.close()
