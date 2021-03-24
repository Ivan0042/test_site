import datetime
import sqlalchemy
from sqlalchemy import orm
from flask_login import UserMixin
#from .db_session import SqlAlchemyBase
from Class.Application import Application
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, 
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    about = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String, 
                              index=True, unique=True, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, 
                                     default=datetime.datetime.now)
    like = sqlalchemy.Column(sqlalchemy.String, default='')
    dislike = sqlalchemy.Column(sqlalchemy.String, default='')
    moderation = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    quests = orm.relation("Quest", back_populates='user')
    commentary = orm.relation('Commentary')
    
    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)