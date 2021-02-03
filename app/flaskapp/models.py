from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flaskapp import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader  # decorator for managing our sessions
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):  # UserMixin adds some extra methods for login_manager
    id = db.Column(db.Integer, primary_key=True)
    usertype = db.Column(db.String(20), unique=False, nullable=False)
    firstname = db.Column(db.String(20), unique=False, nullable=False, default='')
    lastname = db.Column(db.String(20), unique=False, nullable=False, default='')
    username = db.Column(db.String(50), unique=False, nullable=False, default='')
    email = db.Column(db.String(120), unique=False, nullable=False, default='')
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False, default='0')  # we will hash paswds to 60 chars
    jobs = db.relationship('Job', backref='user', lazy=True)
    profiles = db.relationship('Profile', backref='user', lazy=True)

    def __repr__(self):
        return f"User('{self.firstname}', '{self.lastname}', '{self.email}', '{self.image_file}')"

    def get_reset_token(self, expires_sec=1800):  # create timed tokens for email
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod  # this method won't accept self as an argument
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)


class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    title = db.Column(db.String(100), nullable=False, default='')
    date = db.Column(db.DateTime, nullable=False,
                     default=datetime.utcnow)  # not utcnow() as we want to pass the function as arg not the current time
    skills = db.Column(db.String(100), nullable=False, default='')
    description = db.Column(db.Text, nullable=False, default='')
    category = db.Column(db.String(100), nullable=False, default='')
    subcategory = db.Column(db.String(100), nullable=False, default='')
    payment_type = db.Column(db.String(100), nullable=False, default='')
    budget = db.Column(db.String(100), nullable=False, default='')
    min_budget = db.Column(db.String(100), nullable=False, default='')
    links_quoters = db.Column(db.String(10000), nullable=False, default='')
    links_invited = db.Column(db.String(10000), nullable=False, default='')
    links_hired = db.Column(db.String(10000), nullable=False, default='')

    job_cluster_id = db.Column(db.Integer, nullable=False, default=0)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
                        nullable=False)  # table name user referenced here instead of class name User

    def __repr__(self):
        return f"Job('{self.title}', '{self.skills}', '{self.category}')"

class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    link = db.Column(db.String(100), nullable=False, default='')
    skills = db.Column(db.Text, nullable=False, default='')
    total_feedbacks = db.Column(db.String(100), nullable=False, default='')
    rating = db.Column(db.String(10), nullable=False, default='')
    location = db.Column(db.String(100), nullable=False, default='')
    min_hourly_rate = db.Column(db.String(1000), nullable=False, default='')
    max_hourly_rate = db.Column(db.String(1000), nullable=False, default='')
    min_starting_rate = db.Column(db.String(1000), nullable=False, default='')
    max_starting_rate = db.Column(db.String(1000), nullable=False, default='')
    earnings_annual = db.Column(db.String(100), nullable=False, default='0')
    earnings_alltime = db.Column(db.String(100), nullable=False, default='0')
    earnings_avg = db.Column(db.String(100), nullable=False, default='0')
    member_since = db.Column(db.String(100), nullable=False, default='')
    transactions_completed = db.Column(db.String(100), nullable=False, default='')
    weighted_rating = db.Column(db.String(10), nullable=False, default='1')
    
    profile_cluster_id = db.Column(db.Integer, nullable=False, default=0)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
                        nullable=False)  # table name user referenced here instead of class name User

    def __repr__(self):
        return f"Profile('{self.user.username}', '{self.location}')"