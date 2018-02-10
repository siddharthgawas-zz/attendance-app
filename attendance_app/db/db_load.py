from attendance_app import app,db
import csv
import bcrypt
import attendance_app.models as models
from attendance_app import config

def load_db():
    db.drop_all()
    db.create_all()
    load_student()
    load_login()
    load_faculty()
    load_course()
    load_subject()
    load_attendance()

def load_student():
    with open('student.csv') as f:
        reader = csv.DictReader(f)
        for row in reader:
            student = models.StudentModel()
            student.ID = row['id']
            student.STUDENTNAME = row['name']
            student.ROLLNO = row['roll_no']
            student.COURSEID = row['course_id']
            db.session.add(student)
        db.session.commit()

def load_login():
    with open('student_login.csv') as f:
        reader = csv.DictReader(f)
        for row in reader:
            student = models.StudentLoginModel()
            student.username = row['roll_no']
            student.api_key = row['api_key']
            hashed_pwd = bcrypt.hashpw(config.DEFAULT_PASSWORD.encode('utf-8'),bcrypt.gensalt())
            student.password = hashed_pwd.decode()
            db.session.add(student)
        db.session.commit()

def load_faculty():
    with open('faculty.csv','r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            faculty = models.FacultyModel()
            faculty.FACULTYID = row['faculty_id']
            faculty.FACULTYNAME = row['faculty_name']
            db.session.add(faculty)
        db.session.commit()

def load_course():
    with open('course.csv','r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            course = models.CourseModel()
            course.COURSEID = row['course_id']
            course.COURSE_NAME = row['course_name']
            course.CNAME = row['cname']
            db.session.add(course)
        db.session.commit()

def load_subject():
    with open('subject.csv','r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            subject = models.SubjectModel()
            subject.SUBJECTID = row['subject_id']
            subject.SUBJECT_NAME = row['subject_name']
            subject.SEM_NO = row['sem_no']
            subject.COURSEID = row['course_id']
            subject.LECT_PER_WEEK = row['lect_per_week']
            subject.PRAC_PER_WEEK = row['prac_per_week']
            subject.TUT_PER_WEEK = row['tut_per_week']
            subject.COURSETYPE = row['course_type']
            db.session.add(subject)
        db.session.commit()

def load_attendance():
    with open('attendance.csv','r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            attendance = models.AttendanceModel()
            attendance.ID = row['id']
            attendance.COURSEID = row['course_id']
            attendance.SEM_NO = row['sem_no']
            attendance.SUBJECTID  = row['subject_id']
            attendance.ROLLNO  = row['roll_no']
            attendance.SUBJECT_TYPE = row['subject_type']
            attendance.DATE_OF_ATTENDANCE= row['date_of_attendance']
            attendance.LECTURE_STARTTIME = row['lecture_starttime']
            attendance.ATT_STATUS = row['att_status']
            attendance.YEAR = row['year']
            attendance.USERNAME = row['username']
            db.session.add(attendance)
        db.session.commit()

if __name__ == '__main__':
    load_db()