from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from datetime import date

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///moringa.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ----------------- MODELS -----------------

class Mentor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    expertise = db.Column(db.String(200), nullable=False)
    

    students = db.relationship('Student', back_populates='mentor', cascade="all, delete-orphan")
    cohorts = db.relationship('Cohort', back_populates='mentor', cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Mentor {self.name}>'

class Cohort(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)

    mentor_id = db.Column(db.Integer, db.ForeignKey('mentor.id'), nullable=False)

    mentor = db.relationship('Mentor', back_populates='cohorts')
    students = db.relationship('Student', back_populates='cohort', cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Cohort {self.name}>'

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    course = db.Column(db.String(200), nullable=False)

    mentor_id = db.Column(db.Integer, db.ForeignKey('mentor.id'), nullable=False)
    cohort_id = db.Column(db.Integer, db.ForeignKey('cohort.id'), nullable=False)

    mentor = db.relationship('Mentor', back_populates='students')
    cohort = db.relationship('Cohort', back_populates='students')

    def __repr__(self):
        return f'<Student {self.name}>'

# ----------------- ROUTES -----------------

@app.route('/top_mentors')
def top_mentors():
    top_mentors = (
        db.session.query(
            Mentor.name,
            func.count(Student.id).label('student_count')
        )
        .join(Student)
        .group_by(Mentor.id)
        .order_by(func.count(Student.id).desc())
        .limit(5)
        .all()
    )

    result = {mentor: student_count for mentor, student_count in top_mentors}
    return jsonify(result)

@app.route('/')
def home():
    return "Moringa Flask MVP is running!"

# ----------------- RUN -----------------

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
