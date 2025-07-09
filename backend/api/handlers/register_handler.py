import tornado.web
import json
from backend.db.connection.connection import get_connection

class RegisterHandler(tornado.web.RequestHandler):
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
            data = json.loads(self.request.body.decode("utf-8"))
            mail_address = data.get("mail_address")
            event_id = data.get("event_id")

            if not mail_address or not event_id:
                self.set_status(400)
                self.write({"error": "mail_addressとevent_idは必須です"})
                return

            conn = get_connection()
            cursor = conn.cursor()

            # ユーザーが存在することを前提に取得
            cursor.execute("SELECT id FROM users WHERE mail_address = %s;", (mail_address,))
            user = cursor.fetchone()

            if not user:
                self.set_status(400)
                self.write({"error": "登録前にユーザー確認が必要です"})
                return

            user_id = user[0]

            # 参加者登録（重複登録は無視）
            cursor.execute("""
                INSERT INTO participants (user_id, event_id)
                VALUES (%s, %s)
                ON CONFLICT (user_id, event_id) DO NOTHING;
            """, (user_id, event_id))

            conn.commit()
            self.set_status(201)
            self.write({"message": "登録が完了しました"})

        except Exception as e:
            self.set_status(500)
            self.write({"error": str(e)})
        finally:
            if cursor: cursor.close()
            if conn: conn.close()
