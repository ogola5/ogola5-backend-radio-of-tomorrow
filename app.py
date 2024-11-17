from flask import Flask
from personalized import personalized_bp
from genai import genai_bp
from flask_cors import CORS
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Register blueprints
app.register_blueprint(personalized_bp, url_prefix='/personalized')
app.register_blueprint(genai_bp, url_prefix='/genai')

@app.route('/')
def home():
    return {"message": "Welcome to the main application"}

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
