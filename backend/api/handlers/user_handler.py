# api/handlers/user_handler.py
import datetime
import json
import pytz
import tornado.web
from backend.db.connection.connection import get_connection

class UserHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Content-Type", "application/json")
        self.set_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.set_header("Access-Control-Allow-Headers", "Content-Type")

    async def options(self, user_id):
        self.set_status(204)
        self.finish()

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


    async def post(self, user_id):
        try:
            data = json.loads(self.request.body.decode("utf-8"))
            username = data.get("username")
            password = data.get("password")

            if not username or not password:
                self.set_status(400)
                self.write({"error": "usernameまたはpasswordのいずれかを指定してください"})
                return

            conn = get_connection()
            cursor = conn.cursor()

            if username:
                cursor.execute("""
                    UPDATE users
                    SET username = %s,
                        updated_at = (now() AT TIME ZONE 'Asia/Tokyo')
                    WHERE id = %s;
                """, (username, user_id))

            if password:
                cursor.execute("""
                    UPDATE users
                    SET password = %s,
                        updated_at = (now() AT TIME ZONE 'Asia/Tokyo')
                    WHERE id = %s;
                """, (password, user_id))

            conn.commit()
            self.set_status(200)
            self.write({"message": "ユーザー情報を更新しました"})

        except Exception as e:
            self.set_status(500)
            self.write({"error": str(e)})
        
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
