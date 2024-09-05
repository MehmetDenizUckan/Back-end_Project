from flask import Flask, render_template, request, redirect, url_for, flash, session
from db import LoginCredentials, MyDatabaseClass, DatabaseConnectionPool

class Authentication:
    def __init__(self, app):
        self.app = app
        self.db_pool = DatabaseConnectionPool(minconn=1 , maxconn=10)  # Create the database connection
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
                
                db_class = LoginCredentials(db_pool=self.db_pool, password=password, email=email)
                user_db = MyDatabaseClass(self.db_pool, name=None, password=None, email=email, comments=None)
                if db_class.authenticate_user(password):
                    flash('You have successfully logged in!', 'success')
                    session['user_email'] = email  # Store email in session
                    username = user_db.get_user_name()                
                    session['username'] = username  # Store username in session
                    
                    
                    return redirect(url_for('userpage'))  # Redirect to home page
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
                
                             
                db_class = MyDatabaseClass(db_pool=self.db_pool, name=name, password=password, email=email, comments=comments)      
                if db_class.register_user() :
                    flash('You have successfully registered!', 'success')
                    session['user_email'] = email
                    return redirect(url_for('login'))  # Redirect to login page
                else:
                    flash('Email already exists.', 'error')
                    return redirect(url_for('signup'))

                        
            return render_template('sign-up.html')
