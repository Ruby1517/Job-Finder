from flask_wtf import FlaskForm
from flask_wtf.recaptcha import validators
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, Optional  



class SignUpForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])    
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    profile_img = StringField("(Optional) Profile Picture")
    location = StringField('Location (city, state)')
   


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()]) 
    password = PasswordField('Password', validators=[Length(min=6)])  
    
    
class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])    
    email = StringField('Email', validators=[DataRequired(), Email()])    
    profile_img = StringField("(Optional) Profile Picture")
    location = StringField('Location (city, state)')
   


class SearchJobsForm(FlaskForm):
    title = StringField('Job Title', validators=[DataRequired()])    
    location = StringField('Location', validators=[DataRequired()])


class CreateJobForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    company = StringField('Company Name', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()]) 
    description = TextAreaField('Description')
 

 