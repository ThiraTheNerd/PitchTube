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
  upvotes = db.relationship('Upvote', backref = 'pitch', lazy = 'dynamic')
  downvotes = db.relationship('Downvote', backref = 'pitch', lazy = 'dynamic')
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
  category= db.Column(db.String())

  def __repr__(self):
    return f'Pitch {self.pitch}'

class User(UserMixin,db.Model):
  __tablename__ = 'users'
  id = db.Column(db.Integer, primary_key = True)
  username = db.Column(db.String(255))
  email = db.Column(db.String(255), unique = True, index = True)
  pitches = db.relationship('Pitch', backref = 'user', lazy = "dynamic")
  comments = db.relationship('Comment', backref = 'user', lazy = 'dynamic')
  upvotes = db.relationship('Upvote', backref = 'user', lazy = 'dynamic')
  downvotes = db.relationship('Downvote', backref = 'user', lazy = 'dynamic')
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
class Comment(db.Model):
  __tablename__ = "comments"

  id = db.Column(db.Integer, primary_key = True)
  comment = db.Column(db.String(), nullable = False)
  posted_date = db.Column(db.DateTime, default = datetime.utcnow())
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
  pitch_id = db.Column(db.Integer, db.ForeignKey('pitches.id'))

  def save(self):
    db.session.add(self)
    db.session.commit()

  @classmethod
  def get_comments(cls,pitch_id):
    comments = Comment.query.filter_by(pitch_id=pitch_id).all()
    return comments


class Upvote(db.Model):
    __tablename__ = 'upvotes'

    id = db.Column(db.Integer,primary_key=True)
    upvote = db.Column(db.Integer, default = 1)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    pitch_id = db.Column(db.Integer,db.ForeignKey('pitches.id'))
    

    def save(self):
      db.session.add(self)
      db.session.commit()

    @classmethod
    def get_upvotes(cls,id):
      upvote = Upvote.query.filter_by(pitch_id=id).all()
      return upvote


    def __repr__(self):
      return f'{self.user_id}:{self.pitch_id}'

class Downvote(db.Model):
  __tablename__ = 'downvotes'

  id = db.Column(db.Integer,primary_key=True)
  user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
  pitch_id = db.Column(db.Integer,db.ForeignKey('pitches.id'))
  

  def save(self):
      db.session.add(self)
      db.session.commit()
  @classmethod
  def get_downvotes(cls,id):
      downvote = Downvote.query.filter_by(pitch_id=id).all()
      return downvote

  def __repr__(self):
      return f'{self.user_id}:{self.pitch_id}'