from models import Users, Note, Comments, db

class NoteRepository:

    def get_all_notes(self):
        all_notes = Note.query.all()
        return all_notes

    def create_note(self, title, course, descript, content):#, creator_id):
        new_notes = Note(title=title, course=course, descript=descript, content=content)#, creator_id=creator_id)    
        db.session.add(new_notes)
        db.session.commit()
        return new_notes
    
    def get_note_by_id(self, note_id):
        #just in case
        #single_note = Note.query.get_or_404(note_id)
        single_note = Note.query.filter(Note.note_id == note_id).first()
        return single_note

    def get_comments(self, note_id):
        return Comments.query.filter(Comments.thread_id == note_id).all()

    def search_by_author(self, author):
        author_id = Users.query.filter(Users.username.ilike(f'%{author}%')).first()
        return Note.query.filter(Note.creator_id == author_id).all()
    
    def search_by_title(self, title):
        return Note.query.filter(Note.title.ilike(f'%{title}%')).all()
    
    def search_by_course(self, course):
        return Note.query.filter(Note.course.ilike(f'%{course}%')).all()

note_repository_singleton = NoteRepository()


class UserRepository:

    def create_user(self, username, email, password):
        new_user = Users(username=username, email=email, pw=password)
        db.session.add(new_user)
        db.session.commit()
    
    def get_user(self, username):
        my_user = Users.query.filter_by(username=username).first()
        print(my_user)
        return my_user
        
user_repository_singleton = UserRepository()