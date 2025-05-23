# Import Flask and render_template for rendering HTML pages
from flask import Flask, Blueprint, render_template
from pages import contact_bp, home_bp, projects_bp

# Create a Flask application instance
app = Flask(__name__)
app.register_blueprint(contact_bp)
app.register_blueprint(home_bp)
app.register_blueprint(projects_bp)

# Run the app in debug mode if this file is executed directly
if __name__ == "__main__":
    app.run(debug=True)
