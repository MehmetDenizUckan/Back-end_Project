import psycopg2
import logging
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from psycopg2 import pool

# Configure the logging
logging.basicConfig(filename='userDB_errors.txt', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

db_pool = None
# Create a db connection pool 
class DatabaseConnectionPool:
    def __init__(self, minconn, maxconn):
        global db_pool
        self.pool = psycopg2.pool.SimpleConnectionPool(minconn, maxconn,
                                                       dbname="user_db",
                                                       user="postgres",
                                                       password="postresql.2024",
                                                       host="localhost",
                                                       port="5432")

    def get_conn(self):
        return self.pool.getconn()

    def put_conn(self, conn):
        self.pool.putconn(conn)

    def close_all(self):
        self.pool.closeall()


class LoginCredentials:
    def __init__(self, db_pool ,email, password):
        self.email = email
        self.db_pool = db_pool
        self.password = generate_password_hash(password, "scrypt")  # Hash the password before storing

    def authenticate_user(self, text_password):
        conn = self.db_pool.get_conn()  # Get a connection from the pool
        try:
            with conn.cursor() as db_cursor:
                query = "SELECT user_password FROM user_info WHERE user_email = %s"
                db_cursor.execute(query, (self.email,))
                result = db_cursor.fetchone()

                if result and check_password_hash(result[0], text_password):  # Compare with the stored hash
                    conn.commit()  # Commit if the authentication is successful
                    return True
                else:
                    conn.rollback()  # Rollback if authentication fails
                    return False
        except Exception as e:
            error = f"Failed to authenticate user with email {self.email}: {str(e)}"
            logging.error(error)
            conn.rollback()  # Rollback on exception
            return False
        finally:
            self.db_pool.put_conn(conn)  # Return the connection to the pool

class MyDatabaseClass(LoginCredentials):
    def __init__(self, db_pool, name, password, email, comments):
        super().__init__(db_pool, email, password)
        self.name = name
        self.comments = comments
        self.img_url = 'test url'

    # Decorator for the methods
    def with_cursor(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            conn = self.db_pool.get_conn()  # Get a connection from the pool
            try:
                with conn.cursor() as db_cursor:
                    return func(self, db_cursor, *args, **kwargs)
            except Exception as e:
                error = f"Error in method {func.__name__} with args {args} and kwargs {kwargs}: {str(e)}"
                logging.error(error)
                conn.rollback()  # Rollback on exception
                raise
            finally:
                self.db_pool.put_conn(conn)  # Return the connection to the pool
        return wrapper

    @with_cursor
    def register_user(self, db_cursor):
        try:
            if self.check_if_data_exists(self.email):
                return False
            else:
                query = """
                    INSERT INTO user_info (user_name, user_password, user_email, img_url, user_comments)
                    VALUES (%s, %s, %s, %s, %s)
                """
                db_cursor.execute(query, (self.name, self.password, self.email, self.img_url, self.comments))
                db_cursor.connection.commit()  # Commit the transaction
                return True
        except Exception as e:
            error = f"Failed to insert user with email {self.email}: {str(e)}"
            logging.error(error)
            db_cursor.connection.rollback()  # Rollback on exception
            return False
        
    @with_cursor
    def check_if_data_exists(self, db_cursor, email):
        try:
            query = "SELECT user_email FROM user_info WHERE user_email = %s"
            db_cursor.execute(query, (email,))
            result = db_cursor.fetchone()
            return result is not None
        except Exception as e:
            error = f"Failed to check if data exists for email {email}: {str(e)}"
            logging.error(error)
            db_cursor.connection.rollback()  # Rollback on exception
            return False

        
        

# Close all the db connections to release back the memory space
def cleanup():
    global db_pool
    if db_pool:
        db_pool.close_all()
        print("Closed all connections")