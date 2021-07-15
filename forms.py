from flask_wtf import FlaskForm
from flask_wtf.recaptcha import validators
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Email, Length 



class SignUpForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Length(min=6)])


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()]) 
    password = PasswordField('Password', validators=[Length(min=6)])  
    
    
class EditProfileForm():
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Length(min=6)])


class SearchJobsForm(FlaskForm):
    title = StringField('Job Title', validators=[DataRequired()])    
    location = StringField('Location', validators=[DataRequired()])


class CreateJobForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    company = StringField('Company Name', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()]) 
    description = TextAreaField('Description')
 
