from flask_login import UserMixin
from . import db
from sqlalchemy.sql import func
from flask_sqlalchemy import SQLAlchemy

students_courses = db.Table(
    "students_courses",
    db.Column("student_id", db.Integer, db.ForeignKey("students.student_id")),
    db.Column("course_id", db.Integer, db.ForeignKey("courses.course_id")),
)

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

    courses = db.relationship("Course", secondary=students_courses, backref="students")

    def get_id(self):
        return (self.student_id)

    def __repr__(self):
        return f"id: {self.student_id}, email: {self.account}, name: {self.name}"

class Course(db.Model, UserMixin):
    __tablename__ = "courses"


    def __init__(self, id, number, name, teacher, classroom, date, time, credit,outline):

        self.course_id = id
        self.number = number
        self.name = name
        self.teacher = teacher
        self.classroom = classroom
        self.date = date
        self.time = time
        self.credit = credit
        self.outline = outline

    course_id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    teacher = db.Column(db.String(50), nullable=False)
    classroom = db.Column(db.String(50), nullable=False)
    date = db.Column(db.String(50), nullable=False)
    time = db.Column(db.String(50), nullable=False)
    credit = db.Column(db.Integer, nullable=False)
    outline = db.Column(db.String(500), nullable=False)

    def get_id(self):
        return (self.course_id)

    # students = db.relationship("Student", secondary=students_courses, backref="courses")

class Enrollment(db.Model, UserMixin):
    __tablename__ = "enrollments"

    def __init__(self, student_id, class_id):
        self.student_id = student_id
        self.class_id = class_id

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.student_id'), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('courses.course_id'), nullable=False)

    student = db.relationship('Student', backref='enrollments', lazy=True)
    course = db.relationship('Course', backref='enrollments', lazy=True)

class Follow(db.Model, UserMixin):
    __tablename__ = "follow"

    def __init__(self, student_id, class_id):
        self.student_id = student_id
        self.class_id = class_id

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.student_id'), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('courses.course_id'), nullable=False)

    student = db.relationship('Student', backref='follow', lazy=True)
    classes = db.relationship('Course', backref='follow', lazy=True)