Job search web app
Features:
- Create a profile
- Search for jobs
- Add new jobs
- Edit jobs
- Delete jobs

Functionality:
- Upon entering the webpage, a user can choose to sign up for login and search jobs
- Once logged in as a user, user will be able to add/edit/delete created job



Database Schema:
- User:id, username, email, password
- Job :id, title, company, location, description, User_id(ForeignKey)

Technicalities:
This App was made using the Adzuna API, which provided all the jobs

	
Technologies Used:
- Python
- Flask
- Flask-Bcrypt
- Flask-SQLAlchemy
- Postgresql
- Flask-WTForms
- Jinja
- HTML
- CSS

