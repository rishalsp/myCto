from flask import Flask, request, session, redirect
from flask import render_template
from flask import current_app as app
from flask_security import auth_required, roles_required
from application.models import *


@app.before_first_request
def create_user():
    db.create_all()
    if not user_datastore.find_user(email="testadmin@admin.com"):
        user_datastore.create_user(username='testadmin', email="testadmin@admin.com", password=hash_password("password"), roles=['admin'])
    db.session.commit()

@app.route('/userManagerCreation', methods=['GET', 'POST'])
@roles_required('admin')
def userManagerCreation():
    if request.method=="GET":
        allCompanys = Company.query.all()
        return render_template("userManagerCreation.html", companys=allCompanys)
    if request.method=="POST": 
        username = request.form.get("username")
        password = request.form.get("password")
        email = request.form.get("email")
        companys = request.form.getlist('companyList')
        user_datastore.create_user(username=username, email=email, password=password, roles=['manager'], companys=[str(company) for company in companys])
        db.session.commit()
        return render_template('home.html')
        
@app.route('/userViewerCreation', methods=['GET', 'POST'])
@roles_required('admin')
def userViewerCreation():
    if request.method=="GET":
        allCompanys = Company.query.all()
        return render_template("userViewerCreation.html", companys=allCompanys)
    if request.method=="POST": 
        username = request.form.get("username")
        password = request.form.get("password")
        email = request.form.get("email")
        companys = request.form.getlist('companyList')
        user_datastore.create_user(username=username, email=email, password=password, roles=['viewer'], companys=[str(company) for company in companys])
        db.session.commit()
        return render_template('home.html')
        
@app.route('/companyCreation', methods=['GET', 'POST'])
@roles_required('admin')
def companyCreation():
    if request.method=="GET":
        return render_template("companyCreation.html")
    if request.method=="POST": 
        name = request.form.get("name")
        email = request.form.get("email")
        newCompany = Company(name, email)
        db.session.add(newCompany)
        db.session.commit()
        return render_template('home.html')
        
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

@app.route('/')
@auth_required()
def home():
    return render_template('home.html')
