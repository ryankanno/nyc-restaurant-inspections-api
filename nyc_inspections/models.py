from sqlalchemy import Column
from sqlalchemy import Integer, Unicode, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict
import itertools
from utilities import empty_dict


BOROUGHS = {
    1: 'Manhattan',
    2: 'The Brox',
    3: 'Brooklyn',
    4: 'Queens',
    5: 'Staten Island',
}


class Action(Base):
    __tablename__ = 'Action'

    id = Column(Integer, primary_key=True)
    code = Column(String(10))
    description = Column(String(150))
    start_at = Column(DateTime)
    end_at = Column(DateTime)

    def __init__(self, code=None, description=None,
                 start_at=None, end_at=None):
        self.code = code
        self.description = description
        self.start_at = start_at
        self.end_at = end_at

    def __repr__(self):
        return u"<Action %r>".format(self.code)


class Violation(Base):
    __tablename__ = 'Violation'

    id = Column(Integer, primary_key=True)
    code = Column(String(3))
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

    id = Column(Integer, primary_key=True)
    code = Column(String(3), unique=True)
    description = Column(Unicode(600))

    def __init__(self, code=None, description=None):
        self.code = code
        self.description = description

    def __repr__(self):
        return u"<Cuisine %r>".format(self.description)


class Restaurant(Base):
    __tablename__ = 'Restaurant'

    id = Column(Integer, primary_key=True)
    unique_id = Column(String(10), unique=True)
    name = Column(String(256))
    building = Column(String(10))
    street = Column(String(100))
    zip = Column(String(5))
    borough = Integer()
    phone = Column(String(20))
    inspections = relationship(
        'Inspection', backref='restaurant',
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

    def _serialized_inspections(self):
        serialized_inspections = []
        if self.inspections:
            groups = []
            sorted_inspections = sorted(
                self.inspections, key=lambda x: x.graded_at,
                reverse=True)

            for k, g in itertools.groupby(sorted_inspections,
                                          key=lambda x: x.graded_at):
                groups.append(list(g))

            for group in groups:
                if len(group) > 0:
                    serialized_inspection = self._init_inspection(group[0])
                    violations = []
                    for inspection in group:
                        violations.append(self._parse_violation(inspection))
                    serialized_inspection['violations'] = violations
                    serialized_inspections.append(serialized_inspection)

        return serialized_inspections

    def _init_inspection(self, inspection_obj):
        inspection = {}
        if inspection_obj:
            inspection = inspection_obj.serialize
            empty_dict(inspection,
                       ['action_code', 'action_desc',
                        'violation_code', 'violation_desc',
                        'violation_is_critical'])
        return inspection

    def _parse_violation(self, inspection_obj):
        violation = {}
        if inspection_obj:
            inspection = inspection_obj.serialize
            violation['violation_code'] = inspection['violation_code']
            violation['violation_desc'] = inspection['violation_desc']
            violation['violation_is_critical'] = \
                inspection['violation_is_critical']
        return violation

    @property
    def address(self):
        bldg = self.building.strip()
        bldg = "{0} ".format(bldg) if len(bldg) > 0 else ""
        if self.street and self.zip:
            return u"{building}{street}".format(
                building=bldg, street=self.street)
        else:
            return ""

    @property
    def serialize(self):
        restaurant = OrderedDict()
        restaurant['name'] = self.name
        restaurant['phone'] = self.phone
        restaurant['street_address'] = self.address
        restaurant['zip_code'] = self.zip
        restaurant['city'] = 'New York'
        restaurant['state'] = 'NY'
        restaurant['inspections'] = self._serialized_inspections()
        return restaurant


class Inspection(Base):
    __tablename__ = 'Inspection'

    id = Column(Integer, primary_key=True)
    restaurant_id = Column(Integer, ForeignKey('Restaurant.id'))
    cuisine_id = Column(Integer, ForeignKey('Cuisine.id'))
    inspected_at = Column(DateTime)
    action_id = Column(Integer, ForeignKey('Action.id'))
    violation_id = Column(Integer, ForeignKey('Violation.id'))
    score = Column(Integer)
    current_grade = Column(String)
    graded_at = Column(DateTime)
    generated_at = Column(DateTime)

    cuisine = relationship(
        'Cuisine', uselist=False,
        primaryjoin="Inspection.cuisine_id==Cuisine.id")

    action = relationship(
        'Action', uselist=False,
        primaryjoin="Inspection.action_id==Action.id")

    violation = relationship(
        'Violation', uselist=False,
        primaryjoin="Inspection.violation_id==Violation.id")

    def __init__(self, restaurant_id=None, cuisine_id=None,
                 inspected_at=None, action_id=None, violation_id=None,
                 score=None, current_grade=None, graded_at=None,
                 generated_at=None):
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
    def serialize(self):
        inspection = {
            'score': self.score,
            'current_grade': self.current_grade,
            'inspection_date': self.graded_at.strftime('%Y-%m-%dT%H:%M:%S'),
            'action_code': '',
            'action_desc': '',
            'violation_code': '',
            'violation_desc': '',
            'violation_is_critical': ''
        }

        if self.action:
            inspection['action_code'] = self.action.code
            inspection['action_desc'] = self.action.description

        if self.violation:
            inspection['violation_code'] = self.violation.code
            inspection['violation_desc'] = self.violation.description
            inspection['violation_is_critical'] = self.violation.is_critical

        return inspection
