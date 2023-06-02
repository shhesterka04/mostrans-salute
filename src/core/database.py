from sqlalchemy import create_engine, Column, String, Integer, exists
from sqlalchemy.orm import sessionmaker, declarative_base
import json

Base = declarative_base()


class Route(Base):
    __tablename__ = 'routes'

    id = Column(Integer, primary_key=True)
    short_route_name = Column(String)
    long_route_name = Column(String)
    link = Column(String)

    def __init__(self, short_route_name, long_route_name, link):
        self.short_route_name = short_route_name
        self.long_route_name = long_route_name
        self.link = link


engine = create_engine('sqlite:///routes.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


