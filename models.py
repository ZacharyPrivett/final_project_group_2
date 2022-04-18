from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Users(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    pw = db.Column(db.String, nullable=False)

class Note(db.Model):
    note_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    course = db.Column(db.String, nullable=False)
    descript = db.Column(db.String, nullable=False)
    content = db.Column(db.Text, nullable=False)
    #creator_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=True)

class Comments(db.Model):
    comment_id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String, nullable=False)
    time_stamp = db.Column(db.DateTime, nullable=False)
    commenter_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'), nullable=True)
    thread_id = db.Column(db.String, db.ForeignKey('Notes.note_id'), nullable=False)

def __repr__(self):
    return f'Note({self.note_id}, {self.title}, {self.course}, {self.descript}, {self.content}, {self.creator_id})'