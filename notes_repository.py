from models import Users, Note, Comments, db

class NoteRepository:

    def get_all_notes(self):
        all_notes = Note.query.all()
        return all_notes

    def create_note(self, title, course, descript, content, creator_id):
        new_notes = Note(title=title, course=course, descript=descript, content=content, creator_id=creator_id)    
        db.session.add(new_notes)
        db.session.commit()
        return new_notes
    
    def get_note_by_id(self, note_id):
        #just in case
        #single_note = Note.query.get_or_404(note_id)
        single_note = Note.query.filter(Note.note_id == note_id).first()
        return single_note

    def create_comment(self, content, time_stamp, username, thread_id, commenter_id):
        new_comment = Comments(content=content, time_stamp=time_stamp, username = username, thread_id=thread_id, commenter_id = commenter_id)
        db.session.add(new_comment)
        db.session.commit()
        return new_comment

    def get_comments(self, note_id):
        return Comments.query.filter(Comments.thread_id == note_id).all()
    
    def get_comment_by_id(self, comment_id):
        #single_comment = Comments.query.filter(Comments.comment_id == comment_id)
        single_comment = Comments.query.get_or_404(comment_id)
        return single_comment

    def search_by_author(self, author):
        searched_author = Users.query.filter(Users.username.ilike(f'%{author}%')).first()
        return Note.query.filter(Note.creator_id == searched_author.user_id).all()
    
    def search_by_title(self, title):
        return Note.query.filter(Note.title.ilike(f'%{title}%')).all()
    
    def search_by_course(self, course):
        return Note.query.filter(Note.course.ilike(f'%{course}%')).all()

    def get_notes_by_author(self, author):
        return Note.query.filter(Note.creator_id == author).all()

note_repository_singleton = NoteRepository()


class UserRepository:

    def create_user(self, username, email, password, profile_pic):
        new_user = Users(username=username, email=email, pw=password, profile_pic=profile_pic)
        db.session.add(new_user)
        db.session.commit()
    
    def get_user(self, username):
        my_user = Users.query.filter_by(username=username).first() 
        return my_user
    
    def get_all_user(self):
        all_user = Users.query.all()
        return all_user
        
    def get_user_by_id(self, user_id):
        user_id = Users.query.filter_by(user_id=user_id).first()
        return user_id 
      
user_repository_singleton = UserRepository()