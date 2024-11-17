from flask import Blueprint
from . import personalized

# Create the blueprint
personalized_bp = Blueprint('personalized', __name__)

# Import and initialize routes
personalized.init_routes(personalized_bp)
