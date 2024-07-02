from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Pokemon(Base):
    __tablename__ = 'pokemon'

    pokedex = Column(Integer, primary_key=True)
    name = Column(String)
    image = Column(String)
    types = Column(String)

