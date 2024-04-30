import sqlalchemy
from .db_session import SqlAlchemyBase


class Admin(SqlAlchemyBase):
    __tablename__ = 'ADMINISTRATORS'

    id = sqlalchemy.Column(sqlalchemy.Integer,  primary_key=True, autoincrement=True)
    login = sqlalchemy.Column(sqlalchemy.String, nullable=True, unique=True, index=True)
    password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    adm_name = sqlalchemy.Column(sqlalchemy.String, nullable=True, unique=True, index=True)

    amd_info = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    amd_games = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    amd_games = sqlalchemy.Column(sqlalchemy.String, nullable=True)