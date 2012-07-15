from sqlalchemy import Column, Integer, String
from database import Base


class Action(Base):
    __tablename__ = 'Action'

    id    = Column(Integer, primary_key=True)
    code  = Column(String(32))
    description = Column(String(256))

    def __init__(self, code=None, description=None):
        self.code = code
        self.description = description 

    def __repr__(self):
        return '<Action %r>' % (self.code)
