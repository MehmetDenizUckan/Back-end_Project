# -*- coding: utf-8 -*-
from flask import Flask, render_template, redirect, url_for

class Routes:
    def __init__(self, app) -> None:
        # Initialise the app to be used on routes
        self.app = app
        
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
        
        @self.app.route('/signup1', methods=['GET'])
        def signup1():
            return render_template('sign-up.html')

        @self.app.route('/login1', methods=['GET'])
        def login1():
            return render_template('log-in.html')
        
    def register_error_handlers(self):
        @self.app.errorhandler(404)
        def page_not_found(error):
            return render_template('404.html'), 404
        
        @self.app.errorhandler(500)
        def internal_server_error(error):
            return render_template('500.html'), 500
