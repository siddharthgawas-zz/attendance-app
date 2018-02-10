from attendance_app import db

class StudentModel(db.Model):
    __table__ = db.Model.metadata.tables['STUDENT_TABLE']

    def __repr__(self):
        return self.ROLLNO

class CourseModel(db.Model):
    __table__ = db.Model.metadata.tables['COURSE_TABLE']

    def __repr__(self):
        return self.CNAME

class FacultyModel(db.Model):
    __table__ = db.Model.metadata.tables['FACULTY_TABLE']

    def __repr__(self):
        return self.FACULTYNAME

class SubjectModel(db.Model):
    __table__ = db.Model.metadata.tables['SUBJECT_TABLE']

class AttendanceModel(db.Model):
    __table__ = db.Model.metadata.tables['STUDENT_ATT_TABLE']
    date_of_att = None

class StudentLoginModel(db.Model):
    __table_args__ = {'extend_existing': True}
    username = db.Column(db.String(10),db.ForeignKey('STUDENT_TABLE.ROLLNO'
                                               ,ondelete='CASCADE'),primary_key=True)
    password = db.Column(db.String(255),nullable=False)
    api_key = db.Column(db.String(255),nullable=False,unique=True)
    student = db.relationship('StudentModel',backref='student_login',lazy=True)