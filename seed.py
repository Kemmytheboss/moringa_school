from flask import Flask
from model import db, Mentor, Cohort, Student
import datetime
from sqlalchemy import func

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///moringa.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


def seed_data():
    db.drop_all()
    db.create_all()

    mentor1 = Mentor(name="Alice Wambui", expertise="Data Science")
    mentor2 = Mentor(name="Sam Tomashi", expertise="Software Development")
    mentor3 = Mentor(name="Bob Marley", expertise="Mobile Development")

    db.session.add_all([mentor1, mentor2, mentor3])
    db.session.commit()

    cohort1 = Cohort(
        name="DSFT12",
        start_date=datetime.date(2024, 1, 10),
        end_date=datetime.date(2024, 6, 10),
        mentor_id=mentor1.id
    )
    cohort2 = Cohort(
        name="SDFT15",
        start_date=datetime.date(2024, 2, 15),
        end_date=datetime.date(2024, 7, 15),
        mentor_id=mentor2.id
    )

    db.session.add_all([cohort1, cohort2])
    db.session.commit()

    students = [
        Student(name="David Chege", course="Data Science", mentor_id=mentor1.id, cohort_id=cohort1.id),
        Student(name="Eva Moraa", course="Data Science", mentor_id=mentor1.id, cohort_id=cohort1.id),
        Student(name="Frank Kipyegon", course="Software Development", mentor_id=mentor2.id, cohort_id=cohort2.id),
    ]

    db.session.add_all(students)
    db.session.commit()


def get_top_mentor():
    return (
        db.session.query(
            Mentor,
            func.count(Student.id).label("student_count")
        )
        .outerjoin(Student)
        .group_by(Mentor.id)
        .order_by(func.count(Student.id).desc())
        .first()
    )


if __name__ == "__main__":
    with app.app_context():
        seed_data()

        mentor, count = get_top_mentor()
        print(f" Top Mentor: {mentor.name} ({count} students)")
