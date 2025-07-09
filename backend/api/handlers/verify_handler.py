import tornado.web
import json
from backend.db.connection.connection import get_connection

class VerifyHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Content-Type", "application/json")
        self.set_header("Access-Control-Allow-Headers", "content-type")
        self.set_header("Access-Control-Allow-Methods", "POST, OPTIONS")

    async def options(self):
        self.set_status(204)
        self.finish()

    async def post(self):
        conn = None
        cursor = None
        try:
            data = json.loads(self.request.body.decode("utf-8"))
            mail_address = data.get("mail_address")

            if not mail_address:
                self.set_status(400)
                self.write({"error": "mail_address は必須です"})
                return

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT username FROM users WHERE mail_address = %s;
            """, (mail_address,))
            row = cursor.fetchone()

            if row:
                self.write({"exists": True, "username": row[0]})
            else:
                self.write({"exists": False})

        except Exception as e:
            self.set_status(500)
            self.write({"error": str(e)})
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
