import sqlalchemy
from .db_session import SqlAlchemyBase


class Game(SqlAlchemyBase):
    __tablename__ = 'GAMES'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    passcode = sqlalchemy.Column(sqlalchemy.String, nullable=False, index=True)
    gameinfo = sqlalchemy.Column(sqlalchemy.BLOB, nullable=True)
