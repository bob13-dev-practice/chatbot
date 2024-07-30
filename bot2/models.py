from sqlalchemy import Column, BigInteger, String, DateTime
from database import Base

class Access_Table(Base):
    __tablename__ = 'access_table'

    id = Column(BigInteger, primary_key=True)
    user_id = Column(String)
    channel_id = Column(String)
    access_time = Column(DateTime)
    access_id = Column(String)

class User(Base):
    __tablename__ = 'user'

    id = Column(String, primary_key=True)