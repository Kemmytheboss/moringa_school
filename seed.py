from model import app, db, Mentor, Cohort, Student
import datetime

def seed_data():
    db.drop_all()
    db.create_all()

    # Create Mentors
    mentor1 = Mentor(name="Alice Johnson", expertise="Data Science")
    mentor2 = Mentor(name="Bob Smith", expertise="Web Development")
    mentor3 = Mentor(name="Catherine Lee", expertise="Mobile Development")

    db.session.add_all([mentor1, mentor2, mentor3])
    db.session.commit()

    # Create Cohorts
    cohort1 = Cohort(name="DS Jan 2024", start_date=datetime.date(2024, 1, 10), end_date=datetime.date(2024, 6, 10), mentor=mentor1)
    cohort2 = Cohort(name="WD Feb 2024", start_date=datetime.date(2024, 2, 15), end_date=datetime.date(2024, 7, 15), mentor=mentor2)

    db.session.add_all([cohort1, cohort2])
    db.session.commit()

    # Create Students
    student1 = Student(name="David Brown", course="Data Science", mentor=mentor1, cohort=cohort1)
    student2 = Student(name="Eva Green", course="Data Science", mentor=mentor1, cohort=cohort1)
    student3 = Student(name="Frank White", course="Web Development", mentor=mentor2, cohort=cohort2)

    db.session.add_all([student1, student2, student3])
    db.session.commit()