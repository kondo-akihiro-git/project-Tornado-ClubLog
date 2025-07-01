# api/main.py
import tornado.ioloop
import tornado.web
from handlers.hello_handler import HelloHandler

def make_app():
    return tornado.web.Application([
        (r"/", HelloHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8000)
    print("Server is running")
    tornado.ioloop.IOLoop.current().start()
