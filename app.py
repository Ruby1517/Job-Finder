import os
from flask import Flask, request, render_template, g, redirect, flash, url_for, session, jsonify, json
import requests
from dotenv import load_dotenv
load_dotenv()
from sqlalchemy.exc import IntegrityError
from models import db, connect_db, User, Job
from forms import EditProfileForm, SignUpForm, LoginForm, SearchJobsForm, CreateJobForm, EditJobForm
from urllib.parse import urlencode

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///jobSearch-app'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")

connect_db(app)

############ API App_key and App_ID ############
BASE_URL = "https://api.adzuna.com/v1/api"
BASE_PARAMS = "&results_per_page=20&content-type=application/json"

APP_ID = os.getenv('APP_ID')
APP_KEY = os.getenv('APP_KEY')
################################################################################
## User signup/login/logout

CURR_USER_KEY = 'curr_user'

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
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                username=form.username.data,
                email=form.email.data,
                password=form.password.data,
                profile_img=form.profile_img.data or User.profile_img.default.arg,
                location=form.location.data                
            )
            db.session.commit()            

        except IntegrityError:
            flash("Username already taken, please try again", 'danger') 
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

@app.route('/users/search-job', methods =["GET", "POST"])
def get_jobs_list():
    
    form = SearchJobsForm()

    if form.validate_on_submit():
        title = form.title.data     
        location = form.location.data
        country = 'us'            
        
        query_params = urlencode({"app_id": APP_ID, "app_key": APP_KEY, "what":title, "where":location })
        response = requests.get(f"{BASE_URL}/jobs/{country.lower()}/search/1?{query_params}{BASE_PARAMS}")
            
         ####### reset form
        form.title.data = ""
        form.location.data = ""
        
        if response.status_code not in range(200, 299):
            return {}
        results = response.json()['results'] 
        print(results)      
        return render_template('search.html', results=results, form=form)


@app.route('/users/<int:user_id>/favorites')
def favorite_jobs(user_id):
    user = User.query.get_or_404(user_id)
    return render_template("favorites.html", user=user)  



########## User's created Jobs  ###########

@app.route('/users/<int:user_id>')
def profile(user_id):

    user = User.query.get_or_404(user_id)    
    jobs = (Job.query.filter(Job.user_id == user_id).all())
    
    return render_template("profile.html", user=user, jobs=jobs)   

@app.route('/users/<int:user_id>/edit')
def Update_profile(user_id):
    user = User.query.get_or_404(user_id)
    form = EditProfileForm(obj=user)
    return render_template("edit_profile.html", form=form)

    #if form.validate_on_submit():
    #    if User.authenticte(User.username, form.password.data):
    #        user.first_name = form.first_name.data
    #        user.last_name = form.last_name.data
    #        user.username = form.username.data
    #        user.email = form.email.data
    #        user.profile_img = form.profile_img.data
    #        user.location = form.location.data
#
    #        db.session.commit()
    #        return redirect(f'/users/{user_id}')       
    #    flash("Invalid Password, please try again", "danger")
    #return render_template("edit_profile.html", form=form)

################### Add New Job #################

@app.route('/users/<int:user_id>/jobs/add', methods=["GET", "POST"])
def create_job(user_id):
    if not g.user:
        flash("For add new job you should login", "danger")
        return redirect("/login") 

    user = User.query.get_or_404(user_id)    
    form = CreateJobForm(obj=user)    

    if form.validate_on_submit():
        title = form.title.data
        company = form.company.data
        location = form.location.data
        description = form.description.data

        new_job = Job(title=title, company=company, 
                        location=location, description=description, user_id=g.user.id)
        
        db.session.add(new_job)
        db.session.commit()
        flash(f"Job '{new_job.title}' posted.", 'success')      
       
        return redirect(f"/users/{g.user.id}")
    return render_template("add_job.html", form=form)  
     
@app.route("/jobs/<int:job_id>", methods=["GET","POST"])
def job_update(job_id):   
    
    job = Job.query.get_or_404(job_id)      
    form = EditJobForm(obj=job)
    if form.validate_on_submit():
        if job.user_id == g.user.id:
            job.title = form.title.data
            job.company = form.company.data
            job.location = form.location.data
            job. description = form.description.data

           
            db.session.commit() 

            flash(f"Job '{job.title}' Updated.", 'success')
            return redirect("/users/{job.user_id}")
        
    return render_template("edit_job.html", job=job, form=form)
    
@app.route("/jobs/<int:job_id>/delete", methods=["POST"])
def job_remove(job_id):
    
    job = Job.query.get_or_404(job_id)  
    if job.user_id == g.user.id:
        db.session.delete(job)
        db.session.commit()
        flash(f"The {job.title} is deleted", 'danger')

    return redirect(f"/users/{job.user_id}")
   
    



