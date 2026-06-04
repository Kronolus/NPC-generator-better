from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base

DEFAULT_DB = "sqlite:///dnd_npc_city_generator.sqlite"

def get_engine(path=DEFAULT_DB):
    return create_engine(path, echo=False, future=True)

def init_db(engine):
    Base.metadata.create_all(engine)

def create_session(path=DEFAULT_DB):
    engine = get_engine(path)
    init_db(engine)
    Session = sessionmaker(bind=engine)
    return Session()
