from flask import Flask, render_template, request, session, redirect
from flask_sqlalchemy import SQLAlchemy
import os
current_dir = os.path.abspath(os.path.dirname(__file__))
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_required, current_user, login_user, logout_user, UserMixin


app = Flask(__name__)
app.secret_key = 'xyz'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///"+os.path.join(current_dir, "testdb.sqlite3")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy()
db.init_app(app)
app.app_context().push()
login = LoginManager()
login.init_app(app)
login.login_view = 'userLogin'
#above all is just initialising stuff

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
    
    
@login.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.before_first_request
def create_table():
    db.create_all()



@app.route("/userCreation", methods=['GET','POST'])
def userCreation():
    if request.method=="GET":
        ALLCOMPANYS = Company.query.all()
        return render_template("userCreation.html", companys = ALLCOMPANYS)
    if request.method=="POST": #once the form is filled 
        clientUsername = request.form.get("clientUsername")
        clientEmail = request.form.get("clientEmail")
        companyName = request.form.get("companyName")
        clientPassword = request.form.get("clientPassword")
        companyOfUser = Company.query.filter_by(companyName=companyName).first()
        newUser = User(clientUsername, clientEmail, companyOfUser.id, clientPassword)
        db.session.add(newUser)
        db.session.commit()
        return render_template('home.html')

@app.route("/companyCreation", methods=['GET','POST'])
def companyCreation():
    if request.method=="GET":
        return render_template("companyCreation.html")
    if request.method=="POST":
        companyName = request.form.get("companyName")
        pocName = request.form.get("pocName")
        phone = request.form.get("phone")
        newCompany = Company(companyName, pocName, phone)
        db.session.add(newCompany)
        db.session.commit()
        ALLCOMPANYS = Company.query.all()
        return render_template('userCreationAfterCompanyCreation.html', companys = ALLCOMPANYS)

@app.route('/addReport', methods=['GET','POST'])
def addReport():
    if request.method=="GET":
        ALLCOMPANYS = Company.query.all()
        return render_template("addReport.html", companys = ALLCOMPANYS)
    if request.method=="POST":
        companyName = request.form.get("companyName")
        feedbackRating = request.form.get("feedbackRating")
        feedbackText = request.form.get("feedbackText")
        if feedbackRating!="" and feedbackText!="":
            reportReady = True
        companyOfFeedback = Company.query.filter_by(companyName=companyName).first()
        companyOfFeedback.feedbackRating = feedbackRating
        companyOfFeedback.feedbackText = feedbackText
        companyOfFeedback.reportReady = reportReady
        db.session.commit()
        return render_template('home.html')

@app.route('/viewReport', methods=['GET','POST'])
@login_required
def viewReport():
    return render_template('viewReport.html', user = current_user)

@app.route('/userLogin', methods = ['POST','GET'])
def userLogin():
    if current_user.is_authenticated:
        return render_template('viewReport.html', user = current_user)
    if request.method == 'POST':
        email = request.form['email']
        user = User.query.filter_by(email = email).first()
        if user is not None and user.checkPassword(request.form['password']):
            login_user(user)
            return render_template('/viewReport.html', user = user)
    return render_template('userLogin.html')

@app.route('/userLogout')
def userLogout():
    logout_user()
    return redirect('/')
    
@app.route('/userChangePassword', methods=['POST', 'GET'])
def userChangePassword():
    if request.method=='GET':
        return render_template('userChangePassword.html')
    if request.method=='POST':
        clientEmail = request.form.get("clientEmail")
        oldPassword = request.form.get("oldPassword")
        newPassword = request.form.get("newPassword")
        user = User.query.filter_by(email=clientEmail).first()
        if oldPassword==newPassword:
            pass
        if user is not None and user.checkPassword(oldPassword) and oldPassword!=newPassword:
            user.setPassword(newPassword)
            return render_template('userChangePasswordSuccess.html')
            
@app.route('/')
def home():
    return render_template('home.html')

if __name__=="__main__": #driver function
    app.debug=True
    app.run()