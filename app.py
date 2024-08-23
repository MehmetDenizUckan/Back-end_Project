# -*- coding: utf-8 -*-
from flask import Flask
from routes import Routes
from auth import Authentication
from dotenv import load_dotenv
import os

# load .env file
load_dotenv()

def create_app():
    app = Flask(__name__)
    
    # Configure the app (e.g., app.config.from_object('config.Config'))
    app.config.from_object('config.Config')
    
    # Initialize routes
    Routes(app)
    
    # Initialize authentication
    Authentication(app)
    
    return app

def main():
    web_app = create_app()
    if __name__ == "__main__":
        web_app.run(debug=True)

# Run the app        
main()

