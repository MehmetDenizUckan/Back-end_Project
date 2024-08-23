from flask import Flask, render_template, request, redirect, url_for, flash
from db import LoginCredentials, MyDatabaseClass, connect_to_database

class Authentication:
    def __init__(self, app):
        self.app = app
        self.db_connection = connect_to_database()  # Create the database connection
        self.setup_routes()

    def setup_routes(self):
        @self.app.route('/login', methods=['GET', 'POST'])
        def login():
            if request.method == 'POST':
                email = request.form.get("email")
                password = request.form.get("password")
                
                if not (email and password):
                    flash('Please fill out all fields.', 'error')
                    return redirect(url_for('login'))
                
                db_class = LoginCredentials(self.db_connection, password=password, email=email)
                if db_class.authenticate_user():
                    flash('You have successfully logged in!', 'success')
                    return redirect(url_for('index'))  # Redirect to home page
                else:
                    flash('Invalid email or password.', 'error')
                    return redirect(url_for('login'))
            
            return render_template('log-in.html')
        
        @self.app.route('/sign-up', methods=['GET', 'POST'])
        def signup():
            if request.method == 'POST':
                name = request.form.get("name")
                email = request.form.get("email")
                password = request.form.get("password")
                comments = request.form.get("comments")
                
                if not (name and password and email):
                    flash('Please fill out all fields.', 'error')
                    return redirect(url_for('signup'))
                
                db_class = MyDatabaseClass(self.db_connection, name=name, password=password, email=email, comments=comments)      
                if db_class.register_user() :
                    flash('You have successfully registered!', 'success')
                    return redirect(url_for('login'))  # Redirect to login page
                else:
                    flash('Email already exists.', 'error')
                    return redirect(url_for('signup'))
            
            return render_template('sign-up.html')
