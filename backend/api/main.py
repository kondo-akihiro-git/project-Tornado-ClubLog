# api/main.py
import tornado.ioloop
import tornado.web
from backend.api.handlers.approval_handler import ApprovalHandler
from backend.api.handlers.events_handler import EventsHandler
from backend.api.handlers.link_handler import LinkHandler
from backend.api.handlers.participants_handler import ParticipantsHandler
from backend.api.handlers.records_handler import RecordsHandler
from backend.api.handlers.register_handler import RegisterHandler
from backend.api.handlers.user_handler import UserHandler
from backend.api.handlers.users_handler import UsersHandler
from backend.api.handlers.verify_handler import VerifyHandler


def make_app():
    return tornado.web.Application([
        (r"/participants", ParticipantsHandler), 
        (r"/users", UsersHandler),
        (r"/user/([0-9]+)/info", UserHandler),
        (r"/user/([0-9]+)", UserHandler),
        (r"/user/([0-9]+)/records", RecordsHandler),  
        (r"/link", LinkHandler),
        (r"/events", EventsHandler),
        (r"/register", RegisterHandler),
        (r"/verify", VerifyHandler),
        (r"/approval", ApprovalHandler),

    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8000)
    print("------------ Tornado Server Running ------------")
    tornado.ioloop.IOLoop.current().start()
