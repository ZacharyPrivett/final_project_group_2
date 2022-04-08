from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, true

db = SQLAlchemy()

# Just getting started on this. 
# This is written b4 sql db is finalized so change anything that needs to be changed

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)


class Note(db.Model):
    note_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    notes = db.Colum(db.String, nullable=False)
    creator_id = db.Column(db.Integer, db.foreign_key('user_id'))  #Not exactly sure how foreign key works here
    course_id = db.Column(db.Interger, db.foreign_key('course_id')) #Not exactly sure how foreign key works here

class Course(db.Model):
    course_id = db.Column(db.Integer, primary_key=True)
    course = db.Column(db.String, nullable=False)

