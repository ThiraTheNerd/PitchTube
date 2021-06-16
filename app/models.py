from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from . import login_manager
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
  return User.query.get(int(user_id))

class Pitch(db.Model):
  __tablename__ = 'pitches'

  id = db.Column(db.Integer, primary_key = True)
  pitch = db.Column(db.String())
  posted_date = db.Column(db.DateTime, default = datetime.utcnow(), nullable = False)
  content = db.Column(db.String())
  comments = db.relationship('Comment', backref = 'pitch', lazy = 'dynamic')
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
  category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))


  def __repr__(self):
    return f'Pitch {self.pitch}'

class Comment(db.Model):
  __tablename__ = "comments"

  id = db.Column(db.Integer, primary_key = True)
  comment = db.Column(db.String())
  posted_date = db.Column(db.DateTime, default = datetime.utcnow())
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
  pitch_id = db.Column(db.Integer, db.ForeignKey('pitches.id'))

  def __repr__(self):
    return f'Comment {self.comment}'


class Category(db.Model):
  __tablename__ = 'categories'
  id = db.Column(db.Integer, primary_key = True)
  category_name = db.Column(db.String(255))
  pitches = db.relationship('Pitch', backref = 'category', lazy = 'dynamic')

  def __repr__(self):
    return f'Category {self.category_name}'


class User(UserMixin,db.Model):
  __tablename__ = 'users'
  id = db.Column(db.Integer, primary_key = True)
  username = db.Column(db.String(255))
  email = db.Column(db.String(255), unique = True, index = True)
  pitches = db.relationship('Pitch', backref = 'user', lazy = "dynamic")
  comments = db.relationship('Comment', backref = 'user', lazy = 'dynamic')
  bio = db.Column(db.String(255))
  profile_pic_path = db.Column(db.String(), default = 'app/static/photos/default.png')
  pass_secure = db.Column(db.String(255))

  @property
  def password(self):
    raise AttributeError('You cannot read the password attribute')

  @password.setter
  def password(self, password):
    self.pass_secure = generate_password_hash(password)

  def verify_password(self,password):
    return check_password_hash(self.pass_secure,password)


  def __repr__(self):
    return f'User {self.username}'