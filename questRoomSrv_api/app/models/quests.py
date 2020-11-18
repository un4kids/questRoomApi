from app import db
from flask_sqlalchemy import inspect
import datetime
from sqlalchemy.sql import func


class Quest(db.Model):
    __tablename__ = "quests"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    mac_addr = db.Column(db.Text(), unique=True)
    index = db.Column(db.Integer, unique=True)
    config = db.Column(db.JSON)

    created_on = db.Column(db.DateTime, default=func.now())
    updated_on = db.Column(db.DateTime, onupdate=datetime.datetime.now)

    def toDict(self):
        data = {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}
        data["created_on"] = data["created_on"].strftime("%Y-%m-%d %H:%M")
        if data["updated_on"]:
            data["updated_on"] = data["updated_on"].strftime("%Y-%m-%d %H:%M")
        return data
