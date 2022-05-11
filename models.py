import profile
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Users(db.Model):
    __tablename__ = 'Users'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    profile_pic = db.Column(db.Text, nullable=False)
    pw = db.Column(db.String, nullable=False)
    # A user can have many notes
    user_notes = db.relationship('Note', backref='author')
    # Deletes users notes when account is deleted
    delete = db.relationship('Note', cascade='all, delete-orphan')

class Note(db.Model):
    __tablename__ = 'Note'
    note_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    course = db.Column(db.String, nullable=False)
    descript = db.Column(db.String, nullable=False)
    content = db.Column(db.Text, nullable=False)
    likes = db.Column(db.Integer, nullable=False, default = 0)
    creator_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'), nullable=False)

    def to_dict(self):
        return {
            "noteId": self.note_id,
            "title":self.title,
            "course": self.course,
            "descript": self.descript,
            "content": self.content,
            "likes": self.likes,
            "creatorId": self.creator_id,
        }

    def __repr__(self):
        return f'Note({self.note_id}, {self.title}, {self.course}, {self.descript}, {self.content}, {self.creator_id})'
        
class Comments(db.Model):
    __tablename__ = 'Comments'
    comment_id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String, nullable=False)
    time_stamp = db.Column(db.String, nullable=False)
    commenter_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'), nullable=True)
    username = db.Column(db.String, nullable = True)
    thread_id = db.Column(db.Integer, db.ForeignKey('Note.note_id'), nullable=False)

