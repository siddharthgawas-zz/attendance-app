from attendance_app import app,db
from flask import request, jsonify
from http import HTTPStatus
from functools import wraps
import attendance_app.exc_codes as exc
from attendance_app.config import  APPLICATION_KEY as KEY
import re
from attendance_app import models as models

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
            student = models.StudentLoginModel.query.filter_by(api_token = token_key).first()
            if student is None:
                raise KeyError
            student = student.student
            kwargs['user_id']=student.id
            return some_func(*args,**kwargs)

        except KeyError:
            response = jsonify(status=exc.UNAUTHORIZED_ACCESS[1],code=exc.UNAUTHORIZED_ACCESS[0])
            response.status_code = HTTPStatus.UNAUTHORIZED
            return response
    return wrapper