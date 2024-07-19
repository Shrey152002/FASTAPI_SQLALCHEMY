from sqlalchemy import Boolean, Column, String, Integer, Time,ForeignKey
from database import Base
from sqlalchemy.orm import relationship
class Movie(Base):
    __tablename__ = "movies"
    title = Column(String(255), primary_key=True, index=True)
    description = Column(String(255))
    rating =Column(Integer)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, index=True)
    email = Column(String(255), unique=True, index=True)

class Booking(Base):
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    movie_title = Column(String, ForeignKey('movies.title'))
    seats = Column(Integer)
    
    user = relationship("User")
    movie = relationship("Movie")