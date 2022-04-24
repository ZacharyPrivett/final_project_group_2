import re
from tokenize import String
from flask import Flask, flash, redirect, render_template, request, session, abort
from flask_bcrypt import Bcrypt
from notes_repository import note_repository_singleton, user_repository_singleton 
from models import db
import os
from dotenv import load_dotenv


load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#app.config['SQLALCHEMY_ECHO'] = True
app.secret_key = os.getenv('SECRET_KEY')

db.init_app(app)
bcrypt = Bcrypt(app)

# Index
@app.get('/')
def index():
    return render_template('index.html')

# login
@app.get('/login/page')
def get_login_page():
    if 'user' in session:
        flash("You are already logged in")
        return redirect('/dashboard')
    return render_template('login.html')


@app.post('/login')
def login():
    username = request.form.get('username', '')
    password = request.form.get('pw', '')

    if username == '' or password == '':
        abort(400)

    existing_user = user_repository_singleton.get_user(username) 

    if not existing_user or existing_user.user_id == 0:
        return redirect('/fail')

    if not bcrypt.check_password_hash(existing_user.pw, password):
        return redirect('/fail')

    session['user'] = {
        'username': username,
        'user_id': existing_user.user_id
    }

    return redirect('/success')

    #return render_template('login.html')

@app.get('/fail')
def fail():
    if 'user' in session:
        return redirect('/success')
    return render_template('fail.html')

@app.get('/success')
def success():
    if not 'user' in session:
        abort(401)
    return render_template('dashboard.html', user=session['user']['username'])


#logout
@app.get('/logout/page')
def get_logout_page():
    if 'user' not in session:
        flash("No user logged in")
        return render_template('login.html')
    return render_template('logout.html')


@app.post('/logout')
def logout():
    if 'user' not in session:
        abort(401)

    del session['user']

    return redirect('/')


# Signup
@app.get('/signup')
def get_signup_page():
    if 'user' in session:
        return redirect('/success')
    return render_template('signup_page.html')    

@app.post('/signup')
def signup():
    username = request.form.get('username', '')
    email = request.form.get('email', '')
    password = request.form.get('pw', '')
    repeat_pw = request.form.get('pw2', '' )

    if password != repeat_pw or username == '' or password == '' or repeat_pw == '':
        abort(400)

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    user_repository_singleton.create_user(username, email, hashed_password)
    return redirect('/login/page')


# Creating new notes
@app.get('/notes/new')
def create_note_form():
    if 'user' not in session:
        return redirect('/login/page')

    return render_template('add_notes.html', add_notes_active=True,)

@app.post('/notes')
def create_note():
    title = request.form.get('title', '')
    course = request.form.get('course', '')
    descript = request.form.get('descript', '')
    content = request.form.get('content', '')
    #creator_id = 1  # so code doesnt break. Will update when we have login made
    note_repository_singleton.create_note(title, course, descript, content)#, creator_id)
    return redirect('/notes/new')


# Dashborad
@app.get('/dashboard')
def dashboard():
    return render_template('dashboard.html')


# Search and view notes
@app.get('/search')
def search_notes():
    found_notes = []
    q = request.args.get('q', '')
    filter = request.args.get('filter', '')
    if q != '':
        if filter == 'Course':
            found_notes = note_repository_singleton.search_by_course(q)
        elif filter == "Author":
            found_notes = note_repository_singleton.search_by_author(q)
        else:
            found_notes = note_repository_singleton.search_by_title(q)
    
    return render_template('search_notes.html', search_active=True, notes=found_notes, search_query=q)

@app.get('/single_note/<note_id>')
def single_note(note_id):
    single_note = note_repository_singleton.get_note_by_id(note_id)
    return render_template('single_note_page.html', note=single_note)

@app.get('/notes/list')
def view_all_notes():
    all_notes = note_repository_singleton.get_all_notes()
    return render_template('view_all_notes.html', list_notes_active=True, notes=all_notes)


# About
@app.get('/about')
def about():
    return render_template('about.html')

