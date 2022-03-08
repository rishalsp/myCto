from flask import Flask, request, session, redirect
from flask import render_template
from flask import current_app as app
from application.models import *


login = LoginManager()
login.init_app(app)
login.login_view = 'userLogin'

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
