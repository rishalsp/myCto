from flask import Flask, render_template, request, session, redirect
from flask_sqlalchemy import SQLAlchemy
import os
current_dir = os.path.abspath(os.path.dirname(__file__))
from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, \
    RoleMixin, login_required

app = Flask(__name__)
app.secret_key = 'super-secret'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///"+os.path.join(current_dir, "testdb.sqlite3")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy()
db.init_app(app)
app.app_context().push()
#above all is just initialising stuff

roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('users.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('roles.id')))

class Role(db.Model, RoleMixin):
    __tablename__='roles'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))
    
class User(db.Model, UserMixin):
    __tablename__='users' 
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                           backref=db.backref('users', lazy='dynamic'))


# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

@app.before_first_request
def create_table():
    db.create_all()

# Views
@app.route('/')
@login_required
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.debug=True
    app.run()