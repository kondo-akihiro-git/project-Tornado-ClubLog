# api/main.py
import tornado.ioloop
import tornado.web
from backend.api.handlers.link_handler import LinkHandler
from backend.api.handlers.participants_handler import ParticipantsHandler
from backend.api.handlers.records_handler import RecordsHandler
from backend.api.handlers.user_handler import UserHandler
from backend.api.handlers.users_handler import UsersHandler


def make_app():
    return tornado.web.Application([
        (r"/participants", ParticipantsHandler), 
        (r"/users", UsersHandler),
        (r"/user/([0-9]+)/info", UserHandler),
        (r"/user/([0-9]+)/records", RecordsHandler),  
        (r"/link", LinkHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8000)
    print("Server is running")
    tornado.ioloop.IOLoop.current().start()
