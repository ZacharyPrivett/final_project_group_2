from models import User, Note, Cousre, db

class NoteRepository:

    def get_all_notes(self):
        all_notes = Note.query.all()
        return all_notes

    def search_notes(self, title):
        search = "%{}%".format(title)
        pos_notes = Note.query.filter(Note.title.like(search)).all()
        return pos_notes     


note_repository_singleton = NoteRepository()