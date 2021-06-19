from flask import render_template,request,redirect, url_for,abort,flash
from . import main
from flask_login import login_required,current_user
from ..models import User, Pitch , Comment, Upvote, Downvote
from .forms import UpdateProfile, PitchForm, CommentForm
from .. import db, photos


#Views
@main.route('/')
def index():
  '''
  View root page function that returns the index page and its data
  '''
  title = "Home Page"
  pitches = Pitch.query.order_by(Pitch.posted_date.desc())
  return render_template('index.html', title = title, pitches = pitches)

@main.route('/user/<uname>')
def profile(uname):
  user  = User.query.filter_by(username = uname).first()
  pitches = Pitch.query.filter_by(user_id = user.id).all()

  if user is None:
    abort(404)
  return render_template('profile/profile.html', user = user, pitches = pitches)

@main.route('/user/update/<uname>', methods = ['GET', 'POST'])
@login_required
def update_profile(uname):
  user = User.query.filter_by(username = uname).first()
  print(user)
  if user is None:
    abort(404)
  prof_updateform = UpdateProfile()

  if prof_updateform.validate_on_submit():
    user.bio = prof_updateform.bio.data

    db.session.add(user)
    db.session.commit()

    return redirect(url_for('.profile', uname = user.username))
  return render_template('profile/update_profile.html', prof_updateform = prof_updateform)

@main.route('/user/<uname>/update/pic', methods = ['POST'])
@login_required
def update_pic(uname):
  user = User.query.filter_by(username = uname).first()
  if 'photo' in request.files:
    filename = photos.save(request.files['photo'])
    path = f'photos/{filename}'
    user.profile_pic_path = path
    db.session.commit()
  return redirect(url_for('main.profile', uname = uname))

@main.route('/pitch/new', methods = ['GET', 'POST'])
@login_required
def new_pitch():
  pitch_form = PitchForm()
  if pitch_form.validate_on_submit():
    pitch = Pitch(pitch=pitch_form.pitch_title.data, content =pitch_form.content.data, 
    user_id = current_user.id,category = pitch_form.category.data)
    db.session.add(pitch)
    db.session.commit()
    flash('Your pitch has been created successfully')
    return redirect(url_for('main.index'))
  return render_template('pitches/new_pitch.html', title = "New Pitch", pitch_form = pitch_form)

@main.route('/pitch/<int:id>')
def pitch(id):
  pitch = Pitch.query.filter_by(id = id).first()
  comments = Comment.query.filter_by(pitch_id = id).all()
  print(comments)
  return render_template('pitches/pitch.html', pitch= pitch, comments = comments)

@main.route('/pitch/<string:category>')
def pitch_category(category):
  pitches = Pitch.query.filter_by(category = category).all()
  if pitches == None:
    flash('No pitches in this category')
  return render_template('pitches/pitch_category.html', pitches = pitches)

@main.route('/pitch/new_comment/<int:id>', methods = ['GET','POST'])
@login_required
def new_comment(id):
  comments = Comment.query.filter_by(pitch_id = id).all()
  form = CommentForm()
  pitch = Pitch.query.filter_by(id = id).first()
  print(pitch.id)
  if form.validate_on_submit():
    comment = form.comment.data
    new_comment = Comment(comment = comment, user_id = current_user.id, pitch_id = pitch.id)
    new_comment.save()

    return redirect(url_for('.pitch', pitch= pitch, comments = comments, id = pitch.id))
  return render_template('pitches/new_comment.html', form = form, pitch = pitch)
