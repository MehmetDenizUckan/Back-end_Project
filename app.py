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
    
    # Initialize FileClass
    FileClass(app, r'C:\Users\UCKAN\Desktop\test')
    
    return app

  
def main():
    atexit.register(cleanup)
    web_app = create_app()
    if __name__ == "__main__":
        web_app.run(debug=True)
    

# Run the app        
main()

