from models import Users, Note, Comments, db

class NoteRepository:

    def get_all_notes(self):
        all_notes = Note.query.all()
        return all_notes

    def create_note(self, title, course, description, notes):
        new_notes = Note(title=title, course=course, description=description, notes=notes)
        db.sesion.add(new_notes)
        db.sesion.commit()

    def get_note_by_id(self, note_id):
        return Note.query.filter(Note.note_id == note_id).first()

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