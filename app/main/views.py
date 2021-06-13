from flask import render_template
from . import main
from flask_login import login_required

#Views
@main.route('/')
def index():
  '''
  View root page function that returns the index page and its data
  '''
  title = "Home Page"
  return render_template('index.html', title = title)

