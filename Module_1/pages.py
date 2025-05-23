from flask import Blueprint, render_template

# Define a Blueprint for the Contact page
contact_bp = Blueprint("contact", __name__, template_folder='templates')

# Define a Blueprint for the Home page
home_bp = Blueprint("home", __name__, template_folder='templates')

# Define a Blueprint for the Projects page

projects_bp = Blueprint("projects", __name__, template_folder='templates')

# Route for the Contact page
@contact_bp.route('/contact')
def contact():
  return render_template('contact.html')

# Route for the Home page
@home_bp.route('/')
def home():
  return render_template('home.html')

# Route for the Projects page
@projects_bp.route('/projects')
def projects():
  return render_template('projects.html')