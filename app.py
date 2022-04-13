from flask import Flask, redirect, render_template, request
from notes_repository import note_repository_singleton
from models import db

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:1120@localhost:3306/[db name]'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

db.init_app(app)

@app.get('/')
def index():
    return render_template('index.html')

@app.get('/notes')
def create_notes():
    title = request.form.get('title', '')
    course = request.form.get('course', '')
    description = request.get('description', '')
    notes = request.get('notes', '')

    create_notes = note_repository_singleton.create_notes(title, course, description, notes)
    return redirect(f'/notes/')


@app.get('/search')
def search_notes():
    found_notes = []
    q = request.args.get('q', '')
    if q != '':
        found_notes = note_repository_singleton.search_notes(q)
    return render_template('search_notes.html', search_active=True, movies=found_notes, search_query=q)

@app.get('/notes/list')
def view_all_notes():
    all_notes = note_repository_singleton.get_all_notes()
    return render_template('view_all_notes.html', list_notes_active=True, notes=all_notes)

@app.get('/about')
def about():
    return render_template('about.html')