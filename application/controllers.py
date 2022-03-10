from flask import Flask, request, session, redirect
from flask import render_template
from flask import current_app as app
from flask_security import auth_required, roles_required
from application.models import *


@app.before_first_request
def create_user():
    db.create_all()
    if not user_datastore.find_user(email="test@me.com"):
        user_datastore.create_user(email="test@me.com", password=hash_password("password"), roles=['viewer', 'manager'])
    db.session.commit()

@app.route('/addReport', methods=['GET','POST'])
@roles_required('manager')
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
@roles_required('viewer')
def viewReport():
    return render_template('viewReport.html', user = current_user)


'''
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
'''            
@app.route('/')
@auth_required()
def home():
    return render_template('home.html')
