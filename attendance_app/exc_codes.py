UNAUTHORIZED_ACCESS = (401,'Unauthorized Access')
LOGIN_SUCCESS = (2001,'Login Successful')
PASSWORD_CHANGED=(2002,'Password Changed')

class UserNotFound(BaseException):
    msg = 'User Was Not Found'
    code = 1001

class PasswordDidNotMatch(BaseException):
    msg = 'Password Did Not Match'
    code = 1002

