## Description
Job Search Web APP was created to connect users to find a job. In this project user can apply for jobs, save them to favorites, post new jobs and edit them. 

## Features

- access the website as a User
- edit user's profile
- view available jobs on the search page
- save jobs to favorites to apply later
- apply from search page and get redirected to Adzuna website for more information about the job 
- post new jobs
- delete/edit posted 

## Installation

- create virtual environment and activate it

```terminal
$python3 -m venv venv
$source venv/bin/activate
```

- install all requirements

```terminal
$pip install -r requirements.txt
```

- start the app in localhost

```terminal
$flask run
```

## Tests

- to run tests, use respective commands in command line
  
```terminal
$python3 -m test_app.py
$python3 -m test_models.py
```

## API Used
This App was made using the [Adzuna API](https://api.adzuna.com) , which provided all the jobs


## Thechnology

- Web/Frontend
  - JavaScript | CSS | HTML
  
- Frontend Libraries/Frameworks
  - Bootstrap | jQuery | Axios | Jinja
  
- Server/Backend
  - Python | SQL | PostgreSQL

- Backend Libraries/Frameworks
  - Flask | Flask-SQLAlchemy



## Database Schema:

![db_schema](./static/img/dbSchema.png)


	
