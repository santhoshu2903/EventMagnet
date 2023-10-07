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
        self.createEventRegistrationTable()
        self.createEventCommentTable()




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

    def createEventRegistrationTable(self):
        with sqlite3.connect("eventRegistration.db") as db:
            cursor = db.cursor()
            cursor.execute("""CREATE TABLE IF NOT EXISTS eventRegistration(
                eventRegistrationID integer PRIMARY KEY AUTOINCREMENT,
                eventID integer NOT NULL,
                userID integer NOT NULL,
                FOREIGN KEY(eventID) REFERENCES event(eventID),
                FOREIGN KEY(userID) REFERENCES user(userID));""")
            db.commit()

    def createEventCommentTable(self):
        with sqlite3.connect("eventComment.db") as db:
            cursor = db.cursor()
            cursor.execute("""CREATE TABLE IF NOT EXISTS eventComment(
                eventCommentID integer PRIMARY KEY AUTOINCREMENT,
                eventID integer NOT NULL,
                userID integer NOT NULL,
                comment text NOT NULL,
                FOREIGN KEY(eventID) REFERENCES event(eventID),
                FOREIGN KEY(userID) REFERENCES user(userID));""")
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
        self.label = tkinter.Label(self.tkn, text="Login Page", font=("Helvetica", 20))
        self.label.pack(pady=20)

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
        self.login_button = tkinter.Button(self.tkn, text="Login",command=self.loginUser)
        self.login_button.pack(pady=20)

        # Register button
        self.register_button = tkinter.Button(self.tkn, text="Register", command=self.registerUser)
        self.register_button.pack(pady=10)

        # Back button to return to the welcome page
        self.back_button = tkinter.Button(self.tkn, text="Back to Welcome", command=self.show_welcome_page)
        self.back_button.pack(pady=10)

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

    def show_admin_event_page(self):
        self.tkn.geometry("800x500")
        for widget in self.tkn.winfo_children():
            widget.destroy()

        # Add event form elements
        label = tkinter.Label(self.tkn, text="Admin Event Page", font=("Helvetica", 20))
        label.pack(pady=20)

        # Event Name entry
        self.event_name_label = tkinter.Label(self.tkn, text="Event Name:")
        self.event_name_label.pack()
        self.event_name_entry = tkinter.Entry(self.tkn)
        self.event_name_entry.pack()

        # Event Date entry
        self.event_date_label = tkinter.Label(self.tkn, text="Event Date:")
        self.event_date_label.pack()
        self.event_date_entry = tkinter.Entry(self.tkn)
        self.event_date_entry.pack()

        # Event Time entry
        self.event_time_label = tkinter.Label(self.tkn, text="Event Time:")
        self.event_time_label.pack()
        self.event_time_entry = tkinter.Entry(self.tkn)
        self.event_time_entry.pack()

        # Event Location entry
        self.event_location_label = tkinter.Label(self.tkn, text="Event Location:")
        self.event_location_label.pack()
        self.event_location_entry = tkinter.Entry(self.tkn)
        self.event_location_entry.pack()

        # Event Description entry
        self.event_description_label = tkinter.Label(self.tkn, text="Event Description:")
        self.event_description_label.pack()
        self.event_description_entry = tkinter.Entry(self.tkn)
        self.event_description_entry.pack()

        # Register button
        self.register_button = tkinter.Button(self.tkn, text="Register", command=self.registerEvent)
        self.register_button.pack(pady=20)

        # Back button to return to the welcome page
        self.back_button = tkinter.Button(self.tkn, text="Back to Welcome", command=self.show_welcome_page)
        self.back_button.pack(pady=10)



    def user_dashboard(self):
        self.tkn.geometry("800x500")
        for widget in self.tkn.winfo_children():
            widget.destroy()

        # Add user dashboard elements
        label = tkinter.Label(self.tkn, text="User Dashboard", font=("Helvetica", 20))
        label.pack(pady=20)

        # Add buttons to navigate to different views
        event_button = tkinter.Button(self.tkn, text="Register for Event", command=self.show_user_event_page)
        my_events_button = tkinter.Button(self.tkn, text="My Events", command=self.show_my_events_page)
        logout_button = tkinter.Button(self.tkn, text="Logout", command=self.show_welcome_page)
       

        event_button.pack(pady=20)
        my_events_button.pack(pady=10)
        logout_button.pack(pady=10)

    def show_user_event_page(self):
        self.tkn.geometry("800x500")
        for widget in self.tkn.winfo_children():
            widget.destroy()

        # Add user event page elements
        label = ttk.Label(self.tkn, text="User Event Page", font=("Helvetica", 20))
        label.pack(pady=20)

        # Search box
        search_label = ttk.Label(self.tkn, text="Search Events:")
        search_label.pack()
        self.search_entry = ttk.Entry(self.tkn)
        self.search_entry.pack()
        search_button = ttk.Button(self.tkn, text="Search", command=self.search_events)
        search_button.pack()

        # Create a Treeview widget to display events
        self.event_tree = ttk.Treeview(self.tkn, columns=("Event Name", "Event Date", "Event Time", "Event Location", "Event Description"))
        self.event_tree.heading("#1", text="Event Name")
        self.event_tree.heading("#2", text="Event Date")
        self.event_tree.heading("#3", text="Event Time")
        self.event_tree.heading("#4", text="Event Location")
        self.event_tree.heading("#5", text="Event Description")

        # Connect to the 'events.db' database and retrieve event data
        with sqlite3.connect("event.db") as db:
            cursor = db.cursor()
            cursor.execute("SELECT * FROM event")
            events = cursor.fetchall()

        # Populate the Treeview with event data
        for event in events:
            self.event_tree.insert("", "end", values=event)

        self.event_tree.pack()

        # Register button to register for selected event
        register_button = ttk.Button(self.tkn, text="Register for Event", command=self.register_for_event)
        register_button.pack(pady=10)

        user_dashboard_button = ttk.Button(self.tkn, text="My Dashboard", command=self.user_dashboard)
        user_dashboard_button.pack(pady=10)

        # Back button to return to the main page
        back_button = ttk.Button(self.tkn, text="Logout", command=self.show_main_page)
        back_button.pack(pady=10)

    def show_my_events_page(self):
        self.tkn.geometry("800x500")
        for widget in self.tkn.winfo_children():
            widget.destroy()

        # Add my events page elements
        label = ttk.Label(self.tkn, text="My Events", font=("Helvetica", 20))
        label.pack(pady=20)

        # Create a Treeview widget to display events
        event_tree = ttk.Treeview(self.tkn, columns=("Event Name", "Event Date", "Event Time", "Event Location", "Event Description"))
        event_tree.heading("#1", text="Event Name")
        event_tree.heading("#2", text="Event Date")
        event_tree.heading("#3", text="Event Time")
        event_tree.heading("#4", text="Event Location")
        event_tree.heading("#5", text="Event Description")

        # Get the user's email (you should have a way to fetch the user's email after login)
        user_email = self.current_user  # Replace with the actual user's email

        # Connect to the 'eventRegistration.db' database
        with sqlite3.connect("eventRegistration.db") as registration_db:
            cursor = registration_db.cursor()

            # Connect to the 'user.db' database to retrieve user-related information
            with sqlite3.connect("user.db") as user_db:
                user_cursor = user_db.cursor()

                # Query the user table in 'user.db' to get the userID based on email
                user_cursor.execute("SELECT userID FROM user WHERE email=?", (user_email,))
                user_id = user_cursor.fetchone()

                if user_id:
                    # Query the eventRegistration table in 'eventRegistration.db' to get eventIDs associated with the user
                    cursor.execute("SELECT eventID FROM eventRegistration WHERE userID=?", (user_id[0],))
                    event_ids = cursor.fetchall()
                else:
                    event_ids = []

        # Connect to the 'event.db' database
        with sqlite3.connect("event.db") as event_db:
            cursor = event_db.cursor()

            # Retrieve event data for the user's registered events
            events = []
            for event_id in event_ids:
                cursor.execute("SELECT * FROM event WHERE eventID=?", event_id)
                event_data = cursor.fetchone()
                events.append(event_data)

        # Populate the Treeview with events registered by the user
        for event in events:
            event_tree.insert("", "end", values=event)

        event_tree.pack()

        # Back button to return to the main page
        back_button = ttk.Button(self.tkn, text="My Dashboard", command=self.user_dashboard)
        back_button.pack(pady=10)




    



#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def register_for_event(self):
    # Get the selected event
        selected_event = self.event_tree.focus()

        # Validate that an event was selected
        if selected_event == "":
            messagebox.showerror("Error", "Please select an event")
        else:
            # Get the event's data
            event_data = self.event_tree.item(selected_event, "values")

            # Get the user's email (you should have a way to fetch the user's email after login)
            user_email = self.current_user  # Replace with the actual user's email
            # Connect to the 'user.db' database to retrieve the user's ID based on email
            with sqlite3.connect("user.db") as user_db:
                cursor = user_db.cursor()
                cursor.execute("SELECT userID FROM user WHERE email=?", (user_email,))
                user_id = cursor.fetchone()

                if user_id:
                    # Check if the user has already registered for this event
                    with sqlite3.connect("eventRegistration.db") as registration_db:
                        cursor = registration_db.cursor()
                        cursor.execute("SELECT * FROM eventRegistration WHERE eventID=? AND userID=?", (event_data[0], user_id[0]))
                        existing_registration = cursor.fetchone()

                    if existing_registration:
                        messagebox.showinfo("Info", "You have already registered for this event.")
                    else:
                        # Connect to the 'eventRegistration.db' database and insert the event's data
                        with sqlite3.connect("eventRegistration.db") as registration_db:
                            cursor = registration_db.cursor()
                            cursor.execute("""INSERT INTO eventRegistration(eventID, userID)
                            VALUES(?,?)""", (event_data[0], user_id[0]))
                            registration_db.commit()
                        messagebox.showinfo("Success", "You have registered for the event successfully!")
                        self.user_dashboard()
                else:
                    messagebox.showerror("Error", "User not found")



    def search_events(self):
        # Get the user's input
        search = self.search_entry.get()

        # Validate the user's input
        if search == "":
            messagebox.showerror("Error", "Please enter a search term")
        else:
            # Connect to the 'events.db' database and retrieve event data
            with sqlite3.connect("events.db") as db:
                cursor = db.cursor()
                cursor.execute("SELECT * FROM event WHERE eventName LIKE ?", (search,))
                events = cursor.fetchall()

            # Populate the Treeview with event data
            for event in events:
                self.event_tree.insert("", "end", values=event)


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

        self.current_user = email

        # Validate the user's input
        if email == "" or password == "":
            messagebox.showerror("Error", "Please fill in all fields")
        else:
            # Check if the user's input matches the database
            with sqlite3.connect("user.db") as db:
                cursor = db.cursor()
                cursor.execute("SELECT * FROM user WHERE email=? AND password=?", (email, password))
                user = cursor.fetchone()
                if user is not None:
                    messagebox.showinfo("Success", "You have logged in successfully!")
                    if email == "admin":
                        self.show_admin_event_page()
                    else:
                        self.user_dashboard()
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
        
    

#-----------------------------------------------------------------------------------------------------------------------





if __name__ == "__main__":
    app = EventHub()
    app.tkn.mainloop()