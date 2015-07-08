from sqlalchemy import create_engine as c_e
from sqlalchemy.orm import create_session
from sqlalchemy.orm import scoped_session
from sqlalchemy.ext.declarative import declarative_base


engine = None
db_session = scoped_session(
    lambda: create_session(bind=engine, autocommit=False, autoflush=False)
)
Base = declarative_base()
Base.query = db_session.query_property()


def init_engine(database_uri):
    global engine
    engine = c_e(database_uri, convert_unicode=True)


def create_db(database_uri):
    init_engine(database_uri)
    Base.metadata.create_all(bind=engine)


def drop_db(database_uri):
    init_engine(database_uri)
    Base.metadata.drop_all(bind=engine)
