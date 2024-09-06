import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')

    # Local database URL for development/testing
    LOCAL_DATABASE_URL = 'postgresql://postgres:postresql.2024@localhost:5432/user_db'

    # Default to the DATABASE_URL from the environment (used in production/server)
    DATABASE_URL = os.getenv('DATABASE_URL', LOCAL_DATABASE_URL)

    # Append sslmode=require for Heroku's PostgreSQL connection
    if DATABASE_URL.startswith('postgres://'):
        DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)  # Ensure correct URI scheme
        DATABASE_URL += '?sslmode=require'

    # Flask environment (development or production)
    FLASK_ENV = os.getenv('FLASK_ENV', 'production')
