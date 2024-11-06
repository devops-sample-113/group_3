from flask_login import UserMixin
from . import db
from sqlalchemy.sql import func
from flask_sqlalchemy import SQLAlchemy

class Student(db.Model, UserMixin):
    __tablename__ = "students"

    def __init__(self, account, name, password):
        self.account = account
        self.name = name
        self.password = password
    
    def get_id(self):
        return (self.student_id)

    student_id = db.Column(db.Integer, primary_key=True)
    account = db.Column(db.String(50))
    name = db.Column(db.String(50))
    password = db.Column(db.String(150))

    def __repr__(self):
        return f"id: {self.student_id}, email: {self.account}, name: {self.name}"

class Classes(db.Model, UserMixin):
    __tablename__ = "classes"


    def __init__(self, id, number, name, teacher, classroom, date, time, credit):

        self.id = id
        self.number = number
        self.name = name
        self.teacher = teacher
        self.classroom = classroom
        self.date = date
        self.time = time
        self.credit = credit

    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    teacher = db.Column(db.String(50), nullable=False)
    classroom = db.Column(db.String(50), nullable=False)
    date = db.Column(db.String(50), nullable=False)
    time = db.Column(db.String(50), nullable=False)
    credit = db.Column(db.Integer, nullable=False)

class Enrollment(db.Model, UserMixin):
    __tablename__ = "enrollments"

    def __init__(self, student_id, class_id):
        self.student_id = student_id
        self.class_id = class_id

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.student_id'), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'), nullable=False)

    student = db.relationship('Student', backref='enrollments', lazy=True)
    classes = db.relationship('Classes', backref='enrollments', lazy=True)
