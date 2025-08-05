# api/handlers/users_handler.py
import tornado.web
from backend.db.connection.connection import get_connection

class UsersHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")

    async def get(self):
        try:
            conn = get_connection()
            cursor = conn.cursor()

            # ★ 全件取得
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
            """)
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

            self.write({
                "user_participation": result,
                "total_count": len(result)
            })

        except Exception as e:
            self.set_status(500)
            self.write({"error": str(e)})
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
