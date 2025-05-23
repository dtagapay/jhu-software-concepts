# Import Flask and render_template for rendering HTML pages
from flask import Flask, render_template

# Create a Flask application instance
app = Flask(__name__)

# Define the route for the homepage
@app.route("/")
def home():
    # Render the home.html template
    return render_template("home.html")

# Define the route for the contact page
@app.route("/contact")
def contact():
    return render_template("contact.html")

# Define the route for the projects page
@app.route("/projects")
def projects():
    return render_template("projects.html")

# Run the app in debug mode if this file is executed directly
if __name__ == "__main__":
    app.run(debug=True)
