from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Mentor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    expertise = db.Column(db.String(100))

    students = db.relationship("Student", backref="mentor", lazy=True)


class Cohort(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)

    mentor_id = db.Column(db.Integer, db.ForeignKey("mentor.id"))


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    course = db.Column(db.String(100))

    mentor_id = db.Column(db.Integer, db.ForeignKey("mentor.id"))
    cohort_id = db.Column(db.Integer, db.ForeignKey("cohort.id"))
