from attendance_app import app,db
import csv
import attendance_app.models as models
def load_db():
    db.drop_all()
    db.create_all()
    load_student()
    load_login()

def load_student():
    with open('student.csv') as f:
        reader = csv.DictReader(f)
        for row in reader:
            student = models.StudentModel()
            student.id = row['id']
            student.name = row['name']
            student.roll_no = row['roll_no']
            db.session.add(student)
        db.session.commit()

def load_login():
    with open('student_login.csv') as f:
        reader = csv.DictReader(f)
        for row in reader:
            student = models.StudentLoginModel()
            student.student_id = row['student_id']
            student.api_token = row['api_token']
            db.session.add(student)
        db.session.commit()

if __name__ == '__main__':
    load_db()