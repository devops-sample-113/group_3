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

    def __init__(self, id, name, teacher, classroom, startTime, endTime):
        self.id = id
        self.name = name
        self.teacher = teacher
        self.classroom = classroom
        self.startTime = startTime
        self.endTime = endTime

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    teacher = db.Column(db.String(50), nullable=False)
    classroom = db.Column(db.String(50), nullable=False)
    startTime = db.Column(db.String(50), nullable=False)
    endTime = db.Column(db.String(50), nullable=False)

class Enrollment(db.Model, UserMixin):
    __tablename__ = "enrollments"

    def __init__(self, id, student_id, class_id):
        self.id = id
        self.student_id = student_id
        self.class_id = class_id

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.student_id'), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'), nullable=False)

    student = db.relationship('Student', backref='enrollments', lazy=True)
    classes = db.relationship('Classes', backref='enrollments', lazy=True)
