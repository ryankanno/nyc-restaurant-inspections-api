from sqlalchemy import Column, Integer, Unicode, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship 
from database import Base


BOROUGHS = {
    1:'Manhattan',
    2:'The Brox',
    3:'Brooklyn',
    4:'Queens',
    5:'Staten Island',
} 


class Action(Base):
    __tablename__ = 'Action'

    id    = Column(Integer, primary_key=True)
    code  = Column(String(10))
    description = Column(String(150))
    start_at = Column(DateTime)
    end_at = Column(DateTime)

    def __init__(self, code=None, description=None, start_at=None, end_at=None):
        self.code = code
        self.description = description 
        self.start_at = start_at
        self.end_at = end_at

    def __repr__(self):
        return u"<Action %r>".format(self.code)


class Violation(Base):
    __tablename__ = 'Violation'

    id    = Column(Integer, primary_key=True)
    code  = Column(String(3))
    description = Column(Unicode(600))
    is_critical = Column(Boolean())
    start_at = Column(DateTime)
    end_at = Column(DateTime)

    def __init__(self, code=None, description=None, is_critical=False,
            start_at=None, end_at=None):
        self.code = code
        self.description = description 
        self.is_critical = is_critical
        self.start_at = start_at
        self.end_at = end_at

    def __repr__(self):
        return u"<Violation %r>".format(self.code)


class Cuisine(Base):
    __tablename__ = 'Cuisine'

    id    = Column(Integer, primary_key=True)
    code  = Column(String(3), unique=True)
    description = Column(Unicode(600))

    def __init__(self, code=None, description=None):
        self.code = code
        self.description = description 

    def __repr__(self):
        return u"<Cuisine %r>".format(self.description)


class Restaurant(Base):
    __tablename__ = 'Restaurant'

    id    = Column(Integer, primary_key=True)
    unique_id = Column(String(10), unique=True)
    name = Column(String(256))
    building = Column(String(10))
    street = Column(String(100))
    zip = Column(String(5))
    borough = Integer()
    phone = Column(String(20))
    
    inspections = relationship('Inspection', backref='restaurant',
        primaryjoin="Restaurant.id==Inspection.restaurant_id")

    def __init__(self, unique_id=None, name=None, building=None, street=None,
            zip=None, borough=None, phone=None):
        self.unique_id = unique_id
        self.name = name
        self.building = building
        self.street = street
        self.zip = zip
        self.borough = borough
        self.phone = phone

    def __repr__(self):
        return u"<Restaurant %r>".format(self.name)

    @property
    def to_json(self):
        return to_json(self, self.__class__)


class Inspection(Base):
    __tablename__ = 'Inspection'

    id    = Column(Integer, primary_key=True)
    restaurant_id = Column(Integer, ForeignKey('Restaurant.id'))
    cuisine_id = Column(Integer, ForeignKey('Cuisine.id'))
    inspected_at = Column(DateTime)
    action_id = Column(Integer, ForeignKey('Action.id'))
    violation_id = Column(Integer, ForeignKey('Violation.id'))
    score = Column(Integer)
    current_grade = Column(String)
    graded_at = Column(DateTime)
    generated_at = Column(DateTime)

    cuisine = relationship('Cuisine', uselist=False,
        primaryjoin="Inspection.cuisine_id==Cuisine.id")

    action = relationship('Action', uselist=False,
        primaryjoin="Inspection.action_id==Action.id")

    violation = relationship('Violation', uselist=False,
        primaryjoin="Inspection.violation_id==Violation.id")

    def __init__(self, restaurant_id=None, cuisine_id = None, 
        inspected_at = None, action_id = None, violation_id = None,
        score = None, current_grade = None, graded_at = None, 
        generated_at = None):
        self.restaurant_id = restaurant_id 
        self.cuisine_id = cuisine_id 
        self.inspected_at = inspected_at 
        self.action_id = action_id
        self.violation_id = violation_id
        self.score = score
        self.current_grade = current_grade
        self.graded_at = graded_at
        self.generated_at = generated_at

    def __repr__(self):
        return u"<Inspection {0}>".format(self.id)

    @property
    def to_json(self):
        return to_json(self, self.__class__)


CONVERTERS = {}

def to_json(inst, cls):
    converters = {}
    data = {}

    for col in cls.__table__.columns:
        val = getattr(inst, col.name)
        print col.type
        if col.type in converters.keys() and val is not None:
            try:
                data[col.name] = converters[col.type](v)
            except:
                data[c.name] = "Error:  Failed to covert using ", str(converters[c.type])
        else:
            data[col.name] = val if val else ""

    return data
