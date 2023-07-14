from sqlalchemy import create_engine, func
from sqlalchemy import ForeignKey, Table, Column, Integer, String, DateTime
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.associationproxy import association_proxy

engine = create_engine('sqlite:///many_to_many.db')

Base = declarative_base()

class Game(Base):
    __tablename__ = 'games'

    id = Column(Integer(), primary_key=True)
    title = Column(String())
    genre = Column(String())
    platform = Column(String())
    price = Column(Integer())
    created_at = Column(DateTime(), server_default=func.now())
    updated_at = Column(DateTime(), onupdate=func.now())

    reviews = relationship('Review', back_populates='game', cascade='all, delete-orphan')
    users = association_proxy('reviews', 'user',
        creator=lambda us: Review(user=us))

    def __repr__(self):

        return f'Game(id={self.id}, ' + \
            f'title={self.title}, ' + \
            f'platform={self.platform})'

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    created_at = Column(DateTime(), server_default=func.now())
    updated_at = Column(DateTime(), onupdate=func.now())

    reviews = relationship('Review', back_populates='user', cascade='all, delete-orphan')
    games = association_proxy('reviews', 'game',
        creator=lambda gm: Review(game=gm))

    def __repr__(self):

        return f'User(id={self.id}, ' + \
            f'name={self.name})'

class Review(Base):
    __tablename__ = 'reviews'

    id = Column(Integer(), primary_key=True)

    score = Column(Integer())
    comment = Column(String())
    created_at = Column(DateTime(), server_default=func.now())
    updated_at = Column(DateTime(), onupdate=func.now())

    game_id = Column(Integer(), ForeignKey('games.id'))
    user_id = Column(Integer(), ForeignKey('users.id'))

    game = relationship('Game', back_populates='reviews')
    user = relationship('User', back_populates='reviews')

    def __repr__(self):

        return f'Review(id={self.id}, ' + \
            f'score={self.score}, ' + \
            f'game_id={self.game_id})'