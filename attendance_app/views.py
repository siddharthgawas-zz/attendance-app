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

@app.route('/',methods=['GET'])
@util.authenticate_app
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
        student = models.StudentModel.query.filter_by(roll_no=username).first()
        if student is None:
            raise exc.UserNotFound
        if not bcrypt.checkpw(pwd.encode(),student.login[0].pwd.encode()):
            raise exc.PasswordDidNotMatch
        response = jsonify(code=exc.LOGIN_SUCCESS[0],status=exc.LOGIN_SUCCESS[1],
                           api_token=student.login[0].api_token,user_id=student.id)
        return response

    except KeyError:
        response = jsonify(status=exc.UNAUTHORIZED_ACCESS[1],code=exc.UNAUTHORIZED_ACCESS[0])
        response.status_code = HTTPStatus.UNAUTHORIZED
        return response
    except (exc.UserNotFound, exc.PasswordDidNotMatch)as e:
        response = jsonify(status=e.msg, code=e.code)
        response.status_code = HTTPStatus.UNAUTHORIZED
        return response
