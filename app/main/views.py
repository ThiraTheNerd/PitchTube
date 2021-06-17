from flask import render_template,request,redirect, url_for,abort,flash
from . import main
from flask_login import login_required,current_user
from ..models import User, Pitch , Comment, Upvote, Downvote
from .forms import UpdateProfile, PitchForm
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

  if user is None:
    abort(404)
  return render_template('profile/profile.html', user = user)

@main.route('/user/update/<uname>', methods = ['GET', 'POST'])
@login_required
def update_profile(uname):
  user = User.query.filter_by(username = uname).first()
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
  return render_template('pitches/pitch.html', pitch= pitch)

@main.route('/pitch/<string:category>')
def pitch_category(category):
  pitches = Pitch.query.filter_by(category = category).all()
  return render_template('pitches/pitch_category.html', pitches = pitches)

@main.route('/like/<int:id>', methods = ['POST', 'GET'])
@login_required
def like(id):
  pitch = Pitch.query.get(id)
  new_vote = Upvote(user_id = current_user, pitch_id = pitch )
  print(new_vote)
  # new_vote.save()
  return redirect(url_for('main.index', pitch = pitch))

@main.route('/dislike/<int:id>', methods = ['POST', 'GET'])
@login_required
def dislike(id):
  pitches = Upvote.get_downvotes(id)
  valid_string = f'{current_user.id} : {id}'
  for pitch in pitches:
    to_str = f'{pitch}'
    print(valid_string+" "+to_str)
    if valid_string == to_str:
      return redirect('main.index', id = id)
    else:
      continue
  new_vote = Downvote(user_id = current_user, pitch_id = id )
  new_vote.save()
  return redirect(url_for('main.index', id = id))

