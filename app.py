import os
from flask import Flask, request, render_template, g, redirect, flash, url_for, session, jsonify
import requests
from dotenv import load_dotenv
load_dotenv()
import json
from sqlalchemy.exc import IntegrityError
from models import db, connect_db, User, Job
from forms import ProfileForm, SignUpForm, LoginForm, SearchJobsForm, CreateJobForm
from urllib.parse import urlencode

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///jobSearch-app'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")

connect_db(app)
#db.drop_all()
db.create_all()



CURR_USER_KEY = 'curr_user'

############ API App_key and App_ID############

BASE_URL = "https://api.adzuna.com/v1/api"
BASE_PARAMS = "search/1?&results_per_page=20&content-type=application/json"
APP_ID = os.getenv('APP_ID')
APP_KEY = os.getenv('APP_KEY')


################################################################################
## User signup/login/logout

@app.before_request
def add_user_to_g():
    """ If we're logged in, add curr user to Flask global"""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None    


def do_login(user):
    session[CURR_USER_KEY] = user.id


def do_logout():

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


@app.route('/signup', methods=["GET", "POST"])
def signup():
        

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

    form = SignUpForm()
    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                email=form.email.data,
                password=form.password.data
            )
            db.session.commit()

        except IntegrityError:
            flash("Username already taken", 'danger') 
            return render_template('signup.html', form=form)  

        do_login(user)
        return redirect("/")         

    else:
        return render_template("signup.html", form=form)



@app.route('/login', methods=["GET", "POST"])
def login():
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.authenticte(form.username.data,form.password.data)


        if user:
            do_login(user)            
            return redirect("/")

        flash("Invalid username/password.", "danger")   

    return render_template('login.html', form=form)   


# User Profile
#@app.route('/users')
#def profile():
#    user = User.query.get(session[CURR_USER_KEY])
#    form = ProfileForm(obj=user)   
#    
#
#    return render_template("profile.html", form=form, user_id=user.id)    

@app.route('/logout')
def logout():

    do_logout()    
    return redirect('/login')


###############################################################
### Home Page

@app.route("/")
def home():
    """
    Show Homepage:

    - anon useres
    - logged in
    """

    if g.user:       
        form = SearchJobsForm()
        return render_template("search.html", form=form)

    else:
        return render_template("home.html")    

################################################################
### Using API

@app.route('/api/search-job', methods =["POST", "GET"])
def get_jobs_list():
    
    form = SearchJobsForm()

    if form.validate_on_submit():
        title = form.title.data     
        location = form.location.data
        country = 'us'            
        
        query_params = urlencode({"app_id": APP_ID, "app_key": APP_KEY, "what":title, "where":location })
        response = requests.get(f"{BASE_URL}/jobs/{country.lower()}/search/1?{query_params}&results_per_page=20&content-type=application/json")
        if response.status_code not in range(200, 299):
            return {}
        print(response.json())
        results = response.json()['results']
        return render_template('search.html', results=results, form=form)



        
        
        
        
    

     

   
@app.route('/api/create-job')
def create_job_page():
    form = CreateJobForm()
    return render_template("add_job.html", form=form)     


@app.route('/api/create-job', methods=["POST"])
def create_job():
    if not g.user:
        flash("For add new job you should login", "danger")
        return redirect("/login")    

    form = CreateJobForm()
    if form.validate_on_submit():
        title = form.title.data
        company = form.company.data
        location = form.location.data
        description = form.description.data

        new_job = Job(title=title, company=company, location=location, description=description)
        db.session.add(new_job)
        db.session.commit()
        response_json = jsonify(job=new_job.serialize())
        return redirect(response_json, 201)

    return render_template("add_job.html", form=form)    


    
    
   
    



