import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY') or 'your-secret-key-here'
    UPLOAD_FOLDER = os.path.join('static', 'uploads')  # This creates 'static/uploads'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    MODEL_PATH = 'model/diabetic_retinopathy_model.h5'

DB_CONFIG = {
    'host': os.getenv('DB_HOST') or 'localhost',
    'user': os.getenv('DB_USER') or 'root',
    'password': os.getenv('DB_PASSWORD') or '',
    'database': os.getenv('DB_NAME') or 'retinopathy_db'
}