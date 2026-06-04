import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Race(Base):
    __tablename__ = "races"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(Text)
    traits = Column(Text, default="[]")
    name_templates = Column(Text, default="[]")
    sample_names = Column(Text, default="[]")
    name_rules = Column(Text, default="{}")

class City(Base):
    __tablename__ = "cities"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    region = Column(String)
    atmosphere = Column(String)
    danger_level = Column(String)
    notes = Column(Text)
    demographics = Column(Text, default="[]")

class NPC(Base):
    __tablename__ = "npcs"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    race = Column(String)
    city = Column(String)
    age = Column(Integer)
    gender = Column(String)
    role = Column(String)
    profession = Column(String)
    social_class = Column(String)
    alignment = Column(String)
    personality = Column(Text)
    appearance = Column(Text)
    voice = Column(Text)
    motivation = Column(Text)
    secret = Column(Text)
    fear = Column(Text)
    flaw = Column(Text)
    rumor = Column(Text)
    quest_hook = Column(Text)
    useful_info = Column(Text)
    combat_role = Column(String)
    stat_hint = Column(String)
    inventory = Column(Text)
    relationships = Column(Text)
    tags = Column(Text)
    dm_notes = Column(Text)
    seed = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

class NPCHistory(Base):
    __tablename__ = "npc_history"
    id = Column(Integer, primary_key=True)
    npc_id = Column(Integer)
    snapshot = Column(Text)
    saved_at = Column(DateTime, default=datetime.datetime.utcnow)
