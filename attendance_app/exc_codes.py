UNAUTHORIZED_ACCESS = (401,'Unauthorized Access')
LOGIN_SUCCESS = (2001,'Login Successful')
class UserNotFound(BaseException):
    msg = 'User Was Not Found'
    code = 1001

class PasswordDidNotMatch(BaseException):
    msg = 'Password Did Not Match'
    code = 1002

