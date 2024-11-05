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

class Classes(db.Model):
    __tablename__ = "classes"

    def __init__(self, id, name, teacher, classroom, time):
        self.id = id
        self.name = name
        self.teacher = teacher
        self.classroom = classroom
        self.time = time

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    teacher = db.Column(db.String(50), nullable=False)
    classroom = db.Column(db.String(50), nullable=False)
    time = db.Column(db.String(50), nullable=False)