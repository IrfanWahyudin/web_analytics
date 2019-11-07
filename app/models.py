from app import db
from app import login

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class Location(db.Model):
    location_name = db.Column(db.String(40), primary_key=True)
    lat_long = db.Column(db.String(200))
    created_by = db.Column(db.String(200))
    address = db.Column(db.String(500))
    city = db.Column(db.String(200))
    def __repr__(self):
        return '{}|{}|{}|{}|{}'.format(self.location_name, self.lat_long, self.created_by, self.address, self.city) 

@login.unauthorized_handler
def unauthorized():
    return "<h1>Unauthorized</h1>"

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
    
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '{}|{}|{}|{}|{}'.format(self.id, self.email, self.username, self.address, self.password_hash) 

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Titanic(db.Model):
    # 'PassengerId', 'Survived', 'Pclass', 'Name', 'Sex', 'Age', 'SibSp',
    #    'Parch', 'Ticket', 'Fare', 'Cabin', 'Embarked'],
    #   dtype='object'
    PassengerId = db.Column(db.Float, primary_key = True)
    Survived = db.Column(db.Float)
    Pclass = db.Column(db.Float)
    Name = db.Column(db.String(100))
    Sex = db.Column(db.String(10))
    Age = db.Column(db.Float)
    SibSp = db.Column(db.Float)
    Parch = db.Column(db.Float)
    Ticket = db.Column(db.String(20))
    Fare = db.Column(db.Float)
    Cabin = db.Column(db.String(20))
    Embarked = db.Column(db.String(20))




    



    