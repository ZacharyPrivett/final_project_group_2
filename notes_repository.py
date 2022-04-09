from models import User, Note, Cousre, db

class NoteRepository:

    def get_all_notes(self):
        all_notes = Note.query.all()
        return all_notes


note_repository_singleton = NoteRepository()