from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime, date


db = SQLAlchemy()
bcrypt = Bcrypt()

DEFAULT_IMG ="https://www.pngitem.com/pimgs/m/146-1468479_my-profile-icon-blank-profile-picture-circle-hd.png"

def connect_db(app):
    db.app = app
    db.init_app(app)



class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True) 
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)      
    username = db.Column(db.String(30), nullable=False, unique=True)    
    email = db.Column(db.Text, nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    profile_img = db.Column(db.Text, default=DEFAULT_IMG)
    location = db.Column(db.Text)    
    jobs = db.relationship("Job", backref="user", cascade="all, delete-orphan")

    @classmethod
    def signup(cls, first_name, last_name, username, email, password, profile_img, location):
        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            first_name = first_name,
            last_name = last_name,
            username=username,
            email=email,
            password=hashed_pwd,
            profile_img=profile_img,
            location=location                    
        )

        db.session.add(user)
        return user


    @classmethod
    def authenticate(cls, username, password):
        
        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False
     



class Job(db.Model):
    __tablename__ = 'jobs'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    company = db.Column(db.Text, nullable=False)
    location = db.Column(db.Text, nullable=False)   
    description = db.Column(db.Text)
    created = db.Column(db.DateTime, nullable=False, default=datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'company': self.company,
            'location': self.location,
            'description': self.description,
            'created': self.created
        }
    