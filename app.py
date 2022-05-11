from datetime import datetime
import re
import json
from tokenize import String
from flask import Flask, flash, redirect, render_template, request, session, abort, jsonify
from flask_bcrypt import Bcrypt
from notes_repository import note_repository_singleton, user_repository_singleton 
from models import db
import os
from dotenv import load_dotenv


load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("CLEARDB_DATABASE_URL")
#app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#app.config['SQLALCHEMY_ECHO'] = True
app.secret_key = os.getenv('SECRET_KEY')
db.init_app(app)
bcrypt = Bcrypt(app)


# Index
@app.get('/')
def index():
    if 'user' in session:
        creator_id = session['user']['user_id']
        profile = user_repository_singleton.get_user_by_id(creator_id)
        return render_template('index.html', profile=profile, user=session['user']['username'])
    return render_template('index.html')

# login
@app.get('/login/page')
def get_login_page():
    if 'user' in session:
        creator_id = session['user']['user_id']
        profile = user_repository_singleton.get_user_by_id(creator_id)
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


@app.get('/fail')
def fail():
    if 'user' in session:
        return redirect('/success')
    return render_template('fail.html')

@app.get('/success')
def success():
    if not 'user' in session:
        abort(401)
    return redirect('/dashboard')


#logout
@app.get('/logout/page')
def get_logout_page():
    creator_id = session['user']['user_id']
    profile = user_repository_singleton.get_user_by_id(creator_id)
    if 'user' not in session:
        flash("No user logged in")
        return render_template('login.html')
    return render_template('logout.html', profile=profile, user=session['user']['username'])


@app.post('/logout')
def logout():
    if 'user' not in session:
        abort(401)

    del session['user']
    flash("You have been logged out")
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
    profile_pic = request.form.get('profile_pic', '' )

    if password != repeat_pw or username == '' or password == '' or repeat_pw == '':
        abort(400)

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    user_repository_singleton.create_user(username, email, hashed_password, profile_pic)
    return redirect('/login/page')


# Creating new notes
@app.get('/notes/new')
def create_note_form():
    creator_id = session['user']['user_id']
    profile = user_repository_singleton.get_user_by_id(creator_id)
    if 'user' not in session:
        return redirect('/login/page')
    return render_template('add_notes.html', add_notes_active=True, profile = profile, user=session['user']['username'])


@app.post('/notes')
def create_note():
    title = request.form.get('title', '')
    course = request.form.get('course', '')
    descript = request.form.get('descript', '')
    content = request.form.get('content', '')
    creator_id = session['user']['user_id']
    note_repository_singleton.create_note(title, course, descript, content, creator_id)
    return redirect('/notes/new')


# Dashborad
@app.get('/dashboard')
def dashboard():
    if 'user' in session:
        creator_id = session['user']['user_id']
        profile = user_repository_singleton.get_user_by_id(creator_id)
        author = session['user']['user_id']
        user_notes = []
        user_notes = note_repository_singleton.get_notes_by_author(author)
        return render_template('dashboard.html', notes=user_notes, profile=profile, user=session['user']['username'])
    return redirect('/login/page')

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
    if 'user' in session:
        creator_id = session['user']['user_id']
        profile = user_repository_singleton.get_user_by_id(creator_id)
        return render_template('search_notes.html', search_active=True, notes=found_notes, profile=profile, search_query=q, user=session['user']['username'])
    return render_template('search_notes.html', search_active=True, notes=found_notes, search_query=q)

#Single Notes
@app.route('/single_note/<note_id>', methods=['GET', 'POST'])
def single_note(note_id):
    
    single_note = note_repository_singleton.get_note_by_id(note_id)
    comment = note_repository_singleton.get_comments(note_id)

    users = user_repository_singleton.get_all_user()

    if request.method == 'POST':
        content = request.form.get('comment','')
        time_stamp = datetime.utcnow().strftime('%B %d %Y - %H:%M')
        thread_id = note_id
        username = session['user']['username']
        note_repository_singleton.create_comment(content=content, time_stamp=time_stamp, username=username, thread_id=thread_id)
        comment = note_repository_singleton.get_comments(note_id)
    if 'user' in session:
        creator_id = session['user']['user_id']
        profile = user_repository_singleton.get_user_by_id(creator_id)
        return render_template('single_note_page.html', note=single_note, comments = comment, users=users, profile=profile, user=session['user']['username'], liked='0')
    return render_template('single_note_page.html', note=single_note,  liked='0')
    
@app.post('/single_note/<note_id>')
def single_note_like(note_id):
    single_note = note_repository_singleton.get_note_by_id(note_id)
    index = request.form.get('liked')
    single_note.likes = int(request.form.get('likes'))
    db.session.commit()
    if 'user' in session:
        creator_id = session['user']['user_id']
        profile = user_repository_singleton.get_user_by_id(creator_id)
        return render_template('single_note_page.html', note=single_note, profile=profile, user=session['user']['username'],liked=index)
    return render_template('single_note_page.html', note=single_note,liked=index)   

#Liking a Post
@app.get('/liked/<note_id>')
def single_note_likes_get(note_id):
    noteId = note_id.replace("<","").replace(">","")
    single_note = note_repository_singleton.get_note_by_id(int(noteId))
    return jsonify(single_note.to_dict())

@app.post('/liked/<note_id>')
def single_note_likes_post(note_id):
    noteId = note_id.replace("<","").replace(">","")
    single_note = note_repository_singleton.get_note_by_id(noteId)
    data = json.dumps(request.get_json())
    data = data.partition(":")[2].replace("}","").strip()
    single_note.likes = int(data)
    db.session.commit()
    return jsonify(single_note.to_dict())

#view all notes
@app.get('/notes/list')
def view_all_notes():
    all_notes = note_repository_singleton.get_all_notes()
    if 'user' in session:
        creator_id = session['user']['user_id']
        profile = user_repository_singleton.get_user_by_id(creator_id)
        return render_template('view_all_notes.html', list_notes_active=True, notes=all_notes, profile=profile, user=session['user']['username'])
    return render_template('view_all_notes.html', list_notes_active=True, notes=all_notes)

#edit notes page 
@app.get('/notes/<note_id>/edit')
def edit_notes(note_id):
    if 'user' not in session:
        return redirect('/login/page')
    creator_id = session['user']['user_id']
    profile = user_repository_singleton.get_user_by_id(creator_id)
    note_to_edit =  note_repository_singleton.get_note_by_id(note_id)
    return render_template('edit_notes.html', note=note_to_edit, profile=profile, user=session['user']['username'])

#update_notes
@app.post('/notes/<note_id>/edit')
def update_notes(note_id):
    creator_id = session['user']['user_id']
    profile = user_repository_singleton.get_user_by_id(creator_id)
    if 'user' not in session:
        abort(401)
    note_to_update = note_repository_singleton.get_note_by_id(note_id)
    title = request.form.get('title', '')
    course = request.form.get('course', '')
    descript = request.form.get('descript', '')
    content = request.form.get('content', '')
    #will add some testing later 
    note_to_update.title = title
    note_to_update.course = course
    note_to_update.descript = descript
    note_to_update.content = content
    db.session.commit()
    return render_template('edit_notes.html', note=note_to_update, profile=profile, user=session['user']['username'])

#update comments
@app.post('/comment/<comment_id>/edit')
def update_comments(comment_id):
    creator_id = session['user']['user_id']
    profile = user_repository_singleton.get_user_by_id(creator_id)
    comment_to_update = note_repository_singleton.get_comment_by_id(comment_id)
    content = request.form.get('content', '')
    comment_to_update.content = content
    db.session.commit()
    return render_template('edit_comments.html', comment=comment_to_update, profile=profile, user=session['user']['username'])

@app.get('/comment/<comment_id>/edit')
def edit_comments(comment_id):
    comment_to_update = note_repository_singleton.get_comment_by_id(comment_id)
    creator_id = session['user']['user_id']
    profile = user_repository_singleton.get_user_by_id(creator_id)
    return render_template('edit_comments.html', comment=comment_to_update, profile = profile, user=session['user']['username'])

#delete method
@app.post('/notes/<note_id>/delete')
def delete_note(note_id):
    if 'user' not in session:
        abort(401)

    creator_id = session['user']['user_id']
    profile = user_repository_singleton.get_user_by_id(creator_id)

    note_to_delete = note_repository_singleton.get_note_by_id(note_id)
    db.session.delete(note_to_delete)
    db.session.commit()
    return redirect('/dashboard')

#delete comments
@app.post('/comment/<comment_id>/delete')
def delete_comment(comment_id):
    comment_to_delete = note_repository_singleton.get_comment_by_id(comment_id)
    db.session.delete(comment_to_delete)
    db.session.commit()
    return redirect('/dashboard')

#view comments
#changed it back to the original 
@app.route('/notes/<note_id>/comments', methods=['GET', 'POST'])
def view_comments(note_id):
    creator_id = session['user']['user_id']
    profile = user_repository_singleton.get_user_by_id(creator_id)
    single_note = note_repository_singleton.get_note_by_id(note_id)
    comment = note_repository_singleton.get_comments(note_id)
    if request.method == 'POST':
        content = request.form.get('comment','')
        time_stamp = datetime.utcnow().strftime('%B %d %Y - %H:%M')
        thread_id = note_id
        username = session['user']['username']
        commenter_id = session['user']['user_id']
        note_repository_singleton.create_comment(content=content, time_stamp=time_stamp, username=username, thread_id=thread_id, commenter_id=commenter_id)
        comment = note_repository_singleton.get_comments(note_id)
    return render_template('comments.html', note=single_note, comments = comment, profile = profile, user=session['user']['username'])

#get single Comment
@app.get('/comment/<comment_id>')
def get_single_comment(comment_id):
    single_comment = note_repository_singleton.get_comment_by_id(comment_id)
    creator_id = session['user']['user_id']
    profile = user_repository_singleton.get_user_by_id(creator_id)
    return render_template('single_comment.html', comment=single_comment, profile= profile, user=session['user']['username'])

# About
@app.get('/about')
def about():
    if 'user' in session:
        creator_id = session['user']['user_id']
        profile = user_repository_singleton.get_user_by_id(creator_id)
        return render_template('about.html', profile=profile, user=session['user']['username'])
    return render_template('about.html')

# edit user page
@app.get('/edit/<user_id>/page')
def edit_user_page(user_id):
    creator_id = session['user']['user_id']
    profile = user_repository_singleton.get_user_by_id(creator_id)
    if 'user' not in session:
        abort(401)
    user_to_edit = user_repository_singleton.get_user_by_id(user_id)

    return render_template('edit_user_info.html', edit_login_active=True, profile=profile, user=session['user']['username'], user_to_edit=user_to_edit)


# edit username and email
@app.post('/edit/user/<user_id>')
def edit_user(user_id):
    if 'user' not in session:
        abort(401)
    user_to_edit = user_repository_singleton.get_user_by_id(user_id)    
    user_to_edit.username = request.form.get('username', '')
    user_to_edit.email = request.form.get('email', '')
    user_to_edit.profile_pic = request.form.get('profile_pic', '')
    db.session.commit()
    # deletes "old user" from session
    del session['user']
    # creates session with newly updated useraneme
    session['user'] = {
    'username': user_to_edit.username,
    'user_id': user_id
    }
    return redirect('/dashboard')

# edit password page
@app.get('/edit/<user_id>/password/page')
def edit_password_page(user_id):
    creator_id = session['user']['user_id']
    profile = user_repository_singleton.get_user_by_id(creator_id)
    if 'user' not in session:
        abort(401)
    pw_to_edit = user_repository_singleton.get_user_by_id(user_id)
    
    return render_template('edit_password.html', edit_login_active=True, profile=profile, user=session['user']['username'], pw_to_edit=pw_to_edit)

#edit password
@app.post('/edit/<user_id>/password')
def edit_password(user_id):
    if 'user' not in session:
        abort(401)
    pw_to_edit = user_repository_singleton.get_user_by_id(user_id)
    pw1 = request.form.get('password', '')
    pw2 = request.form.get('password_confirm' '')
    if pw1 != pw2:
        abort(400)
    hashed_password = bcrypt.generate_password_hash(pw1).decode('utf-8')
    pw_to_edit.pw = hashed_password
    db.session.commit()
    return redirect('/dashboard')

# delete user page
@app.get('/delete/user/<user_id>/page')
def delete_user_page(user_id):
    creator_id = session['user']['user_id']
    profile = user_repository_singleton.get_user_by_id(creator_id)
    if 'user' not in session:
        abort(401)
    user_to_delete = user_repository_singleton.get_user_by_id(user_id)
    return render_template('delete_user_page.html', profile=profile, user_id=user_to_delete)

# delete user
@app.post('/delete/user/<user_id>')
def delete_user(user_id):
    if 'user' not in session:
        abort(401)
    user_to_delete = user_repository_singleton.get_user_by_id(user_id)
    db.session.delete(user_to_delete)
    db.session.commit()
    del session['user']
    return redirect('/')

