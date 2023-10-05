import tkinter
from tkinter import messagebox
import tkinter.ttk as ttk
import sqlite3




class EventHub():
    def __init__(self):
        super().__init__()
        self.tkn = tkinter.Tk()
        self.tkn.title("Event Hub")
        self.tkn.geometry("800x500")
        self.show_welcome_page()

        # Create the database tables
        self.createUserTable()
        self.createEventTable()



    def createUserTable(self):
        with sqlite3.connect("user.db") as db:
            cursor = db.cursor()
            cursor.execute("""CREATE TABLE IF NOT EXISTS user(
                userID integer PRIMARY KEY AUTOINCREMENT,
                firstName text NOT NULL,
                lastName text NOT NULL,
                email text NOT NULL,
                password text NOT NULL);""")
            db.commit()

    def createEventTable(self):
        with sqlite3.connect("event.db") as db:
            cursor = db.cursor()
            cursor.execute("""CREATE TABLE IF NOT EXISTS event(
                eventID integer PRIMARY KEY AUTOINCREMENT,
                eventName text NOT NULL,
                eventDate text NOT NULL,
                eventTime text NOT NULL,
                eventLocation text NOT NULL,
                eventDescription text NOT NULL);""")
            db.commit()

    def show_welcome_page(self):
        self.tkn.geometry("800x500")
        for widget in self.tkn.winfo_children():
            widget.destroy()

        label = tkinter.Label(self.tkn, text="Welcome to Event Hub", font=("Helvetica", 20))
        label.pack(pady=20)

        info_label = tkinter.Label(self.tkn, text="Discover and attend exciting events in your area.",font=("Helvetica", 15, "italic", "bold"))
        info_label.pack()

        main_page_button = tkinter.Button(self.tkn, text="Main Page", command=self.show_main_page)
        main_page_button.pack(pady=20)

    def show_main_page(self):
        self.tkn.geometry("500x500")
        for widget in self.tkn.winfo_children():
            widget.destroy()

        label = tkinter.Label(self.tkn, text="Main Page", font=("Helvetica", 20))
        label.pack(pady=20)

        # Add buttons to navigate to different views
        welcome_button = tkinter.Button(self.tkn, text="Welcome Page", command=self.show_welcome_page)
        login_button = tkinter.Button(self.tkn, text="Login Page", command=self.show_login_page)
        register_button = tkinter.Button(self.tkn, text="Register Page", command=self.show_register_page)

        welcome_button.pack(pady=20)
        login_button.pack(pady=10)
        register_button.pack(pady=10)


    def show_login_page(self):
        self.tkn.geometry("500x500")
        for widget in self.tkn.winfo_children():
            widget.destroy()

        # Add login form elements
        label = tkinter.Label(self.tkn, text="Login Page", font=("Helvetica", 20))
        label.pack(pady=20)

        # Email (Gmail ID) entry
        email_label = tkinter.Label(self.tkn, text="Email (Gmail ID):")
        email_label.pack()
        email_entry = tkinter.Entry(self.tkn)
        email_entry.pack()

        # Password entry
        password_label = tkinter.Label(self.tkn, text="Password:")
        password_label.pack()
        password_entry = tkinter.Entry(self.tkn)
        password_entry.pack()

        # Login button
        login_button = tkinter.Button(self.tkn, text="Login",command=self.show_login_page)
        login_button.pack(pady=20)

        # Register button
        register_button = tkinter.Button(self.tkn, text="Register", command=self.show_register_page)
        register_button.pack(pady=10)

        # Back button to return to the welcome page
        back_button = tkinter.Button(self.tkn, text="Back to Welcome", command=self.show_welcome_page)
        back_button.pack(pady=10)

    def show_login_page(self):
        self.tkn.geometry("500x500")
        for widget in self.tkn.winfo_children():
            widget.destroy()

        # Add login form elements
        label = tkinter.Label(self.tkn, text="Login Page", font=("Helvetica", 20))
        label.pack(pady=20)

        # Email (Gmail ID) entry
        self.email_label = tkinter.Label(self.tkn, text="Email (Gmail ID):")
        self.email_label.pack()
        self.email_entry = tkinter.Entry(self.tkn)
        self.email_entry.pack()


        # Password entry
        self.password_label = tkinter.Label(self.tkn, text="Password:")
        self.password_label.pack()
        self.password_entry = tkinter.Entry(self.tkn)
        self.password_entry.pack()






        # Login button
        self.login_button = tkinter.Button(self.tkn, text="Login", command=self.loginUser)
        self.login_button.pack(pady=20)

        # Register button
        self.register_button = tkinter.Button(self.tkn, text="Register", command=self.show_register_page)
        self.register_button.pack(pady=10)

        # Back button to return to the welcome page
        self.back_button=tkinter.Button(self.tkn, text="Back to Welcome", command=self.show_welcome_page)
        self.back_button.pack(pady=10)

    def show_register_page(self):
        self.tkn.geometry("500x500")
        for widget in self.tkn.winfo_children():
            widget.destroy()

        # Add registration form elements
        label = tkinter.Label(self.tkn, text="Register Page", font=("Helvetica", 20))
        label.pack(pady=20)

        # First Name entry
        self.first_name_label = tkinter.Label(self.tkn, text="First Name:")
        self.first_name_label.pack()
        self.first_name_entry = tkinter.Entry(self.tkn)
        self.first_name_entry.pack()

        # Last Name entry
        self.last_name_label = tkinter.Label(self.tkn, text="Last Name:")
        self.last_name_label.pack()
        self.last_name_entry = tkinter.Entry(self.tkn)
        self.last_name_entry.pack()


        # Email (Gmail ID) entry
        self.email_entry = tkinter.Label(self.tkn,text="Email (Gmail ID):")
        self.email_entry.pack()
        self.email_entry = tkinter.Entry(self.tkn)
        self.email_entry.pack()

        # Password entry
        self.password_label = tkinter.Label(self.tkn, text="Password:")
        self.password_label.pack()
        self.password_entry = tkinter.Entry(self.tkn)
        self.password_entry.pack()

        # Register button
        self.register_button = tkinter.Button(self.tkn, text="Register", command=self.registerUser)
        self.register_button.pack(pady=20)


        # Back button to return to the welcome page
        self.back_button = tkinter.Button(self.tkn, text="Back to Welcome", command=self.show_welcome_page)
        self.back_button.pack(pady=10)

    # def show_event_page(self):


    def registerUser(self):
        # Get the user's input
        firstName = self.first_name_entry.get()
        lastName = self.last_name_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()

        # Validate the user's input
        if firstName == "" or lastName == "" or email == "" or password == "":
            messagebox.showerror("Error", "Please fill in all fields")
        else:
            # Insert the user's input into the database
            with sqlite3.connect("user.db") as db:
                cursor = db.cursor()
                cursor.execute("""INSERT INTO user(firstName, lastName, email, password)
                VALUES(?,?,?,?)""", (firstName, lastName, email, password))
                db.commit()
            messagebox.showinfo("Success", "You have registered successfully!")
            self.show_login_page()

    def loginUser(self):
        # Get the user's input
        email = self.email_entry.get()
        password = self.password_entry.get()

        # Validate the user's input
        if email == "" or password == "":
            messagebox.showerror("Error", "Please fill in all fields")
        else:
            # Check if the user's input matches the database
            with sqlite3.connect("user.db") as db:
                cursor = db.cursor()
                cursor.execute("SELECT * FROM user WHERE email=? AND password=?", (email, password))
                user = cursor.fetchone()
                if user:
                    messagebox.showinfo("Success", "You have logged in successfully!")
                    self.show_event_page()
                else:
                    messagebox.showerror("Error", "Invalid email or password")

    def registerEvent(self):
        # Get the user's input
        eventName = self.event_name_entry.get()
        eventDate = self.event_date_entry.get()
        eventTime = self.event_time_entry.get()
        eventLocation = self.event_location_entry.get()
        eventDescription = self.event_description_entry.get()

        # Validate the user's input
        if eventName == "" or eventDate == "" or eventTime == "" or eventLocation == "" or eventDescription == "":
            messagebox.showerror("Error", "Please fill in all fields")
        else:
            # Insert the user's input into the database
            with sqlite3.connect("event.db") as db:
                cursor = db.cursor()
                cursor.execute("""INSERT INTO event(eventName, eventDate, eventTime, eventLocation, eventDescription)
                VALUES(?,?,?,?,?)""", (eventName, eventDate, eventTime, eventLocation, eventDescription))
                db.commit()
            messagebox.showinfo("Success", "You have registered successfully!")
            self.show_event_page()
        
    def show_event_page(self):
        self.tkn.geometry("500x500")
        for widget in self.tkn.winfo_children():
            widget.destroy()

        # Add registration form elements
        label = tkinter.Label(self.tkn, text="Event Page", font=("Helvetica", 20))
        label.pack(pady=20)

        # Event Name entry
        event_name_label = tkinter.Label(self.tkn, text="Event Name:")
        event_name_label.pack()
        event_name_entry = tkinter.Entry(self.tkn)
        event_name_entry.pack()

        # Event Date entry
        event_date_label = tkinter.Label(self.tkn, text="Event Date:")
        event_date_label.pack()
        event_date_entry = tkinter.Entry(self.tkn)
        event_date_entry.pack()

        # Event Time entry
        event_time_label = tkinter.Label(self.tkn, text="Event Time:")
        event_time_label.pack()
        event_time_entry = tkinter.Entry(self.tkn)
        event_time_entry.pack()

        # Event Location entry
        event_location_label = tkinter.Label(self.tkn, text="Event Location:")
        event_location_label.pack()
        event_location_entry = tkinter.Entry(self.tkn)
        event_location_entry.pack()

        # Event Description entry
        event_description_label = tkinter.Label(self.tkn, text="Event Description:")
        event_description_label.pack()
        event_description_entry = tkinter.Entry(self.tkn)
        event_description_entry.pack()

        # Register button
        register_button = tkinter.Button(self.tkn, text="Register", command=self.registerEvent)
        register_button.pack(pady=20)

        # Back button to return to the welcome page
        back_button = tkinter.Button(self.tkn, text="Back to Welcome", command=self.show_welcome_page)
        back_button.pack(pady=10)

    def registerEvent(self):
        # Get the user's input
        eventName = self.event_name_entry.get()
        eventDate = self.event_date_entry.get()
        eventTime = self.event_time_entry.get()
        eventLocation = self.event_location_entry.get()
        eventDescription = self.event_description_entry.get()

        # Validate the user's input
        if eventName == "" or eventDate == "" or eventTime == "" or eventLocation == "" or eventDescription == "":
            messagebox.showerror("Error", "Please fill in all fields")
        else:
            # Insert the user's input into the database
            with sqlite3.connect("event.db") as db:
                cursor = db.cursor()
                cursor.execute("""INSERT INTO event(eventName, eventDate, eventTime, eventLocation, eventDescription)
                VALUES(?,?,?,?,?)""", (eventName, eventDate, eventTime, eventLocation, eventDescription))
                db.commit()
            messagebox.showinfo("Success", "You have registered successfully!")
            self.show_event_page()
#-----------------------------------------------------------------------------------------------------------------------





if __name__ == "__main__":
    app = EventHub()
    app.tkn.mainloop()