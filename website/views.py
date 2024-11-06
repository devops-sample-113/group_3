from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user, login_required
from .models import Student, Classes,Enrollment
from . import db
from datetime import datetime
import os, sys

views = Blueprint("views", __name__)

@views.route("/")
@views.route("/home")
def home():
    return render_template("home.html", user=current_user)

@views.route("/search", methods=["GET", "POST"])
@login_required
def search():
    account = ""
    student = None
    if request.method == "POST":
        account = request.form.get("search_query")
        student = Student.query.filter_by(account=account).first()

    return render_template("search.html", student=student, account=account,user=current_user)

@views.route('/timetable', methods=["GET", "POST"])
@login_required
def timetable():
    student_id = current_user.student_id
    
    enrollments = Enrollment.query.filter_by(student_id=student_id).all()

    classes = [Classes.query.get(enrollment.class_id) for enrollment in enrollments]
    
    return render_template('timetable.html', classes=classes, user = current_user)
