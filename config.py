import os
from urllib.parse import urlparse, urlunparse

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')

    # Local database URL for development/testing
    LOCAL_DATABASE_URL = 'postgresql://postgres:postgresql.2024@localhost:5432/user_db'

    # Default to the DATABASE_URL from the environment (used in production/server)
    DATABASE_URL = os.getenv('DATABASE_URL', LOCAL_DATABASE_URL)

    # Parse the URL to modify its parameters
    parsed_url = urlparse(DATABASE_URL)
    query_params = parsed_url.query

    if os.getenv('FLASK_ENV') == 'production':
        # Ensure SSL mode is required in production
        query_params = 'sslmode=require'
    else:
        # Disable SSL mode for local development
        query_params = 'sslmode=disable'

    # Reconstruct the URL with updated query parameters
    DATABASE_URL = urlunparse(parsed_url._replace(query=query_params))

    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
