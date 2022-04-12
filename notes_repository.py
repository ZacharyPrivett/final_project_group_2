from models import Users, Notes, Courses, Comments, db

class NoteRepository:

    def get_all_notes(self):
        all_notes = Notes.query.all()
        return all_notes


    def search_notes(self, title):
        search = "%{}%".format(title)
        pos_notes = Note.query.filter(Note.title.like(search)).all()

    def get_note_by_id(self, note_id):
        return Notes.query.filter(Notes.note_id == note_id).first()

    def get_comments(self, note_id):
        return Comments.query.filter(Comments.thread_id == note_id).all()

    def search_by_author(self, author):
        author_id = Users.query.filter(Users.username.ilike(f'%{author}%')).first()
        return Notes.query.filter(Notes.creator_id == author_id).all()
    
    def search_by_title(self, title):
        return Notes.query.filter(Notes.title.ilike(f'%{title}%')).all()
    
    def search_by_course(self, course):
        course_id = Courses.query.filter(Courses.title.ilike(f'%{course}%')).first()
        return Notes.query.filter(Notes.course_id == course_id).all()

note_repository_singleton = NoteRepository()