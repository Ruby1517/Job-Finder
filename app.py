import os
from flask import Flask, request, render_template, g, redirect, Response, flash, url_for, session, jsonify
import requests
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
BASE_URL = "http://api.adzuna.com/v1/api"
APP_ID = "7bfce7b9"
APP_KEY = "c5eb2f3758b9d308b4440736c4ac509a"
BASE_PARAMS = 'search/1?&results_per_page=20&content-type=application/json'

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
            flash(f"Hello, {user.username}!", "success")
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

    flash("You have successfuly logged out.", "success")
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
        return render_template("home.html", form=form)

    else:
        return render_template("home-anon.html")    

################################################################
### Using API

@app.route('/users/search-job', methods=["POST", "GET"])
def get_jobs_list():      
    
    data = request.json
    print(data)
    
    form = SearchJobsForm(csrf_enabled=False, data=data)
    
    if form.validate_on_submit():
        title = data['title']      
        location = data['location']
        country = 'us'          
        
        query_params = urlencode({"app_id": APP_ID, "app_key": APP_KEY, "what":title, "where":location })
        response = requests.get(f"{BASE_URL}/jobs/{country.lower()}/search/1?{query_params}")
        if response.status_code not in range(200, 299):
            return {}
        #print(response.json())
        res_data = response.json()  
        for result in res_data['results']:
            print(result['title'])
            print(result['company']['display_name'])
            print(result['location']['display_name'])            
            print(result['redirect_url'])
            print(result['description'])

        return res_data    
        
             
       
    
    else:
        return jsonify(errors=form.errors)
    

@app.route('/users/create-job')
def create_job_page():
    form = CreateJobForm()
    return render_template("add_job.html", form=form)     


@app.route('/users/create-job', methods=["POST"])
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

        job = Job(title=title, company=company, location=location, description=description)
        db.session.add(job)
        db.session.commit()

        return redirect("/")

    return render_template("add_job.html", form=form)    


    
    
   
    



