import datetime

from applications.extensions import db


class Analysis(db.Model):
    __tablename__ = 'analysis'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.Integer)
    before_img = db.Column(db.String(512))
    before_img1 = db.Column(db.String(512))
    after_img = db.Column(db.String(512))
    data = db.Column(db.String(2048))
    is_hole = db.Column(db.Boolean)
    checked = db.Column(db.String(32))
    create_time = db.Column(db.DateTime, default=datetime.datetime.now)
