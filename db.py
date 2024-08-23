import psycopg2
import logging
from functools import wraps

# Configure the logging
logging.basicConfig(filename='userDB_errors.txt', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

def connect_to_database():
    try:
        conn = psycopg2.connect(
            dbname="user_db",
            user="postgres",
            password="postresql.2024",
            host="localhost",
            port="5432"
        )
        return conn
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None

db_connection = connect_to_database()

class LoginCredentials:
    def __init__(self, db_connection, password, email):
        self.db_connection = db_connection
        self.password = password
        self.email = email

    def authenticate_user(self):
        try:
            with self.db_connection.cursor() as db_cursor:
                query = "SELECT user_password FROM user_info WHERE user_email = %s"
                db_cursor.execute(query, (self.email,))
                result = db_cursor.fetchone()
                print(result, self.password)
                if result and result[0] == self.password:
                    self.db_connection.commit()  # Commit if the authentication is successful
                    return True
                else:
                    self.db_connection.rollback()  # Rollback if authentication fails
                    return False
        except Exception as e:
            error = f"Failed to authenticate user with email {self.email}: {str(e)}"
            logging.error(error)
            self.db_connection.rollback()  # Rollback on exception
            return False    

class MyDatabaseClass(LoginCredentials):
    def __init__(self, db_connection, name, password, email, comments):
        super().__init__(db_connection, password, email)
        self.name = name
        self.comments = comments
        self.img_url = 'test url'

    # Decorator for the methods
    def with_cursor(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            try:
                with self.db_connection.cursor() as db_cursor:
                    return func(self, db_cursor, *args, **kwargs)
            except Exception as e:
                error = f"Error in method {func.__name__} with args {args} and kwargs {kwargs}: {str(e)}"
                logging.error(error)
                self.db_connection.rollback()  # Rollback on exception
                raise
        return wrapper

    @with_cursor
    def register_user(self, db_cursor):
        try:            
            if self.check_if_data_exists(db_cursor, self.email):
                return False     
            else:
                query = """
                    INSERT INTO user_info (user_name, user_password, user_email, img_url, user_comments)
                    VALUES (%s, %s, %s, %s, %s)
                """
                db_cursor.execute(query, (self.name, self.password, self.email, self.img_url, self.comments))
                self.db_connection.commit()
                return True
        except Exception as e:
            error = f"Failed to insert user with email {self.email}: {str(e)}"
            logging.error(error)
            self.db_connection.rollback()  
            return False
        
    def check_if_data_exists(self, db_cursor, email):
        try:
            query = "SELECT user_email FROM user_info WHERE user_email = %s"
            db_cursor.execute(query, (email,))
            result = db_cursor.fetchone() 
            if result is None:
                return False
            else:
                return True         
        except Exception as e:
            error = f"Failed to check if data exists for email {email}: {str(e)}"
            logging.error(error)
            self.db_connection.rollback()  
            return False
