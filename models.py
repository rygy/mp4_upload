from sqlalchemy import Column, Integer, String, Sequence, Text, DateTime, ForeignKey
from database import Base, engine

import datetime


class Mp4Info(Base):
    __tablename__ = 'mp4_info'

    id = Column(Integer, primary_key=True)
    name = Column(String(2048))
    width = Column(String(2048))
    height = Column(String(2048))
    upload_date = Column(DateTime, default=datetime.datetime.today())
    last_modification = Column(DateTime, default=datetime.datetime.today())
    mime_type = Column(String(2048))
    duration = Column(String(2048))
    owner = Column(String(2048))
    location = Column(String(2048))


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(2048))
    password = Column(String(2048))
    email = Column(String(2048))
    api_key = Column(String(2048))

    def __repr__(self):
        return '<User(username={}, ' \
               'email={}, ' \
               'api_key={})>'.format(self.username,
                                     self.email,
                                     self.api_key)

Base.metadata.create_all(engine)

