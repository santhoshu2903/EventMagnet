import sqlite3
import os 

file_path=os.path.join(os.getcwd(),"model")
Event_db_path=os.path.join(file_path,"event_db.db")
User_db_path = os.path.join(file_path,"user_db.db")

print(Event_db_path)
print(User_db_path)

class Model:
    def __init__(self, event_db_path=Event_db_path, user_db_path=User_db_path):
        self.event_db_path= event_db_path
        self.user_db_path=user_db_path

        self.init_event_db()
        self.init_user_db()

    def init_event_db(self):
        with sqlite3.connect(self.event_db_path) as conn:
            cursor = conn.cursor()

            # Create the events table if it doesn't exist
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS events (
                    event_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    event_name TEXT NOT NULL,
                    event_description TEXT,
                    event_date DATE,
                    event_time TIME,
                    event_organizer TEXT,
                    event_location TEXT
                );
            ''')

    def init_user_db(self):
        with sqlite3.connect(self.user_db_path) as conn:
            cursor = conn.cursor()

            # Create the users table if it doesn't exist
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_firstname TEXT NOT NULL,
                    user_lastname TEXT NOT NULL,
                    user_mailId TEXT,
                    user_phonenumber TEXT,
                    user_dateofbirth DATE
                );
            ''')


    def registerUser(self,firstName,lastName,gmail,phoneNumber,dob):

        with sqlite3.connect(self.user_db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO users (user_firstname,user_lastname,user_gmailId,
                           user_phonenumber,user_dateofbirth)
                VALUES(?,?,?,?,?)
                ''',(firstName,lastName,gmail,phoneNumber,dob))
            conn.commit()


