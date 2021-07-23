# Codin User Flow
- First, create your database and fetch the API data for it .

- Next, set up the environmental variables on Flask so it’s configured for development. When this is done, run Flask.

- Import Flask and SQLAlchemy into your database, then set up the app and database objects so you can work with them. Create classes for all of your database tables through SQLAlchemy.

- Now you can begin to serve up Jinja templates to create dynamic Front-end pages.

- Create a new account in the Signup page. If you create the account successfully you can login with a valid username and password and view the search page.

- In the search page insert job title and location on search form to get a list of jobs from API, then you can apply to jobs, also you can save your favorite jobs.

- Click on the username on the navbar, and view the profile page. In this page you can edit the user's profile, post new jobs, view all lists of posted jobs from this user, and view the user's favorite jobs.

- In the Profile page click on the “Post Job” button or click the “Post New Job” menu on the navbar,  the “post new job” page opens. In this page if you enter “Job Title”, “Company Name”, “Location”, “Description” on the form and submit it, a job was created,and back to the profile page.

- In the profile page, section “Posted Jobs” view all lists of posted jobs with current user, also you can edit the job and delete it.

- Click on the “Search Job” menu on the navbar for search desired jobs from API.

- Click on the “Favorite Jobs” menu on the navbar, view all saved jobs, you can apply to your favorite job or delete the job from your favorites list.

