from . import db

class Pitch(db.Model):
  __tablename__ = 'pitches'

  id = db.Column(db.Integer, primary_key = True)
  pitch = db.Column(db.String())
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
  category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))


  def __repr__(self):
    return f'Pitch {self.pitch}'

class Category(db.Model):
  __tablename__ = 'categories'
  id = db.Column(db.Integer, primary_key = True)
  category_name = db.Column(db.String(255))
  pitches = db.relationship('Pitch', backref = 'category', lazy = 'dynamic')

  def __repr__(self):
    return f'Category {self.category_name}'


class User(db.Model):
  __tablename__ = 'users'
  id = db.Column(db.Integer, primary_key = True)
  username = db.Column(db.String(255))
  pitches = db.relationship('Pitch', backref = 'user', lazy = "dynamic")

  def __repr__(self):
    return f'User {self.username}'