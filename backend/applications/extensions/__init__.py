from flask import Flask

from .init_dotenv import init_dotenv
from .init_sqlalchemy import db, ma, init_databases
from .init_upload import init_upload


def init_plugs(app: Flask) -> None:
    init_databases(app)
    init_upload(app)
    init_dotenv()
