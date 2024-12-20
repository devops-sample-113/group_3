from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user, login_required
from .models import Student, Course,Enrollment
from . import db
from datetime import datetime
import os, sys, re

views = Blueprint("views", __name__)

def get_total_credits(student_id):
    # total_credits = db.session.query(
    #     db.func.sum(Classes.credit)
    # ).join(Enrollment, Classes.id == Enrollment.class_id).filter(
    #     Enrollment.student_id == student_id
    # ).scalar() or 0
    total_credits = 0
    for course in current_user.courses:
        total_credits += course.credit

    return total_credits

def can_add_course(student_id, new_class_id):
    current_credits = get_total_credits(student_id)
    new_class = Course.query.filter_by(number=new_class_id).first()

    new_class_credits = new_class.credit
    if current_credits + new_class_credits > 25:
        return False, "選課失敗：學分數超過25"

    return True, None


def check_time_conflict(student_id, new_class):
    # enrolled_classes = db.session.query(Classes).join(
    #     Enrollment, Classes.id == Enrollment.class_id
    # ).filter(Enrollment.student_id == student_id).all()

    enrolled_courses = current_user.courses

    new_class_date = new_class.date
    new_class_time = new_class.time.split(',')

    for enrolled_class in enrolled_courses:
        if enrolled_class.date != new_class_date:
            continue

        enrolled_class_time = enrolled_class.time.split(',')

        for time in new_class_time:
            if time in enrolled_class_time:
                return False, f"選課失敗：欲加選課程與 {enrolled_class.name} 課程在星期 {new_class_date} 節次 {time} 衝堂"

    return True, None

def check_remaining(student_id, new_class_id):
    new_class = Course.query.filter_by(number=new_class_id).first()

    if new_class.remaining<=0:
        return False, "選課失敗，餘額不足"

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
                theClass = Course.query.filter_by(number=numberOrName).all()
            else:
                theClass = Course.query.filter(Course.name.like(f"%{numberOrName}%")).all()

    return render_template("search.html", theClass=theClass, numberOrName=numberOrName,user=current_user)

@views.route('/timetable')
@login_required
def timetable():
    student_id = current_user.student_id
    # enrollments = Enrollment.query.filter_by(student_id=student_id).all()
    # classes = [Classes.query.get(enrollment.class_id) for enrollment in enrollments]
    # return render_template('timetable.html', classes=classes, user = current_user,classes2 = classes2)
    total_credits = sum(course.credit for course in current_user.courses)
    return render_template('timetable.html', user = current_user,total_credit = total_credits)

@views.route('/add_class', methods=["POST"])
@login_required
def add_class():
    student_id = current_user.get_id()
    class_number = request.form.get('class_number')
    # class_number = number

    new_class = Course.query.filter_by(number=class_number).first()

    can_add, message = can_add_course(student_id, class_number)
    if not can_add:
        flash(message, "error")

        return render_template("search.html", theClass=[new_class], numberOrName="",user=current_user)

    no_conflict, message = check_time_conflict(student_id, new_class)
    if not no_conflict:
        flash(message, "error")

        return render_template("search.html", theClass=[new_class], numberOrName="",user=current_user)

    has_remaining, message = check_remaining(student_id, class_number)
    if not has_remaining:
        flash(message, "error")

        return render_template("search.html", theClass=[new_class], numberOrName="",user=current_user)

    # new_enrollment = Enrollment(student_id=student_id, class_id=new_class.id)
    new_enrollment = Course.query.filter_by(number=class_number).first()
    current_user.courses.append(new_enrollment)
    # db.session.add(new_enrollment)
    db.session.commit()

    flash(f"課程 {new_class.name} 已成功加入", "success")
    theClass = [new_enrollment]
    new_class.remaining -= 1
    db.session.commit()


    # return redirect(url_for('views.search', search_query=request.form.get('search_query', '')))
    return render_template("search.html", theClass=theClass, numberOrName="",user=current_user)


@views.route('/drop_class', methods=[ "POST"])
@login_required
def drop_class():
    class_id = request.form.get('class_id')
    student_id = current_user.get_id()
    current_credits = get_total_credits(student_id)
    course = Course.query.filter_by(course_id=class_id).first()

    if 4 <= current_credits - course.credit:
        course = Course.query.filter_by(course_id=class_id).first()
        current_user.courses.remove(course)
        course.remaining +=1
        db.session.commit()
        flash("退選成功", "success")

    if current_credits - course.credit < 4:
        flash("退選失敗(學分不得低於4)", "error")
    theClass = [course]

    return render_template("search.html", theClass=theClass, numberOrName="",user=current_user)


@views.route('/follow', methods=[ "POST"])
@login_required
def follow():
    # class_number = number
    class_number = request.form.get('class_number')
    course = Course.query.filter_by(course_id=class_number).first()

    current_user.follows.append(course)
    db.session.commit()

    flash(f"課程 {course.name} 關注成功", "success")
    theClass = [course]

    return render_template("search.html", theClass=theClass, numberOrName="",user=current_user)


@views.route('/unfollow', methods=["POST"])
@login_required
def unfollow():
    # class_number = number
    class_number = request.form.get('class_number')
    course = Course.query.filter_by(course_id=class_number).first()

    current_user.follows.remove(course)
    db.session.commit()

    flash(f"課程 {course.name} 取消關注成功", "success")
    theClass = [course]

    return render_template("search.html", theClass=theClass, numberOrName="",user=current_user)