from .database import *
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_required, current_user, login_user, logout_user, UserMixin

class Admin(db.Model):
    __tablename__='admins' 
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String)
    email = db.Column(db.String)
    passwordHash = db.Column(db.String(128))
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)    
        
class Company(db.Model):
    __tablename__='companys'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    companyName = db.Column(db.String, unique=True, index=True)
    pocName = db.Column(db.String)
    phone = db.Column(db.String(10))  
    reportReady = db.Column(db.Boolean)
    def __init__(self, companyName, pocName, phone):
        self.companyName = companyName
        self.pocName = pocName
        self.phone = phone
        self.reportReady = False
    users = db.relationship("User", back_populates="company")
    feedbackRating = db.Column(db.Integer, nullable=True)
    feedbackText =  db.Column(db.Integer, nullable=True)

class User(db.Model, UserMixin):
    __tablename__='users' 
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    companyId = db.Column(db.String, db.ForeignKey('companys.id'))
    company = db.relationship("Company", back_populates = "users")
    passwordHash = db.Column(db.String)
    def __init__(self,username, email, companyId, password):
        self.username = username
        self.email = email
        self.companyId = companyId
        self.passwordHash = generate_password_hash(password)
    def setPassword(self, password):
        self.passwordHash = generate_password_hash(password)
    def checkPassword(self, password):
        return check_password_hash(self.passwordHash, password)
    