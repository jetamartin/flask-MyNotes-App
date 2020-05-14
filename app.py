""" MyNotes app is flask based app that allows users to create, edit, save and delete personal notes"""

from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from werkzeug.exceptions import Unauthorized

from models import connect_db, db, User, My_Note
from forms import RegisterForm, LoginForm, DeleteForm, AddNoteForm, UpdateNoteForm

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgres:///mynotes"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'jetsSecretKey'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)

connect_db(app)

@app.route('/')
def homepage():
  """ Homepage of site """
  return redirect("/register")

@app.route('/register', methods=['GET', 'POST'])
def register():
  """ Display registration form and process completed reg form """
  if "username" in session:
    return redirect(f"/users/{session['username']}")

  form = RegisterForm()

  if form.validate_on_submit():
    username = form.username.data
    password = form.password.data
    first_name = form.first_name.data
    last_name = form.last_name.data
    email = form.email.data

    user = User.register(username, password, first_name, last_name, email)

    db.session.commit()
    session['username'] = user.username
    flash('Welcome! Successfully created your account!', 'success')

    return redirect(f"/users/{user.username}")

  else:
    return render_template("users/register_user.html", form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
  """ Display login form or process login request """
  if "username" in session:
    return redirect(f"/users/{session['username']}")

  form = LoginForm()
  
  if form.validate_on_submit():
    username = form.username.data
    password = form.password.data

    user = User.authenticate(username, password)

    if user:
      session['username'] = user.username
      flash(f'Welcome back {user.username}!  You are now logged in.', 'success')

      return redirect(f"/users/{user.username}")
    else: 
      form.username.errors = ["Invalid username/password"]
      return render_template("users/login_user.html", form=form)

  return render_template('users/login_user.html', form=form)

@app.route('/logout')
def logout():
  """ Logout user out """
  session.pop("username")
  return redirect("/login")

@app.route('/users/<username>')
def show_user_notes(username):
  """ Display users notes """
  if "username" not in session or username != session["username"]:
    raise Unauthorized()

  user = User.query.get(username)
  form = DeleteForm()

  return render_template("my_notes/show_user_notes.html", user=user, form=form)

@app.route('/users/<username>/my_notes/new', methods=['GET', 'POST'])
def add_new_note(username):
  """ Show add new note form and process it"""

  if "username" not in session or username != session['username']:
    raise Unauthorized

  form = AddNoteForm()

  if form.validate_on_submit():
    title = form.title.data
    content = form.content.data

    new_note = My_Note(
      title = title, 
      content = content, 
      username = username
    )
    
    db.session.add(new_note)
    db.session.commit()

    flash(f'Your note was successfully added', 'success')
    
    return redirect(f"/users/{username}")

  else: 
    return render_template("my_notes/new_note.html", form=form)

@app.route('/my_notes/<int:my_note_id>/update', methods=['GET', 'POST'])
def update_note(my_note_id):
  """ Show update note form and process it"""

  my_note=My_Note.query.get(my_note_id)

  if "username" not in session or my_note.username != session['username']:
    raise Unauthorized

  form = UpdateNoteForm(obj=my_note)

  if form.validate_on_submit():
    my_note.title = form.title.data
    my_note.content = form.content.data
    
    db.session.commit()
    flash(f'Your note was successfully updated!', 'success')

    
    return redirect(f"/users/{my_note.username}")

  else: 
    return render_template("my_notes/update_note.html", form=form)

@app.route('/my_notes/<int:my_note_id>/delete', methods=['POST'])
def delete_note(my_note_id):
  """ Delete a users note """

  my_note=My_Note.query.get(my_note_id)

  if "username" not in session or my_note.username != session['username']:
    raise Unauthorized

  form = DeleteForm()

  if form.validate_on_submit():
    db.session.delete(my_note)
    db.session.commit()
    flash(f'Your note was successfully deleted', 'success')
    
  return redirect(f"/users/{my_note.username}")

@app.route('/users/<username>/delete', methods=['POST'])
def delete_user(username):
  """ Delete a user and all of that users tweets """

  if "username" not in session or username != session['username']:
    raise Unauthorized() 

  user = User.query.get(username)

  db.session.delete(user)
  db.session.commit()
  session.pop('username')
  flash(f'Your account was successfully deleted!', 'success')

  return redirect("/login")
