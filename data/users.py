import sqlalchemy
from .db_session import SqlAlchemyBase
from flask_login import UserMixin


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'USERS'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    
    login = sqlalchemy.Column(sqlalchemy.String, nullable=True, unique=True, index=True)
    password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    cmd_name = sqlalchemy.Column(sqlalchemy.String, nullable=True, unique=True, index=True)
    cmd_info = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    cmd_staff = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    achievements = sqlalchemy.Column(sqlalchemy.BLOB, nullable=True)