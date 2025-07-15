import tornado.web
import json
from backend.db.connection.connection import get_connection

class ApprovalHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Content-Type", "application/json")
        self.set_header("Access-Control-Allow-Headers", "content-type")
        self.set_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")

    async def options(self):
        self.set_status(204)
        self.finish()

    async def post(self):
        conn = None 
        cursor = None 
        try:
            data = json.loads(self.request.body.decode("utf-8"))
            user_id = data.get("user_id")
            event_id = data.get("event_id")
            status = data.get("status")

            if not user_id or not event_id or status not in ("approved", "rejected"):
                self.set_status(400)
                self.write({"error": "user_id, event_id, status（'approved'または'rejected'）が必要です"})
                return

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE participants
                SET approved_status = %s
                WHERE user_id = %s AND event_id = %s
            """, (status, user_id, event_id))

            if cursor.rowcount == 0:
                self.set_status(404)
                self.write({"error": "対象の参加者が見つかりません"})
            else:
                conn.commit()
                self.set_status(200)
                self.write({"message": f"ステータスを'{status}'に更新しました"})

        except Exception as e:
            self.set_status(500)
            self.write({"error": str(e)})
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    async def get(self):
        conn = None 
        cursor = None 
        try:
            user_id = self.get_query_argument("user_id", None)
            event_id = self.get_query_argument("event_id", None)

            if not user_id or not event_id:
                self.set_status(400)
                self.write({"error": "user_idとevent_idは必須です"})
                return

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT approved_status FROM participants
                WHERE user_id = %s AND event_id = %s;
            """, (user_id, event_id))
            row = cursor.fetchone()

            # 存在しない参加情報でも pending と返す
            if row:
                status = row[0]
            else:
                status = "pending"

            self.set_status(200)
            self.write({"approved_status": status})

        except Exception as e:
            self.set_status(500)
            self.write({"error": str(e)})
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
