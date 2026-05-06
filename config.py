import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Your secret key (fallback for local dev)
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-key-change-me')

    # Use DATABASE_URL if set (e.g. on Render), otherwise default to a local SQLite file
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') \
        or 'sqlite:///' + os.path.join(os.path.dirname(__file__), 'app.db')

    # Disable track modifications
    SQLALCHEMY_TRACK_MODIFICATIONS = False