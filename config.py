import os

def load_env_file_bc_dotenv_doesnt_work(filepath = 'local_project.env'):
    try:
        with open(filepath) as file:
            for line in file:
                line = line.strip()
                if line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    os.environ[key] = value
    except FileNotFoundError:
        print(f"Warning: {filepath} file not found. Skipping environment loading.")
    

load_env_file_bc_dotenv_doesnt_work()

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
    else:
        FLASK_ENV = os.getenv('FLASK_ENV', 'development')