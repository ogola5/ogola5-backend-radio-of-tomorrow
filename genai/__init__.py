from flask import Blueprint
from . import genai

# Create the blueprint
genai_bp = Blueprint('genai', __name__)

# Import and initialize routes
genai.init_routes(genai_bp)