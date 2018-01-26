from attendance_app import db

class StudentModel(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(255),nullable=False)
    roll_no = db.Column(db.String(10),nullable=False,unique=True)

class StudentLoginModel(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    student_id = db.Column(db.Integer,db.ForeignKey('student_model.id',ondelete='CASCADE'),nullable=False,unique=True)
    pwd = db.Column(db.String(255),nullable=False,
                    default='$2b$12$lgh1fNHyW2WcmBeY0h6kG.qIuKuxOW3foJ333tsoEKpQdP5OXLpWe')
    api_token = db.Column(db.String(255),nullable=False,unique=True)
    student = db.relationship('StudentModel',backref='login',uselist=False,lazy=True)

class SemesterModel(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String,unique=True,nullable=False)
    semester_code = db.Column(db.String(10),unique=True,nullable=False)
    total_lectures = db.Column(db.Integer,nullable=False,default=0)
    subjects = db.relationship('SubjectModel',backref='semester',lazy=True)

class SubjectModel(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(255),unique=True,nullable=False)
    code=db.Column(db.String(10),unique=True,nullable=False)
    total_lectures = db.Column(db.Integer,nullable=False,default=0)
    sem_id = db.Column(db.Integer,db.ForeignKey('semester_model.id',ondelete='SET NULL'))