import datetime

from applications.extensions import db


class Photo(db.Model):
    __tablename__ = 'photo'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Integer)
    name = db.Column(db.String(255), nullable=False)
    href = db.Column(db.String(255))
    mime = db.Column(db.CHAR(50), nullable=False)
    size = db.Column(db.CHAR(30), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.datetime.now)
