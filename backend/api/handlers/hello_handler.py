# api/handlers/hello_handler.py
import tornado.web

class HelloHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")

    async def get(self):
        self.write("Hello, world!")
