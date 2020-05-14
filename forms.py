""" Forms for MyNotes App """

from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length, NumberRange, Optional
from flask_wtf import FlaskForm

class RegisterForm(FlaskForm):
  """ User registration form. """

  username = StringField(
    "Username", 
    validators=[InputRequired(), Length(min=1, max=20)]
  )
  password = PasswordField(
    "Password", 
    validators=[InputRequired(), Length(min=6, max=30)]
  )
  email = StringField(
    "Email", 
    validators=[InputRequired(), Length(max=30)]
  )
  first_name = StringField(
    "First Name", 
    validators=[InputRequired(), Length(max=30)]
  )
  last_name = StringField(
    "Last Name", 
    validators=[InputRequired(), Length(max=30)]
  )
  
class LoginForm(FlaskForm):
  """ User login form. """
  username = StringField(
    "Username", 
    validators=[InputRequired(), Length(min=2, max=20)]
  )
  password = PasswordField(
    "Password", 
    validators=[InputRequired(), Length(min=6, max=30)]
  )

class AddNoteForm(FlaskForm):
  """ Form to add a new note """
  title = StringField(
    "Title",
    validators=[InputRequired(), Length(min=2, max=30)]
  )
  content = StringField(
    "Content",
    validators=[InputRequired(), Length(max=200)]
  )

class UpdateNoteForm(FlaskForm):
  """ Form to add a new note """
  title = StringField(
    "Title",
    validators=[InputRequired(), Length(min=2, max=30)]
  )
  content = StringField(
    "Content",
    validators=[InputRequired(), Length(max=200)]
  )

class DeleteForm(FlaskForm):
  """ """

