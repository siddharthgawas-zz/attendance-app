from attendance_app import app,db
from flask import request, jsonify
import attendance_app.util as util
from flask.json import  loads,dumps
import base64
import re
from attendance_app import exc_codes as exc
from http import HTTPStatus
from attendance_app import models
import bcrypt
import datetime
import hashlib
import uuid

@app.route('/',methods=['GET'])
def greet():
    return 'Test Server Student-App'

@app.route('/login/',methods=['POST'])
@util.authenticate_app
def login():
    """
    Basic Authentication
    :return:
    """
    try:
        authorization = request.headers['Authorization']
        match_group = re.match('^Basic ([a-zA-Z0-9=]+)$',authorization)
        if match_group is None:
            raise KeyError
        authorization = match_group.group(1)
        authorization = base64.b64decode(authorization)
        username,pwd = tuple(authorization.decode().split(':'))
        student = models.StudentLoginModel.query.filter_by(username=username).first()
        if student is None:
            raise exc.UserNotFound
        if not bcrypt.checkpw(pwd.encode(),student.password.encode()):
            raise exc.PasswordDidNotMatch
        response = jsonify(code=exc.LOGIN_SUCCESS[0],status=exc.LOGIN_SUCCESS[1],
                           api_token=student.api_key,user_id=student.student.ID)
        return response

    except KeyError:
        response = jsonify(status=exc.UNAUTHORIZED_ACCESS[1],code=exc.UNAUTHORIZED_ACCESS[0])
        response.status_code = HTTPStatus.UNAUTHORIZED
        return response
    except (exc.UserNotFound, exc.PasswordDidNotMatch)as e:
        response = jsonify(status=e.msg, code=e.code)
        response.status_code = HTTPStatus.UNAUTHORIZED
        return response

@app.route('/get-student-details/<int:id>/',methods=['GET'])
@util.authenticate_app
@util.authenticate_user
def get_student_details(user_id,id):
    student = models.StudentModel.query.filter_by(ID = user_id).first()
    course = models.CourseModel.query.filter_by(COURSEID=student.COURSEID).first()
    if id == user_id and course is not None:
        return jsonify(name=student.STUDENTNAME,roll_no=student.ROLLNO,
                       status='Student Found',code=200,course={'id':int(course.COURSEID),
                                                               'name':course.COURSE_NAME,
                                                               'cname':course.CNAME})
    else:
        return jsonify(status=exc.UserNotFound.msg,code=exc.UserNotFound.code)

@app.route('/get-subject-list/<string:c_name>/<int:sem_no>/<string:course_type>/',methods=['GET'])
@util.authenticate_app
@util.authenticate_user
def get_subject_list(user_id,c_name,sem_no,course_type):
    course=models.CourseModel.query.filter_by(CNAME=c_name).first()
    subject_list=[]
    if course is not None:
        subjects = models.SubjectModel.query.filter\
            ((models.SubjectModel.COURSEID==course.COURSEID)&(models.SubjectModel.SEM_NO==sem_no))
        subjects = subjects.filter_by(COURSETYPE=course_type)

        for subject in subjects:
            subject_list.append(dict(id=int(subject.SUBJECTID),name=subject.SUBJECT_NAME,
                                     lect_per_week=int(subject.LECT_PER_WEEK),
                                     prac_per_week=int(subject.PRAC_PER_WEEK),
                                     tut_per_week=int(subject.TUT_PER_WEEK),
                                     course_type=subject.COURSETYPE))

        return jsonify(subject_list)
    else:
        response = jsonify(code=400,status='Invalid Course')
        response.status_code = HTTPStatus.BAD_REQUEST
        return response

@app.route('/get-course-types/',methods=['GET'])
@util.authenticate_app
@util.authenticate_user
def get_course_types(user_id):
    types = []
    for value in db.session.query(models.SubjectModel.COURSETYPE).distinct().all():
        types.append(value[0])
    response = jsonify(total_types=len(types),types=types,status='Types Found',code=200)
    return response

@app.route('/get-attendance/<int:year>/<int:sem_no>/<string:roll_no>/')
@util.authenticate_app
@util.authenticate_user
def get_attendance(user_id,year,sem_no,roll_no):
    try:

        try:
            subject_id = request.args['subject_id']
        except KeyError:
            subject_id = None
        try:
            from_date = request.args['from_date']
            from_date = datetime.datetime.strptime(from_date,'%d-%m-%Y').date()

        except KeyError:
            from_date = None
        try:
            to_date = request.args['to_date']
            to_date = datetime.datetime.strptime(to_date, '%d-%m-%Y').date()
        except KeyError:
            to_date = None

        attendance =models.AttendanceModel.query.filter((models.AttendanceModel.SEM_NO==sem_no) &
                                                        (models.AttendanceModel.YEAR==year)
                                                    & (models.AttendanceModel.ROLLNO==roll_no))
        if subject_id is not None:
            attendance = attendance.filter_by(SUBJECTID=subject_id)

        attendance = attendance.all()
        util.convert_date_of_attendance(attendance)
        attendance = util.get_attendance_between_dates(attendance,from_date,to_date)
        attendance_counts = util.get_attendance_counts(attendance)
        result = []
        for a in attendance:
            sub = models.SubjectModel.query.filter_by(SUBJECTID=a.SUBJECTID).first()
            data=dict(id=int(a.ID),subject_name=sub.SUBJECT_NAME,subject_type=a.SUBJECT_TYPE,
                      date_of_attendance=a.date_of_att.strftime('%d-%m-%Y'),
                      lecture_starttime=a.LECTURE_STARTTIME,
                      att_status=a.ATT_STATUS,
                      faculty_name=a.USERNAME)
            result.append(data)
        response = jsonify(p_count=attendance_counts[0],a_count=attendance_counts[1]
                           ,d_count=attendance_counts[2],
                           data=result,status='Attendance Results Found',code=200)
        return response

    except KeyError:
        response = jsonify(code=400,status='Please Provide roll_no,from_date,to_date.')
        response.status_code = HTTPStatus.BAD_REQUEST
        return response

@app.route('/change-password/<int:id>/',methods=['POST'])
@util.authenticate_app
@util.authenticate_user
def change_password(user_id,id):
    try:
        if user_id != id:
            return jsonify(code=401, status='Unauthorized User')
        json_data = loads(request.data)
        old_password = json_data['old_password']
        new_password = json_data['new_password']
        roll_no = models.StudentModel.query.filter_by(ID=user_id).first().ROLLNO
        student = models.StudentLoginModel.query.filter_by(username=roll_no).first()
        existing_password = student.password
        if not bcrypt.checkpw(old_password.encode(), existing_password.encode()):
            response = jsonify(status=exc.PasswordDidNotMatch.msg,
                               code=exc.PasswordDidNotMatch.code)
            response.status_code = HTTPStatus.UNAUTHORIZED
            return response
        student.password = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()
        key = uuid.uuid4()
        hash_sha256 = hashlib.sha256((str(key)).encode())
        student.api_key = hash_sha256.hexdigest()
        db.session.commit()
        response = jsonify(code=exc.PASSWORD_CHANGED[0], status=exc.PASSWORD_CHANGED[1])
        return response
    except KeyError:
        response = jsonify(code=400,status='Please Provide old_password and new_password')
        response.status_code = HTTPStatus.BAD_REQUEST
        return response
