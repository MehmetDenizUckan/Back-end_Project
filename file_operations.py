import os
from flask import Flask, flash, request, redirect, url_for, send_from_directory, render_template, session
from werkzeug.utils import secure_filename
from db import LoginCredentials, MyDatabaseClass, DatabaseConnectionPool

UPLOAD_FOLDER = r'C:\Users\UCKAN\Desktop\test'

class FileClass:
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

    def __init__(self, app, upload_folder) -> None:
        self.app = app
        self.db_pool = DatabaseConnectionPool(minconn=1, maxconn=10)
        self.app.config['UPLOAD_FOLDER'] = upload_folder
        self.file_operations()  # Initialize file operations

    def allowed_file(self, filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in self.ALLOWED_EXTENSIONS
    
    def file_operations(self):         
        @self.app.route('/upload_file', methods=['GET', 'POST'])
        def upload_file():
            if request.method == 'POST':
                # Check if the request has the file part
                if 'file' not in request.files:
                    flash('No file part', 'error')
                    # Retrieve username from session
                    username = session.get('username')
                    return redirect(url_for('userpage'))
                
                file = request.files['file']
                
                # Check if the file has no name
                if file.filename == '':
                    flash('No selected file', 'error')
                    # Retrieve username from session
                    username = session.get('username')
                    return redirect(url_for('userpage'))
                
                if file and self.allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(self.app.config['UPLOAD_FOLDER'], filename))
                    flash('File successfully uploaded', 'success')
                    
                    # Generate the image URL
                    image_url = request.url_root + url_for('uploaded_file', filename=filename).lstrip('/')
  
                    # Retrieve email from session
                    user_email = session.get('user_email')
                    
                    if not user_email:
                        flash('User not logged in', 'error')
                        return redirect(url_for('login')) 
                    
                    user_db = MyDatabaseClass(self.db_pool, name=None, password=None, email=user_email, comments=None)
                    
                    success = user_db.save_img_url_to_db(image_url)
                    
                    if not success:
                        flash('Failed to save image URL to the database', 'error')
                        
                    # Retrieve username from session
                    username = session.get('username')
                    
                    print(username)
                       
                    # Pass the image URL to the template
                    return render_template('userpage.html', filename=filename, image_url=image_url, username = username)

                   
                flash('Invalid file type', 'error')
                return redirect(url_for('userpage'))

        @self.app.route('/uploads/<filename>')
        def uploaded_file(filename):
            return send_from_directory(self.app.config['UPLOAD_FOLDER'], filename)

            
        