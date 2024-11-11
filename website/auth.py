from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import current_user, login_user, login_required, logout_user
from .models import Student
from werkzeug.security import generate_password_hash, check_password_hash
from . import db

auth = Blueprint("auth", __name__)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("views.home"))


@auth.route("/login", methods=["GET", "POST"])
def login():
    account = ""
    if request.method == "POST":
        account = request.form.get("account")
        password = request.form.get("password")

        student = Student.query.filter_by(account=account).first()

        if student:
            if check_password_hash(student.password, password):
                flash("Logged in.", category="success")
                login_user(student, remember=True)
                return redirect(url_for("views.home"))
            else:
                flash("Password incorrect.", category="error")

        else:
            flash("User does not exist.", category="error")

    return render_template("login.html", user=current_user, last_account=account)
