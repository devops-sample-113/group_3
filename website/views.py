from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user, login_required
from .models import Student, Classes,Enrollment,Follow
from . import db
from datetime import datetime
import os, sys, re

views = Blueprint("views", __name__)

def get_total_credits(student_id):
    total_credits = db.session.query(
        db.func.sum(Classes.credit)
    ).join(Enrollment, Classes.id == Enrollment.class_id).filter(
        Enrollment.student_id == student_id
    ).scalar() or 0

    return total_credits

def can_add_course(student_id, new_class_id):
    current_credits = get_total_credits(student_id)
    new_class = Classes.query.filter_by(number=new_class_id).first()

    new_class_credits = new_class.credit
    if current_credits + new_class_credits > 25:
        return False, "選課失敗：學分數超過25"

    return True, None

def check_time_conflict(student_id, new_class):
    enrolled_classes = db.session.query(Classes).join(
        Enrollment, Classes.id == Enrollment.class_id
    ).filter(Enrollment.student_id == student_id).all()

    new_class_date = new_class.date
    new_class_time = new_class.time.split(',')

    for enrolled_class in enrolled_classes:
        if enrolled_class.date != new_class_date:
            continue

        enrolled_class_time = enrolled_class.time.split(',')

        for time in new_class_time:
            if time in enrolled_class_time:
                return False, f"選課失敗：欲加選課程與 {enrolled_class.name} 課程在星期 {new_class_date} 節次 {time} 衝堂"
    
    return True, None

@views.route("/")
@views.route("/home")
def home():
    return render_template("home.html", user=current_user)

@views.route("/search", methods=["GET"])
def search():
    numberOrName = ""
    theClass = []
    if request.method == "GET":
        numberOrName = request.args.get("search_query", "")
        if(numberOrName):
            if numberOrName.isdigit():
                theClass = Classes.query.filter_by(number=numberOrName).all()
            else:
                theClass = Classes.query.filter(Classes.name.like(f"%{numberOrName}%")).all()

    return render_template("search.html", theClass=theClass, numberOrName=numberOrName,user=current_user)

@views.route('/timetable')
@login_required
def timetable():
    student_id = current_user.student_id
    enrollments = Enrollment.query.filter_by(student_id=student_id).all()
    follows = Follow.query.filter_by(student_id=student_id).all()
    classes = [Classes.query.get(enrollment.class_id) for enrollment in enrollments]
    classes2 = [Follow.query.get(follow.class_id) for follow in follows]
    
    
    return render_template('timetable.html', classes=classes, user = current_user,classes2 = classes2)

@views.route('/add_class/<number>', methods=["GET", "POST"])
@login_required
def add_class(number):
    student_id = current_user.get_id()
    # class_number = request.form.get('class_number')
    class_number = number

    can_add, message = can_add_course(student_id, class_number)
    if not can_add:
        flash(message, "danger")

        return redirect(url_for('views.search', search_query=request.form.get('search_query', '')))

    new_class = Classes.query.filter_by(number=class_number).first()

    no_conflict, message = check_time_conflict(student_id, new_class)
    if not no_conflict:
        flash(message, "danger")

        return redirect(url_for('views.search', search_query=request.form.get('search_query', '')))

    new_enrollment = Enrollment(student_id=student_id, class_id=new_class.id)
    current_user.enrollments.append(new_enrollment)
    db.session.add(new_enrollment)
    db.session.commit()

    flash(f"課程 {new_class.name} 已成功加入", "success")


    return redirect(url_for('views.search', search_query=request.form.get('search_query', '')))


@views.route('/drop_class/<class_id>', methods=["GET", "POST"])
@login_required
def drop_class(class_id):
    student_id = current_user.get_id()
    current_credits = get_total_credits(student_id)
    course = Classes.query.filter_by(id=class_id).first()


    if 12 <= current_credits - course.credit:
        course = Enrollment.query.filter_by(class_id=class_id, student_id=student_id).first()
        
        db.session.delete(course)
        db.session.commit()




    return redirect(url_for('views.search', search_query=request.form.get('search_query', '')))
@views.route('/follow', methods=["GET", "POST"])
@login_required
def follow():
    student_id = current_user.get_id()
    class_number = request.form.get('class_number')

    can_add, message = can_add_course(student_id, class_number)
    if not can_add:
        flash(message, "danger")

        return redirect(url_for('views.search', search_query=request.form.get('search_query', '')))

    new_class = Classes.query.filter_by(number=class_number).first()

    no_conflict, message = check_time_conflict(student_id, new_class)
    if not no_conflict:
        flash(message, "danger")

        return redirect(url_for('views.search', search_query=request.form.get('search_query', '')))

    follow = Follow(student_id=student_id, class_id=new_class.id)
    db.session.add(follow)
    db.session.commit()

    flash(f"課程 {new_class.name} 已成功加入", "success")


    return redirect(url_for('views.search', search_query=request.form.get('search_query', '')))
