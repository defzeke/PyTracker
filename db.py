# from flask_sqlalchemy import SQLAlchemy

# db = SQLAlchemy()

# class User(db.Model):
#     """
#     User model for the login_sql table.
#     Represents a user with control number, name, ID number, role, password, and email.
#     """
#     __tablename__ = 'login_sql'     # Name of the table in the database
#     control_no = db.Column('Control No.', db.Integer, primary_key=True)      # Primary key 
#     name = db.Column(db.String(100))    
#     ID_number = db.Column(db.String(50), unique=True) # Unique id number for the user to prevent dupes
#     role = db.Column(db.String(20))
#     password = db.Column(db.String(100))
#     email = db.Column(db.String(100), unique=True)   # Unique email for the user to prevent dupes
    
    
    
# class Registration(db.Model):
#     """
#     Registration model for the registration_sql table.
#     Represents a registration entry with control number, temp_ID, name, email, role, and status.
#     """
#     __tablename__ = 'registration_sql'
#     control_no = db.Column('Control No.', db.Integer, primary_key=True)
#     temp_ID = db.Column(db.String(20))
#     name = db.Column(db.String(100))
#     email = db.Column(db.String(100), unique=True)
#     role = db.Column(db.String(20))
#     status = db.Column(db.String(20))
    


# class Enrollment(db.Model):
#     """
#     Enrollment model for the enrollment_database_sql table.
#     Represents an enrollment entry with control number, enrollment ID, student ID, and class ID.
#     """
#     __tablename__ = 'enrollment_database_sql'
#     control_no = db.Column('Control No.', db.Integer, primary_key=True)
#     enrollment_ID = db.Column(db.String(20), unique=True)
#     student_ID = db.Column(db.String(50))
#     class_ID = db.Column(db.String(50))
    
    
    
# class Class(db.Model):
#     """
#     Class model for the classes_database_sql table.
#     Represents a class entry with control number, class ID, subject, semester, teacher ID, and status.
#     """
#     __tablename__ = 'classes_database_sql'
#     control_no = db.Column('Control No.', db.Integer, primary_key=True)
#     class_ID = db.Column(db.String(50))
#     subject = db.Column(db.String(100))
#     semester = db.Column(db.String(20))
#     teacher_ID = db.Column(db.String(50))
#     status = db.Column(db.String(20))
    
    

# class Attendance(db.Model):
#     """
#     Attendance model for the attendance_database_sql table.
#     Represents an attendance entry with control number, date, class ID, student ID, and status.
#     """
#     __tablename__ = 'attendance_database_sql'
#     control_no = db.Column('Control No.', db.Integer, primary_key=True)
#     date = db.Column(db.String(20))
#     class_ID = db.Column(db.String(50))
#     student_ID = db.Column(db.String(50))
#     status = db.Column(db.String(20))