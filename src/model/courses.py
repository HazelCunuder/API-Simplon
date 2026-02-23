from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Courses(Base):

    __tablename__ = "courses_table"

    id = Column(Integer, primary_key=True)
    title = Column(String(50), nullable=False)
    description = Column(Text, nullable=True)
    duration = Column(Integer, nullable=False)
    level = Column(Integer, nullable=False)
    status = Column(Integer, nullable=False, default=0)