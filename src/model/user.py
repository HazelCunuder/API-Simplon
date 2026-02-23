from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):

    __tablename__ = "user_table"

    id = Column(Integer, primary_key=True)
    last_name = Column(String(50), nullable=False)
    first_name = Column(String(50), nullable=False, )
    email = Column(String, unique=True, nullable=False)
    role = Column(String, nullable=False, default="User")
    register_date = Column(Date, nullable=False)