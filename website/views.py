from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user, login_required
from .models import Student
from . import db
from datetime import datetime
import os, sys

views = Blueprint("views", __name__)

@views.route("/")
@views.route("/home")
def home():
    return render_template("home.html", user=current_user)
@views.route("/search")
def search():
    return render_template("search.html", user=current_user)