from flask import Blueprint, render_template

contact_bp = Blueprint("contact", __name__, template_folder='templates')
home_bp = Blueprint("home", __name__, template_folder='templates')
projects_bp = Blueprint("projects", __name__, template_folder='templates')

@contact_bp.route('/contact')
def contact():
  return render_template('contact.html')

@home_bp.route('/')
def home():
  return render_template('home.html')

@projects_bp.route('/projects')
def projects():
  return render_template('projects.html')