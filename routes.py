# -*- coding: utf-8 -*-
from flask import Flask, render_template, redirect, url_for, request, session
from db import DatabaseConnectionPool, MyDatabaseClass

class Routes:
    def __init__(self, app) -> None:
        # Initialize the app to be used on routes
        self.app = app   
        self.db_pool = DatabaseConnectionPool(minconn=1, maxconn=10)
        # Register routes
        self.implement_routes()
        
        # Handle errors if encountered
        self.register_error_handlers()
    
    def implement_routes(self):
        @self.app.route('/article-details')
        def article_details():
            return render_template('article-details.html')
        
        @self.app.route('/about')
        def about():
            return render_template('about.html')

        @self.app.route('/privacy')
        def privacy_policy():
            return render_template('privacy-policy.html')
        
        @self.app.route('/halilbayraktar')
        def hb():
            return render_template('halilbayraktar.html')
        
        @self.app.route('/index')
        def index():
            return render_template('index.html')
        
        @self.app.route('/terms')
        def termsNconditions():
            return render_template('terms-conditions.html')
        
        @self.app.route('/signup1', methods=['GET'])
        def signup1():
            return render_template('sign-up.html')

        @self.app.route('/login1', methods=['GET'])
        def login1():
            return render_template('log-in.html')
        
        @self.app.route('/userpage')
        def userpage():     
            # Retrieve username and email from session
            username = session.get('username')
            email = session.get('user_email')
            
            
            # Redirect to login page if not logged in
            if not username or not email:
                return redirect(url_for('login1'))
            
            filename = request.args.get('filename')
            img_url = self.check_img_url_exist(email)
                     
            return render_template('userpage.html', filename=filename, username=username, image_url=img_url)


        
    def register_error_handlers(self):
        @self.app.errorhandler(404)
        def page_not_found(error):
            return render_template('404.html'), 404
        
        @self.app.errorhandler(500)
        def internal_server_error(error):
            return render_template('500.html'), 500

    def check_img_url_exist(self, email):
        if not email:
            return None  # Return None if email is not present
        
        user_db = MyDatabaseClass(self.db_pool, name=None, password=None, email=email, comments=None)
        img_url = user_db.get_img_url()
        return img_url if img_url else None
