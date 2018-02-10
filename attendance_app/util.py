from attendance_app import app,db
from flask import request, jsonify
from http import HTTPStatus
from functools import wraps
import attendance_app.exc_codes as exc
from attendance_app.config import  APPLICATION_KEY as KEY
import re
from attendance_app import models as models
import datetime

def authenticate_app(some_func):
    @wraps(some_func)
    def wrapper(*args,**kwargs):
        try:
            application_key = request.headers['X-Application-Key']
            if application_key!=KEY:
                raise KeyError
            return some_func(*args,**kwargs)
        except KeyError:
            response = jsonify(status=exc.UNAUTHORIZED_ACCESS[1],code=exc.UNAUTHORIZED_ACCESS[0])
            response.status_code = HTTPStatus.UNAUTHORIZED
            return response
    return wrapper

def authenticate_user(some_func):
    @wraps(some_func)
    def wrapper(*args,**kwargs):
        try:
            token_key = request.headers['Authorization']
            match_group = re.match('^Token ([a-z0-9]+)$',token_key)
            if match_group is None:
                raise KeyError
            token_key = match_group.group(1)
            student = models.StudentLoginModel.query.filter_by(api_key = token_key).first()
            if student is None:
                raise KeyError
            student = student.student
            kwargs['user_id']=student.ID
            return some_func(*args,**kwargs)

        except KeyError:
            response = jsonify(status=exc.UNAUTHORIZED_ACCESS[1],code=exc.UNAUTHORIZED_ACCESS[0])
            response.status_code = HTTPStatus.UNAUTHORIZED
            return response
    return wrapper

def get_attendance_counts(attendance):
    """
    Calculates attendance counts in a list of AttendanceModel objects.
    :param attendance: BaseQuery object of AttendanceModel class
    :return: returns tuple of (present,absent,duty)
    """
    count_a = 0
    count_p = 0
    count_d = 0
    for a in attendance:
        if a.ATT_STATUS == 'A':
            count_a+=1
        elif a.ATT_STATUS == 'D':
            count_d+=1
        elif a.ATT_STATUS == 'P':
            count_p+=1
    return (count_p,count_a,count_d)

def convert_date_of_attendance(attendance):
    """
    Converts string date to date object
    :param attendance: List of AttendanceModel objects or AttendanceModel object
    :return:
    """
    if isinstance(attendance,list):
        for a in attendance:
            a.date_of_att = datetime.datetime.strptime(a.DATE_OF_ATTENDANCE,'%d/%m/%Y').date()
    elif isinstance(attendance,models.AttendanceModel):
        attendance.date_of_att = datetime.datetime.strptime\
            (attendance.DATE_OF_ATTENDANCE, '%d/%m/%Y').date()

def get_attendance_between_dates(attendance:list,from_date:datetime.date,to_date:datetime.date):
    att = []
    if from_date is not None:
        for a in attendance:
            if a.date_of_att >= from_date:
                att.append(a)
        attendance = att

    att = []
    if to_date is not None:
        for a in attendance:
            if a.date_of_att <=to_date:
                att.append(a)
        attendance = att
    return attendance
    pass