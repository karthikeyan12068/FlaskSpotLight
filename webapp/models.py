from datetime import datetime
from webapp import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    #To get user by an id
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    #Adding cloumns to User table
    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(20), unique=True, nullable=False)
    email=db.Column(db.String(120), unique=True, nullable=False)
    image_file=db.Column(db.String(20), nullable=False, default='default.jpg')
    password=db.Column(db.String(60), nullable=False)

    #The below create a imaginary column called author that returns the authorn who has created for the posts and applyicable one to many relatio
    posts= db.relationship('Post', backref='author', lazy=True)
    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.image_file}','{self.password}')"

class Post(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(100), nullable=False)
    date_posted=db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content=db.Column(db.Text, nullable=False)
    #Here lower case bcoz we referencing the table and attribute but in above we eferensing clas to class relationship
    user_id=db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    def __repr__(self):
        return f"User('{self.title}','{self.date_posted}')"