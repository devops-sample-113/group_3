from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user, login_required
from .models import Student, Classes
from . import db
from datetime import datetime
import os, sys, re

views = Blueprint("views", __name__)

@views.route("/")
@views.route("/home")
def home():
    return render_template("home.html", user=current_user)

@views.route("/search", methods=["GET", "POST"])
def search():
    numberOrName = ""
    theClass = None
    if request.method == "POST":
        numberOrName = request.form.get("search_query")
        if re.match(r'^\d+$', numberOrName):
            theClass = Classes.query.filter_by(number=numberOrName).first()
        else:
            theClass = Classes.query.filter_by(name=numberOrName).first()   

    return render_template("search.html", theClass=theClass, user=current_user)
