# api/main.py
import tornado.ioloop
import tornado.web
from backend.api.handlers.hello_handler import HelloHandler
from backend.api.handlers.participants_handler import ParticipantsHandler
from backend.api.handlers.users_handler import UsersHandler
# from handlers.hello_handler import HelloHandler
# from backend.handlers.participants_handler import ParticipantsHandler


def make_app():
    return tornado.web.Application([
        (r"/", HelloHandler),
        (r"/participants", ParticipantsHandler), 
        (r"/users", UsersHandler)
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8000)
    print("Server is running")
    tornado.ioloop.IOLoop.current().start()
