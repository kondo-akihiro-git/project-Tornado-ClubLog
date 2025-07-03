# backend/test/test_connection.py
import tornado.testing
from tornado.testing import gen_test
from backend.db.connection.connection import get_connection


class TestDBConnection(tornado.testing.AsyncTestCase):

    @gen_test
    async def test_DBに接続できる(self):
        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT 1;")
            result = cursor.fetchone()
            assert result[0] == 1
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
