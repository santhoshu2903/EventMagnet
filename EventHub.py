import tkinter
from tkinter import messagebox
import tkinter.ttk as ttk
from PIL import ImageTk, Image
import mysql.connector as mysql
import random
import smtplib
from tkcalendar import Calendar, DateEntry

class EventHub():
    def __init__(self):
        super().__init__()
        self.tkn = tkinter.Tk()
        self.tkn.title("Event Hub")
        self.tkn.geometry("800x500")
        self.show_welcome_page()


        database = {
            'user': 'root',
            'password': 'root',
            'host': 'localhost',
            'port': 3306,
            'database': 'eventhub'
        }


        self.database= mysql.connect(**database)
        self.cursor = self.database.cursor()

        # Create the database tables
        self.createUserTable()
        self.createEventTable()
        self.createEventRegistrationTable()
        self.createEventCommentTable()

    def createUserTable(self):
        # SQL statement for creating the 'user' table
        create_user_table = """
        CREATE TABLE IF NOT EXISTS user (
            userID INT AUTO_INCREMENT PRIMARY KEY,
            firstName VARCHAR(255) NOT NULL,
            lastName VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            password VARCHAR(255) NOT NULL
        );
        """
        self.cursor.execute(create_user_table)
        self.database.commit()

    def createEventTable(self):
        # SQL statement for creating the 'event' table
        create_event_table = """
        CREATE TABLE IF NOT EXISTS event (
            eventID INT AUTO_INCREMENT PRIMARY KEY,
            eventName VARCHAR(255) NOT NULL,
            eventDate VARCHAR(255) NOT NULL,
            eventTime VARCHAR(255) NOT NULL,
            eventLocation VARCHAR(255) NOT NULL,
            eventDescription TEXT NOT NULL
        );
        """
        self.cursor.execute(create_event_table)
        self.database.commit()

    def createEventRegistrationTable(self):
        # SQL statement for creating the 'eventRegistration' table
        create_event_registration_table = """
        CREATE TABLE IF NOT EXISTS eventRegistration (
            eventRegistrationID INT AUTO_INCREMENT PRIMARY KEY,
            eventID INT NOT NULL,
            userID INT NOT NULL,
            FOREIGN KEY (eventID) REFERENCES event (eventID),
            FOREIGN KEY (userID) REFERENCES user (userID)
        );
        """
        self.cursor.execute(create_event_registration_table)
        self.database.commit()

    def createEventCommentTable(self):
        # SQL statement for creating the 'eventComment' table
        create_event_comment_table = """
        CREATE TABLE IF NOT EXISTS eventComment (
            eventCommentID INT AUTO_INCREMENT PRIMARY KEY,
            eventID INT NOT NULL,
            userID INT NOT NULL,
            comment TEXT NOT NULL,
            FOREIGN KEY (eventID) REFERENCES event (eventID),
            FOREIGN KEY (userID) REFERENCES user (userID)
        );
        """
        self.cursor.execute(create_event_comment_table)

        # Commit the changes to the database
        self.database.commit()

    def __del__(self):
        # Close the database connection
        self.cursor.close()
        self.database.close()


    def configure_button(self, button):
        #curver border
        button.configure(bg="#0078d4", fg="white", font=("Verdana", 12), relief="raised")
        #button rounded border
        button.configure(borderwidth=3, highlightthickness=3, width=20, height=1)




    def configure_entry(self, entry_widget):
        entry_widget.config(
            font=("Arial", 12),  # Font and font size
            bd=2,  # Border width
            relief="ridge",  # Border style
            fg="black",  # Text color
            bg="white",  # Background color
            selectbackground="lightblue",  # Background color when selected
            selectforeground="black",  # Text color when selected
            insertbackground="black",  # Cursor color
            insertwidth=2,  # Cursor width
            highlightcolor="blue",  # Highlight color when focused
            highlightthickness=1,  # Highlight thickness
            highlightbackground="black",  # Highlight background color
            disabledbackground="lightgray",  # Background color when disabled
            disabledforeground="gray"  # Text color when disabled
        )
    
    def configure_label(self, label_widget):
        label_widget.config(
            font=("Helvetica", 12),  # Font and font size
            fg="black",  # Text color (foreground color)
            bg="white",  # Background color
            padx=5,  # Padding on the x-axis
            pady=5,  # Padding on the y-axis
            anchor="center",  # Text alignment (centered)
        )




    def show_welcome_page(self):
        self.tkn.geometry("850x600")  # Slightly increase the height for a more dynamic look

        #background color to white
        self.tkn.configure(bg="white")


        for widget in self.tkn.winfo_children():
            widget.destroy()


        #welcome to event hub label
        welcome_label = tkinter.Label(self.tkn, text="Welcome to Event Hub", font=("Helvetica", 20))
        welcome_label.pack(pady=0)
        #label background color to white
        welcome_label.configure(bg="white")


        #display the image in images/welcome.jpg 900x600
        welcome_image_path = Image.open("images/welcome.jpg")
        welcome_image = ImageTk.PhotoImage(welcome_image_path)        
        welcome_image_label = tkinter.Label(self.tkn, image=welcome_image)
        welcome_image_label.photo = welcome_image
        welcome_image_label.pack(pady=0)

        #display text and button upon the image
        #this happens after creating a frame and displaying the text and button on the frame
        #welcome frame
        welcome_frame = tkinter.Frame(self.tkn)
        welcome_frame.pack(pady=10)


        # introduce about the event hub
        label = tkinter.Label(self.tkn, text="Event Hub is a platform for event organizers to create and promote their events, and for users to discover and register for events.", font=("Helvetica", 10))
        label.configure(bg="white")
        label.pack(pady=10)

        #button to main page    
        #let's get started button
        get_started_button = tkinter.Button(self.tkn, text="Let's Get Started", command=self.show_main_page)
        self.configure_button(get_started_button)
        get_started_button.pack(pady=20)




        
    def show_main_page(self):
        for widget in self.tkn.winfo_children():
            widget.destroy()

        # Create a frame for the main page content
        main_frame = tkinter.Frame(self.tkn)
        main_frame.configure(bg="white")
        main_frame.pack(expand=True)

        # Add a title label
        title_label = tkinter.Label(main_frame, text="EVENT HUB", font=("Helvetica", 20))
        title_label.configure(bg="white")
        title_label.pack(pady=20)

        # Create a grid for the buttons
        button_frame = tkinter.Frame(main_frame)
        button_frame.configure(bg="white")
        button_frame.pack(expand=True)

        # Add buttons to navigate to different views
        welcome_button = tkinter.Button(button_frame, text="Back to Welcome Page", command=self.show_welcome_page)
        login_button = tkinter.Button(button_frame, text="Login", command=self.show_login_page)
        register_button = tkinter.Button(button_frame, text="Register", command=self.show_register_page)

        # Configure button appearance
        self.configure_button(welcome_button)
        self.configure_button(login_button)
        self.configure_button(register_button)

        # Pack the buttons in a grid layout
        welcome_button.grid(row=2, column=0, padx=10, pady=10)
        login_button.grid(row=0, column=0, padx=10, pady=10)
        register_button.grid(row=1, column=0, columnspan=2, padx=10, pady=10)


    def show_login_page(self):
        for widget in self.tkn.winfo_children():
            widget.destroy()

        # Add login form elements
        label = tkinter.Label(self.tkn, text="Welcome to Login", font=("Helvetica", 20))
        label.configure(bg="white")
        label.pack(pady=20)

        # Email (Gmail ID) entry
        self.email_entry = tkinter.Label(self.tkn, text="Enter Email ID :")
        self.email_entry.configure(bg="white")
        self.email_entry.pack()

        self.email_entry = tkinter.Entry(self.tkn)
        self.configure_entry(self.email_entry)
        self.email_entry.pack()

        # Send OTP button
        self.send_otp_button = tkinter.Button(self.tkn, text="Send OTP", command=self.verifyUser)
        self.configure_button(self.send_otp_button)  # Apply custom button styling
        self.send_otp_button.pack(pady=20)

        # Placeholder for OTP entry
        self.otp_label = tkinter.Label(self.tkn, text="Enter OTP:")
        self.otp_label.configure(bg="white")
        self.otp_label.pack()
        self.otp_entry = tkinter.Entry(self.tkn, state="disabled")  # Initially disabled
        self.configure_entry(self.otp_entry)
        self.otp_entry.pack()

        # Login button (disabled until OTP is entered)
        self.login_button = tkinter.Button(self.tkn, text="Login", command=self.loginUser, state="disabled")
        self.configure_button(self.login_button)  # Apply custom button styling
        self.login_button.pack(pady=20)

        # Register button
        self.register_button = tkinter.Button(self.tkn, text="Register", command=self.show_register_page)
        self.configure_button(self.register_button)  # Apply custom button styling
        self.register_button.pack(pady=10)

        # Back button to return to the welcome page
        self.back_button = tkinter.Button(self.tkn, text="Back to Welcome", command=self.show_welcome_page)
        self.configure_button(self.back_button)  # Apply custom button styling
        self.back_button.pack(pady=10)



    def show_register_page(self):
        for widget in self.tkn.winfo_children():
            widget.destroy()

        # Add registration form elements
        label = tkinter.Label(self.tkn, text="Register here for Event hub", font=("Helvetica", 20))
        label.configure(bg="white")
        label.pack(pady=20)

        # First Name entry
        self.first_name_label = tkinter.Label(self.tkn, text="First Name:")
        self.configure_label(self.first_name_label)
        self.first_name_label.pack()
        self.first_name_entry = tkinter.Entry(self.tkn)
        self.configure_entry(self.first_name_entry)
        self.first_name_entry.pack()

        # Last Name entry
        self.last_name_label = tkinter.Label(self.tkn, text="Last Name:")
        self.configure_label(self.last_name_label)
        self.last_name_label.pack()
        self.last_name_entry = tkinter.Entry(self.tkn)
        self.configure_entry(self.last_name_entry)
        self.last_name_entry.pack()

        # Email (Gmail ID) entry
        self.email_entry = tkinter.Label(self.tkn, text="Email (Gmail ID):")
        self.configure_label(self.email_entry)
        self.email_entry.pack()
        self.email_entry = tkinter.Entry(self.tkn)
        self.configure_entry(self.email_entry)
        self.email_entry.pack()

        # Password entry
        self.password_label = tkinter.Label(self.tkn, text="Password:")
        self.configure_label(self.password_label)
        self.password_label.pack()
        self.password_entry = tkinter.Entry(self.tkn,show="*")
        self.configure_entry(self.password_entry)
        self.password_entry.pack()

        # Register button
        self.register_button = tkinter.Button(self.tkn, text="Register", command=self.registerUser)
        self.configure_button(self.register_button)
        self.register_button.pack(pady=20)

        # Back button to return to the welcome page
        self.back_button = tkinter.Button(self.tkn, text="Back to Welcome", command=self.show_welcome_page)
        self.configure_button(self.back_button)
        self.back_button.pack(pady=10)


    def admin_dashboard(self):
        for widget in self.tkn.winfo_children():
            widget.destroy()

        # Add admin dashboard elements
        label = tkinter.Label(self.tkn, text="Admin Dashboard", font=("Helvetica", 20))
        label.configure(bg="white")
        label.pack(pady=20)

        #search bar to search events from treeview
        search_label = tkinter.Label(self.tkn, text="Search Event Name :")
        self.configure_label(search_label)
        search_label.pack()
        self.search_entry = tkinter.Entry(self.tkn)
        self.configure_entry(self.search_entry)
        self.search_entry.pack()

        #treeview of events 
        # Create a Treeview widget to display events
        event_tree = ttk.Treeview(self.tkn, columns=(
        "Event Name", "Event Date", "Event Time", "Event Location", "Event Description"), show="headings")
        event_tree.heading("#1", text="Event Name")
        event_tree.column("#1", width=150)
        event_tree.heading("#2", text="Event Date")
        event_tree.column("#2", width=150)
        event_tree.heading("#3", text="Event Time")
        event_tree.column("#3", width=150)
        event_tree.heading("#4", text="Event Location")
        event_tree.column("#4", width=150)
        event_tree.heading("#5", text="Event Description")
        event_tree.column("#5", width=150)

        # Connect to the 'events.db' database and retrieve event data from mysql   
        query = "SELECT * FROM eventhub.event"
        try:
            self.cursor.execute(query)
            events = self.cursor.fetchall()
        except mysql.Error as err:
            messagebox.showerror("Error", f"MySQL Error: {err}")
            return
        
        # Populate the Treeview with event data
        for event in events:
            event_tree.insert("", "end", values=event)
        
        event_tree.pack()

        # Add buttons to navigate to different views
        event_button = tkinter.Button(self.tkn, text="Add Event", command=self.show_admin_event_page)
        self.configure_button(event_button)
        event_button.pack(pady=20)

        logout_button = tkinter.Button(self.tkn, text="Logout", command=self.show_welcome_page)
        self.configure_button(logout_button)
        logout_button.pack(pady=10)


        
    def show_admin_event_page(self):
        self.tkn.geometry("800x500")
        for widget in self.tkn.winfo_children():
            widget.destroy()

        # Add event form elements
        label = tkinter.Label(self.tkn, text="Admin Event Page", font=("Helvetica", 20))
        label.configure(bg="white")
        label.pack(pady=20)

        # Event Name entry
        self.event_name_label = tkinter.Label(self.tkn, text="Event Name:")
        self.configure_label(self.event_name_label)
        self.event_name_label.pack()

        self.event_name_entry = tkinter.Entry(self.tkn)
        self.configure_entry(self.event_name_entry)
        self.event_name_entry.pack()

        # Event Date entry
        self.event_date_label = tkinter.Label(self.tkn, text="Event Date:")
        self.configure_label(self.event_date_label)
        self.event_date_label.pack()
        self.event_date_entry = DateEntry(self.tkn,width=15,background="darkblue", foreground="white", date_pattern="MM/dd/yyyy", font=("Arial", 15))
        # self.configure_entry(self.event_date_entry)
        self.event_date_entry.pack()

        # Event Time entry
        self.event_time_label = tkinter.Label(self.tkn, text="Event Time: HH:MM AM/PM")
        self.configure_label(self.event_time_label)
        self.event_time_label.pack()
        self.event_time_entry = tkinter.Entry(self.tkn)
        self.configure_entry(self.event_time_entry)
        self.event_time_entry.pack()

        # Event Location entry
        self.event_location_label = tkinter.Label(self.tkn, text="Event Location:")
        self.configure_label(self.event_location_label)
        self.event_location_label.pack()
        self.event_location_entry = tkinter.Entry(self.tkn)
        self.configure_entry(self.event_location_entry)
        self.event_location_entry.pack()

        # Event Description entry
        self.event_description_label = tkinter.Label(self.tkn, text="Event Description:")
        self.configure_label(self.event_description_label)
        self.event_description_label.pack()
        self.event_description_entry = tkinter.Entry(self.tkn)
        self.configure_entry(self.event_description_entry)
        self.event_description_entry.pack()

        # Register button
        self.register_button = tkinter.Button(self.tkn, text="Register", command=self.registerEvent)
        self.configure_button(self.register_button)
        self.register_button.pack(pady=10)

        #back to admin dashboard button
        self.back_button = tkinter.Button(self.tkn, text="Back to Admin Dashboard", command=self.admin_dashboard)
        self.configure_button(self.back_button)
        self.back_button.pack(pady=10)


    def user_dashboard(self):
        for widget in self.tkn.winfo_children():
            widget.destroy()

        # Add user dashboard elements
        label = tkinter.Label(self.tkn, text="User Dashboard", font=("Helvetica", 20))
        label.configure(bg="white")
        label.pack(pady=20)

        # Add buttons to navigate to different views
        event_button = tkinter.Button(self.tkn, text="Register for Event", command=self.show_user_event_page)
        self.configure_button(event_button)
        event_button.pack(pady=20)

        #create treeview of events registered by user
        # Create a Treeview widget to display events
        event_tree = ttk.Treeview(self.tkn, columns=(
            "Event Name", "Event Date", "Event Time", "Event Location", "Event Description"), show="headings")
        event_tree.heading("#1", text="Event Name")
        event_tree.column("#1", width=150)
        event_tree.heading("#2", text="Event Date")
        event_tree.column("#2", width=150)
        event_tree.heading("#3", text="Event Time")
        event_tree.column("#3", width=150)
        event_tree.heading("#4", text="Event Location")
        event_tree.column("#4", width=150)
        event_tree.heading("#5", text="Event Description")
        event_tree.column("#5", width=150)

        # Get the user's email (you should have a way to fetch the user's email after login)
        user_email = self.current_email

        # Connect to the MySQL database
        with self.database.cursor() as cursor:
                # Query the user table in MySQL to get the userID based on email
                cursor.execute("SELECT userID FROM eventhub.user WHERE email=%s", (user_email,))
                user_id = cursor.fetchone()
    
                if user_id:
                    # Query the eventRegistration table in MySQL to get eventIDs associated with the user
                    cursor.execute("SELECT eventID FROM eventhub.eventRegistration WHERE userID=%s", (user_id[0],))
                    event_ids = cursor.fetchall()
                else:
                    event_ids = []

        # Connect to the MySQL database
        with self.database.cursor() as cursor:
                # Retrieve event data for the user's registered events
                events = []
                for event_id in event_ids:
                    cursor.execute("SELECT * FROM eventhub.event WHERE eventID=%s", event_id)
                    event_data = cursor.fetchone()
                    events.append(event_data)

        # Populate the Treeview with events registered by the user
        #testing
        for event in events:
            event_tree.insert("", "end", values=event)

        event_tree.pack()

        logout_button = tkinter.Button(self.tkn, text="Logout", command=self.show_welcome_page)
        self.configure_button(logout_button)
        logout_button.pack(pady=10)


    def show_user_event_page(self):
        for widget in self.tkn.winfo_children():
            widget.destroy()

        # Add user event page elements
        label = tkinter.Label(self.tkn, text="User Event Page", font=("Helvetica", 20))
        label.configure(bg="white") 
        label.grid(row=0, column=0, columnspan=2, pady=20)

        # Search box
        search_label = tkinter.Label(self.tkn, text="Search Events:")
        self.configure_label(search_label)
        search_label.grid(row=1, column=0, pady=10)
        self.search_entry = tkinter.Entry(self.tkn)
        self.configure_entry(self.search_entry)
        self.search_entry.grid(row=1, column=1, pady=10)
        search_button = tkinter.Button(self.tkn, text="Search", command=self.search_events)
        self.configure_button(search_button)
        search_button.grid(row=1, column=2, pady=10)

        # Create a Treeview widget to display events
        self.event_tree = ttk.Treeview(self.tkn, columns=(
            "Event Name", "Event Date", "Event Time", "Event Location", "Event Description"), show="headings")
        self.event_tree.heading("#1", text="Event Name")
        self.event_tree.column("#1", width=150)
        self.event_tree.heading("#2", text="Event Date")
        self.event_tree.column("#2", width=150)
        self.event_tree.heading("#3", text="Event Time")
        self.event_tree.column("#3", width=150)
        self.event_tree.heading("#4", text="Event Location")
        self.event_tree.column("#4", width=150)
        self.event_tree.heading("#5", text="Event Description")
        self.event_tree.column("#5", width=150)

        # Connect to the MySQL database
        with self.database.cursor() as cursor:
            # Retrieve event data from the 'event' table in MySQL
            cursor.execute("SELECT * FROM eventhub.event")
            events = cursor.fetchall()

        # Populate the Treeview with event data
        for event in events:
            self.event_tree.insert("", "end", values=event)

        self.event_tree.grid(row=2, column=0, columnspan=3, padx=30,pady=10,sticky="nsew")

        # Register button to register for selected event
        register_button = tkinter.Button(self.tkn, text="Register", command=self.register_for_event)
        self.configure_button(register_button)
        register_button.grid(row=3, column=0, pady=10)

        user_dashboard_button = tkinter.Button(self.tkn, text="My Dashboard", command=self.user_dashboard)
        self.configure_button(user_dashboard_button)
        user_dashboard_button.grid(row=3, column=1, pady=10)

        # Back button to return to the main page
        back_button = tkinter.Button(self.tkn, text="Logout", command=self.show_main_page)
        self.configure_button(back_button)
        back_button.grid(row=3, column=2, pady=10)



    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



    def send_otp(self,gmail):
        #generate a random 6-digit OTP
        self.current_otp = random.randint(100000,999999)

        #setting up server
        server = smtplib.SMTP('smtp.gmail.com',587)
        server.starttls()

        password = "succyohrfxgyuhdv"
        sendermail="santhoshvaraprasad.u@gmail.com"
        #eventhub mail id
        #sendermail = "bis698eventhub@gmailcom"
        server.login(sendermail,password)

        body = f"Your OTP is {self.current_otp}"
        subject = "OTP verification for Eventhub"
        message = f'subject:{subject}\n\n{body}'

        try:
            server.sendmail(sendermail,gmail,message)
            #show message box otp sent
            messagebox.showinfo("OTP Sent", "OTP has been sent to your email")
        except Exception as e:
            print(e)
            messagebox.showerror("Error", "Unable to send OTP")

        server.quit()



    def verifyUser(self):
        #get the user's email
        self.current_email = self.email_entry.get()

        if self.current_email == "admin":
            self.admin_dashboard()
            #welcome to admin page message box
            messagebox.showinfo("Welcome", "Welcome Admin")
            return
        if self.current_email == "user":
            self.user_dashboard()
            #welcome to user page message box
            messagebox.showinfo("Welcome", "Welcome User")
            return

        #check with the database if the email exists
        query = "SELECT * FROM eventhub.user WHERE email = %s"
        data = (self.current_email,)
        try:
            self.cursor.execute(query, data)
            user = self.cursor.fetchone()
        except mysql.Error as err:
            messagebox.showerror("Error", f"MySQL Error: {err}")
            return
        
        if user is not None:
            #send OTP to the user's email
            self.send_otp(self.current_email)
        else:
            messagebox.showerror("Error", "User not found")

        self.otp_entry.configure(state="normal")
        self.login_button.configure(state="normal")




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
            user_email = self.current_email  # Replace with the actual user's email

            # Connect to the 'eventhub' database and retrieve the user's ID based on email
            query = "SELECT userID FROM eventhub.user WHERE email = %s"
            data = (user_email,)

            try:
                self.cursor.execute(query, data)
                user_id = self.cursor.fetchone()
            except mysql.Error as err:
                messagebox.showerror("Error", f"MySQL Error: {err}")
                return

            if user_id:
                # Check if the user has already registered for this event
                query = "SELECT * FROM eventhub.eventRegistration WHERE eventID = %s AND userID = %s"
                data = (event_data[0], user_id[0])

                try:
                    self.cursor.execute(query, data)
                    existing_registration = self.cursor.fetchone()
                except mysql.Error as err:
                    messagebox.showerror("Error", f"MySQL Error: {err}")
                    return

                if existing_registration:
                    messagebox.showinfo("Info", "You have already registered for this event.")
                else:
                    # Connect to the 'eventRegistration' database and insert the event's data
                    query = "INSERT INTO eventhub.eventRegistration(eventID, userID) VALUES (%s, %s)"
                    data = (event_data[0], user_id[0])

                    try:
                        self.cursor.execute(query, data)
                        self.database.commit()
                        messagebox.showinfo("Success", "You have registered for the event successfully!")
                        self.user_dashboard()
                    except mysql.Error as err:
                        messagebox.showerror("Error", f"MySQL Error: {err}")
            else:
                messagebox.showerror("Error", "User not found")


    def search_events(self):
        # Get the user's input
        search = self.search_entry.get()

        # Validate the user's input
        if search == "":
            messagebox.showerror("Error", "Please enter a search term")
        else:
            # Connect to the 'eventhub' database and retrieve event data
            query = "SELECT * FROM eventhub.event WHERE eventName LIKE %s"
            data = (f"%{search}%",)

            try:
                self.cursor.execute(query, data)
                events = self.cursor.fetchall()
            except mysql.Error as err:
                messagebox.showerror("Error", f"MySQL Error: {err}")
                return

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
            query = "INSERT INTO eventhub.user(firstName, lastName, email, password) VALUES (%s, %s, %s, %s)"
            data = (firstName, lastName, email, password)

            try:
                self.cursor.execute(query, data)
                self.database.commit()
                messagebox.showinfo("Success", "You have registered successfully!")
                self.show_login_page()
            except mysql.Error as err:
                messagebox.showerror("Error", f"MySQL Error: {err}")

    def loginUser(self):
        # Get the user otp
        otp = int(self.otp_entry.get())
    
        # Validate the user's input
        if otp == "" :
            messagebox.showerror("Error", "Please fill in otp sent to mail")
        else:
            # Connect to the 'eventhub' database and retrieve event data
            if otp == self.current_otp:
                messagebox.showinfo("Success", "You have logged in successfully!")
                self.user_dashboard()
            else:
                messagebox.showerror("Error", "Invalid otp. Click on send otp again")



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
            query = """INSERT INTO eventhub.event(eventName, eventDate, eventTime, eventLocation, eventDescription)
                    VALUES(%s, %s, %s, %s, %s)"""
            values = (eventName, eventDate, eventTime, eventLocation, eventDescription)

            self.cursor.execute(query, values)
            self.database.commit()

            messagebox.showinfo("Success", "You have registered successfully!")
            self.admin_dashboard()



# -----------------------------------------------------------------------------------------------------------------------


if __name__ == "__main__":
    app = EventHub()
    app.tkn.mainloop()
