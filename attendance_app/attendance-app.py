from attendance_app import app
from attendance_app import db
import attendance_app.util as util

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8000)
