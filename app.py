# -*- coding: utf-8 -*-
from flask import Flask
from routes import Routes
from auth import Authentication
from db import cleanup
import os
import atexit
from file_operations import FileClass




def create_app():
    app = Flask(__name__)
    
    # Configure the app (e.g., app.config.from_object('config.Config'))
    app.config.from_object('config.Config')
    
    # Initialize routes
    Routes(app)
    
    # Initialize authentication
    Authentication(app)
    
    # For local testing, use a relative path or an environment variable
    file_path = r'C:\Users\UCKAN\Desktop\test' if os.getenv('FLASK_ENV') == 'development' else 'path for the bucket'
    print("env = ", os.getenv('FLASK_ENV'))
    FileClass(app, file_path)
    
    return app

  


def local_main():
    atexit.register(cleanup)
    local_app = create_app()
    local_app.run(debug=True)


def server_main():
    atexit.register(cleanup) 
    return create_app() 
    
   
    
if __name__ == "__main__":
    # Determine environment and run accordingly
    if os.getenv('FLASK_ENV') == 'development':
        local_main()
    else:
        server_main()
