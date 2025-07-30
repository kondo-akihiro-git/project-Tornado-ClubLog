# api/handlers/users_handler.py
import tornado.web
from backend.db.connection.connection import get_connection

class UsersHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")

    async def get(self):
        limit = int(self.get_argument("limit", 6))
        offset = int(self.get_argument("offset", 0))

        try:
            conn = get_connection()
            cursor = conn.cursor()

            # ★ 総件数取得
            cursor.execute("""
                SELECT COUNT(*)
                FROM users u
                JOIN participants p ON u.id = p.user_id
                JOIN events e ON p.event_id = e.id
                JOIN clubs c ON e.club_id = c.id
                WHERE p.approved_status = 'approved'
            """)
            total_count = cursor.fetchone()[0] or 0

            # ★ ページングしてデータ取得
            cursor.execute("""
                SELECT
                    u.id,
                    u.username,
                    c.name AS club_name,
                    p.joined_at
                FROM
                    users u
                JOIN participants p ON u.id = p.user_id
                JOIN events e ON p.event_id = e.id
                JOIN clubs c ON e.club_id = c.id
                WHERE
                    p.approved_status = 'approved'
                ORDER BY u.id, p.joined_at
                LIMIT %s OFFSET %s;
            """, (limit, offset))

            rows = cursor.fetchall()
            result = [
                {
                    "user_id": row[0],
                    "username": row[1],
                    "club_name": row[2],
                    "joined_at": row[3].isoformat()
                }
                for row in rows
            ]

            # ★ total_countを追加して返す
            self.write({
                "user_participation": result,
                "total_count": total_count
            })

        except Exception as e:
            self.set_status(500)
            self.write({"error": str(e)})
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
