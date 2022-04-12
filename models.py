from click import password_option
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Users(db.Model):
    user_id = db.column(db.Integer, primary_key=True)
    username = db.column(db.String, nullable = False, unqiue = True)
    email = db.column(db.String, nullable = False, unique = True)
    pw = db.column(db.String, nullable = False)

class Notes(db.Model):
    note_id = db.column(db.Integer, primary_key = True)
    title = db.column(db.String, nullable = False)
    description = db.columns(db.String, nullable = False)
    content = db.column(db.String, nullable = False)
    course_id = db.columns(db.String, db.ForeignKey('Courses.course_id'), nullable = False)
    creator_id = db.column(db.Integer, db.ForeignKey('Users.user_id'), nullable = False)

class Courses(db.Model):
    course_id = db.column(db.Integer, primary_key = True)
    course = db.column(db.String, nullable = False)
    
class Comments(db.Model):
    comment_id = db.column(db.Integer, primary_key = True)
    content = db.column(db.String, nullable = False)
    timestamp = db.column(db.DateTime, nullable = False)
    commenter_id = db.column(db.Integer, db.ForeignKey('Users.user_id'), nullable = False)
    thread_id = db.column(db.String, db.ForeignKey('Notes.note_id'), nullable = False)
