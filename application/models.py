from .database import *
from flask_security import UserMixin, RoleMixin
from flask_security.models import fsqla_v2 as fsqla
from flask_security import SQLAlchemySessionUserDatastore, SQLAlchemyUserDatastore, hash_password

roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('users.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('roles.id')))

companys_users = db.Table('companys_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('users.id')),
        db.Column('company_id', db.Integer(), db.ForeignKey('companys.id')))

class User(db.Model, fsqla.FsUserMixin):
    __tablename__='users' 
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, unique=True)
    email = db.Column(db.String, unique=True)
    #companyId = db.Column(db.String, db.ForeignKey('companys.id'))
    #company = db.relationship("Company", back_populates = "users")
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    roles = db.relationship('Role', secondary=roles_users,
                           backref=db.backref('users', lazy='dynamic'))
    companys = db.relationship('Company', secondary=companys_users,
                           backref=db.backref('users', lazy='dynamic'))
        
class Role(db.Model, fsqla.FsRoleMixin):
    __tablename__='roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    description = db.Column(db.String(255))

class Company(db.Model):
    __tablename__='companys'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, unique=True, index=True)
    #pocName = db.Column(db.String)
    email = db.Column(db.String)
    #phone = db.Column(db.String(10))  
    reportReady = db.Column(db.Boolean)
    feedbackText =  db.Column(db.Integer, nullable=True)
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.reportReady = False
    #users = db.relationship("User", back_populates="company")

    
user_datastore = SQLAlchemySessionUserDatastore(db.session, User, Role)
