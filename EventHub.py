import tkinter
from tkinter import messagebox
import tkinter.ttk as ttk
from PIL import ImageTk, Image
import mysql.connector as mysql
import random
import smtplib
from tkcalendar import Calendar, DateEntry
import sv_ttk

class EventHub():
    def __init__(self):
        super().__init__()
        self.tkn = tkinter.Tk()
        self.tkn.title("Event Hub")
        self.tkn.geometry("850x600")
        self.show_welcome_page()
        self.settheme = sv_ttk.set_theme('light')
        self.style = ttk.Style(self.tkn)
        self.style.configure('TNotebook.Tab', font=('Helvetica', '12', 'bold'))
        self.style.configure('TNotebook', tabposition='n')



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
        self.createOrganizerTable()
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
            phone VARCHAR(255) NOT NULL,
            password VARCHAR(255) NOT NULL
        );
        """
        self.cursor.execute(create_user_table)
        self.database.commit()


    #create oragnizer table
    def createOrganizerTable(self):
        # SQL statement for creating the 'organizer' table
        create_organizer_table = """
        CREATE TABLE IF NOT EXISTS organizer (
            organizerID INT AUTO_INCREMENT PRIMARY KEY,
            organizerName VARCHAR(255) NOT NULL,
            organizationEmail VARCHAR(255) NOT NULL,
            organizerPhone VARCHAR(255) NOT NULL,
            organizationName VARCHAR(255) NOT NULL,
            password VARCHAR(255) NOT NULL
        );
        """
        self.cursor.execute(create_organizer_table)
        self.database.commit()    

    def createEventTable(self):
        # SQL statement for creating the 'event' table
        create_event_table = """
        CREATE TABLE IF NOT EXISTS event (
            eventID INT AUTO_INCREMENT PRIMARY KEY,
            organizerID INT NOT NULL,
            eventName VARCHAR(255) NOT NULL,
            eventDate VARCHAR(255) NOT NULL,
            eventTime VARCHAR(255) NOT NULL,
            eventLocation VARCHAR(255) NOT NULL,
            eventDescription TEXT NOT NULL,
            registeredCount INT NOT NULL DEFAULT 0,
            FOREIGN KEY (organizerID) REFERENCES organizer (organizerID)
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
            organizerID INT NOT NULL,
            userID INT NOT NULL,
            FOREIGN KEY (eventID) REFERENCES event (eventID),
            FOREIGN KEY (userID) REFERENCES user (userID),
            FOREIGN KEY (organizerID) REFERENCES organizer (organizerID)
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
        # self.cursor.close()
        self.database.close()


    def configure_button(self, button):
        #curver border
        button.configure(bg="#0078d4", fg="white", font=("Verdana", 12), relief="raised")
        #button rounded border
        button.configure(borderwidth=3, highlightthickness=3, width=20, height=1)

    # def configure_button(self, button):
    #     button.configure(
    #         corjer_radius=6,
    #         border_width=0,
    #         fg_color=["#3B8ED0", "#1F6AA5"],
    #         hover_color=["#36719F", "#144870"],
    #         border_color=["#3E454A", "#949A9F"],
    #         text_color=["#DCE4EE", "#DCE4EE"],
    #         text_color_disabled=["gray74", "gray60"]
    #     )

         


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


    #show register page should contain two tabs one for user to register and one for organizer to register
    def show_register_page(self):
        for widget in self.tkn.winfo_children():
            widget.destroy()

        # Add registration form elements
        label = tkinter.Label(self.tkn, text="Register here for Event hub", font=("Helvetica", 20))
        label.configure(bg="white")
        label.pack(pady=20)


        #tabs for register as user or organizer
        #create tabs
        tab_control = ttk.Notebook(self.tkn)
        tab1 = ttk.Frame(tab_control,width=200, height=200)
        tab2 = ttk.Frame(tab_control,width=200, height=100)
        tab_control.add(tab1, text='Register as User',sticky="nsew")
        tab_control.add(tab2, text='Register as Organizer',sticky="nsew")
        tab_control.pack(expand=1, fill='both')

        #tab text and position to center
        tab_control.tab(0, text="Register as User",compound=tkinter.CENTER)
        tab_control.tab(1, text="Register as Organizer",compound=tkinter.CENTER)

        #tab1 for user label and entry side by side

        # First Name entry
        self.first_name_label = tkinter.Label(tab1, text="First Name:")
        self.configure_label(self.first_name_label)
        self.first_name_label.pack()
        self.first_name_entry = tkinter.Entry(tab1)
        self.configure_entry(self.first_name_entry)
        self.first_name_entry.pack()

        # Last Name entry
        self.last_name_label = tkinter.Label(tab1, text="Last Name:")
        self.configure_label(self.last_name_label)
        self.last_name_label.pack()
        self.last_name_entry = tkinter.Entry(tab1)
        self.configure_entry(self.last_name_entry)
        self.last_name_entry.pack()

        # Email (Gmail ID) entry
        self.email_entry = tkinter.Label(tab1, text="Email :")
        self.configure_label(self.email_entry)
        self.email_entry.pack()
        self.email_entry = tkinter.Entry(tab1)
        self.configure_entry(self.email_entry)
        self.email_entry.pack()

        #set phone number default extension as +1 like enter the phone number with +1
        # Phone Number entry
        self.phone_label = tkinter.Label(tab1, text="Phone Number:")
        self.configure_label(self.phone_label)
        self.phone_label.pack()
        self.user_phone_entry = tkinter.Entry(tab1)
        self.configure_entry(self.user_phone_entry)
        self.user_phone_entry.pack()

        self.user_phone_entry.insert(0, "+1")



        # Password entry
        self.password_label = tkinter.Label(tab1, text="Password:")
        self.configure_label(self.password_label)
        self.password_label.pack()
        self.user_password_entry = tkinter.Entry(tab1,show="*")
        self.configure_entry(self.user_password_entry)
        self.user_password_entry.pack()

                



        


        # Register button
        self.register_button = tkinter.Button(tab1, text="Register", command=self.registerUser)
        self.configure_button(self.register_button)
        self.register_button.pack(pady=20)

        # Back button to return to the welcome page
        self.back_button = tkinter.Button(tab1, text="Back to Welcome", command=self.show_welcome_page)
        self.configure_button(self.back_button)
        self.back_button.pack(pady=10)

        #tab2 for organizer

        # organizer full name entry
        self.organizer_name_label = tkinter.Label(tab2, text="Organizer Full Name:")
        self.configure_label(self.organizer_name_label)
        self.organizer_name_label.pack()
        self.organizer_name_entry = tkinter.Entry(tab2)
        self.configure_entry(self.organizer_name_entry)
        self.organizer_name_entry.pack()

        #organization name entry
        self.organization_name_label = tkinter.Label(tab2, text="Organization Name:")
        self.configure_label(self.organization_name_label)
        self.organization_name_label.pack()
        self.organization_name_entry = tkinter.Entry(tab2)
        self.configure_entry(self.organization_name_entry)
        self.organization_name_entry.pack()

        # organizer email entry
        self.organizer_email_label = tkinter.Label(tab2, text="Organization Email:")
        self.configure_label(self.organizer_email_label)
        self.organizer_email_label.pack()
        self.organizer_email_entry = tkinter.Entry(tab2)
        self.configure_entry(self.organizer_email_entry)
        self.organizer_email_entry.pack()



        #organizer phone number entry
        self.organizer_phone_label = tkinter.Label(tab2, text="Organizer Phone Number:")
        self.configure_label(self.organizer_phone_label)
        self.organizer_phone_label.pack()
        self.organizer_phone_entry = tkinter.Entry(tab2)
        self.configure_entry(self.organizer_phone_entry)
        self.organizer_phone_entry.pack()

        self.organizer_phone_entry.insert(0, "+1")

        # Password entry
        self.password_label = tkinter.Label(tab2, text="Password:")
        self.configure_label(self.password_label)
        self.password_label.pack()
        self.organizer_password_entry = tkinter.Entry(tab2,show="*")
        self.configure_entry(self.organizer_password_entry)
        self.organizer_password_entry.pack()



        # Register button
        self.register_button = tkinter.Button(tab2, text="Register", command=self.registerOrganizer)
        self.configure_button(self.register_button)
        self.register_button.pack(pady=20)
        
        # Back button to return to the welcome page
        self.back_button = tkinter.Button(tab2, text="Back to Welcome", command=self.show_welcome_page)
        self.configure_button(self.back_button)
        self.back_button.pack(pady=10)

    #organizerdashboard
    def organizer_dashboard(self):
        for widget in self.tkn.winfo_children():
            widget.destroy()

        # Add organizer dashboard elements
        label = tkinter.Label(self.tkn, text="Organizer Dashboard", font=("Helvetica", 20))
        label.configure(bg="white")
        label.pack(pady=20)

        #treeview of the events created by the organizer
        # Create a Treeview widget to display events
        self.org_event_tree = ttk.Treeview(self.tkn, columns=(
            "Event Name", "Event Date", "Event Time", "Event Location", "Registered Count"), show="headings")
        self.org_event_tree.heading("#1", text="Event Name")
        self.org_event_tree.column("#1", width=150,anchor="center")
        self.org_event_tree.heading("#2", text="Event Date")
        self.org_event_tree.column("#2", width=150,anchor="center")
        self.org_event_tree.heading("#3", text="Event Time")
        self.org_event_tree.column("#3", width=150, anchor="center")
        self.org_event_tree.heading("#4", text="Event Location")
        self.org_event_tree.column("#4", width=150, anchor="center")
        self.org_event_tree.heading("#5", text="Registered Count")
        self.org_event_tree.column("#5", width=150, anchor="center")

        # Get the organizer's email (you should have a way to fetch the organizer's email after login)
        organizer_email = self.current_email

        # Connect to the MySQL database
        with self.database.cursor() as cursor:
                # Query the organizer table in MySQL to get the organizerID based on email
                cursor.execute("SELECT organizerID FROM eventhub.organizer WHERE organizationEmail=%s", (organizer_email,))
                organizer_id = cursor.fetchone()
    
                if organizer_id:
                    # Query the event table in MySQL to get eventIDs associated with the organizer
                    cursor.execute("SELECT eventID FROM eventhub.event WHERE organizerID=%s", (organizer_id[0],))
                    event_ids = cursor.fetchall()
                else:
                    event_ids = []
                
                cursor.close()
        
        # Connect to the MySQL database
        with self.database.cursor() as cursor:
                # Retrieve event data for the organizer's events w
                events = []
                for event_id in event_ids:
                    cursor.execute("SELECT * FROM eventhub.event WHERE eventID=%s", event_id)
                    event_data = cursor.fetchone()
                    #append all info except eventID and eventDescription
                    events.append(event_data[2:6] + event_data[7:])

                cursor.close()
        
        # Populate the Treeview with events created by the organizer
        #testing
        for event in events:
            self.org_event_tree.insert("", "end", values=event)

        self.org_event_tree.pack()

        #event registration details button
        event_rsvp_details_button = tkinter.Button(self.tkn, text="Event RSVP Details", command=self.org_show_event_rsvp_details_page)
        self.configure_button(event_rsvp_details_button)
        event_rsvp_details_button.pack(pady=20)

        # Add buttons to navigate to different views
        event_button = tkinter.Button(self.tkn, text="Add Event", command=self.show_organizer_event_page)
        self.configure_button(event_button)
        event_button.pack(pady=20)

        logout_button = tkinter.Button(self.tkn, text="Logout", command=self.show_welcome_page)
        self.configure_button(logout_button)
        logout_button.pack(pady=10)


    #org_show_event_rsvp_details_page
    def org_show_event_rsvp_details_page(self):
        
        org_page_current_event = self.org_event_tree.focus()

        for widget in self.tkn.winfo_children():
            widget.destroy()

        #Event RSVP Details Page
        label = tkinter.Label(self.tkn, text="Event RSVP Details Page", font=("Helvetica", 20))
        label.configure(bg="white")
        label.pack(pady=20)

        #treeview of users registered to that particular event
        # Create a Treeview widget to display events
        event_tree = ttk.Treeview(self.tkn, columns=(
            "User Name", "User Email", "User Phone"), show="headings")
        event_tree.heading("#1", text="User Name")
        event_tree.column("#1", width=150,anchor="center")
        event_tree.heading("#2", text="User Email")
        event_tree.column("#2", width=150,anchor="center")
        event_tree.heading("#3", text="User Phone")
        event_tree.column("#3", width=150, anchor="center")


        #get users id that are registered to the event and then get their details
        # Connect to the MySQL database
        with self.database.cursor() as cursor:
                # Query the event table in MySQL to get the eventID based on eventName
                cursor.execute("SELECT eventID FROM eventhub.event WHERE eventName=%s", (org_page_current_event,))
                event_id = cursor.fetchone()
    
                if event_id:
                    # Query the eventRegistration table in MySQL to get userID associated with the event
                    cursor.execute("SELECT userID FROM eventhub.eventRegistration WHERE eventID=%s", (event_id[0],))
                    user_ids = cursor.fetchall()
                else:
                    user_ids = []
                
                cursor.close()
            
        # Connect to the MySQL database
        with self.database.cursor() as cursor:
                # Retrieve user data for the users registered to the event
                users = []
                for user_id in user_ids:
                    cursor.execute("SELECT * FROM eventhub.user WHERE userID=%s", user_id)
                    user_data = cursor.fetchone()
                    #append all info except userID and password
                    users.append(user_data[1:3] + user_data[5:])

                cursor.close()

        # Populate the Treeview with users registered to the event
        #testing
        for user in users:
            event_tree.insert("", "end", values=user)
        
        event_tree.pack()

        #back to organizer dashboard button
        self.back_button = tkinter.Button(self.tkn, text="Back to Organizer Dashboard", command=self.organizer_dashboard)




        

        
    #show_organizer_event_page
    def show_organizer_event_page(self):
        for widget in self.tkn.winfo_children():
            widget.destroy()

        # Add event form elements
        label = tkinter.Label(self.tkn, text="Organizer Event Page", font=("Helvetica", 20))
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
        self.event_date_label = tkinter.Label(self.tkn, text="Event Date: MM/DD/YYYY")
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
        self.register_button = tkinter.Button(self.tkn, text="Create Event", command=self.registerEvent)
        self.configure_button(self.register_button)
        self.register_button.pack(pady=10)

        #back to organizer dashboard button
        self.back_button = tkinter.Button(self.tkn, text="Back to Organizer Dashboard", command=self.organizer_dashboard)
        self.configure_button(self.back_button)
        self.back_button.configure(width=30)
        self.back_button.pack(pady=10)


    def admin_dashboard(self):
        for widget in self.tkn.winfo_children():
            widget.destroy()

        # Add admin dashboard elements
        label = tkinter.Label(self.tkn, text="Admin Dashboard", font=("Helvetica", 20))
        label.configure(bg="white")
        label.pack(pady=20)

        logout_button = tkinter.Button(self.tkn, text="Logout", command=self.show_welcome_page)
        self.configure_button(logout_button)
        logout_button.pack(pady=10)


        
    def show_admin_event_page(self):
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
        self.register_button = tkinter.Button(self.tkn, text="Create Event", command=self.registerEvent)
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
        event_tree.column("#1", width=150,anchor="center")
        event_tree.heading("#2", text="Event Date")
        event_tree.column("#2", width=150,anchor="center")
        event_tree.heading("#3", text="Event Time")
        event_tree.column("#3", width=150, anchor="center")
        event_tree.heading("#4", text="Event Location")
        event_tree.column("#4", width=150, anchor="center")
        event_tree.heading("#5", text="Event Description")
        event_tree.column("#5", width=150, anchor="center")

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
                
                cursor.close()

        # Connect to the MySQL database
        with self.database.cursor() as cursor:
                # Retrieve event data for the user's registered events
                events = []
                for event_id in event_ids:
                    cursor.execute("SELECT * FROM eventhub.event WHERE eventID=%s", event_id)
                    event_data = cursor.fetchone()
                    #append all info except eventID
                    events.append(event_data[1:])

                cursor.close()






        # Populate the Treeview with events registered by the user
        #testing
        #insert all the data except eventID , organizerID and registeredCount
        for event in events:
            event_tree.insert("", "end", values=event[1:6])

        event_tree.pack()

        logout_button = tkinter.Button(self.tkn, text="Logout", command=self.show_welcome_page)
        self.configure_button(logout_button)
        logout_button.pack(pady=10)


    def show_user_event_page(self):
        self.tkn.geometry("1000x600")
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
            "Event ID","Event Name", "Event Date", "Event Time", "Event Location", "Event Description"), show="headings")
        self.event_tree.heading("#1", text="Event ID")
        self.event_tree.column("#1", width=150,anchor="center")
        self.event_tree.heading("#2", text="Event Name")
        self.event_tree.column("#2", width=150, anchor="center")
        self.event_tree.heading("#3", text="Event Date")
        self.event_tree.column("#3", width=150, anchor="center")
        self.event_tree.heading("#4", text="Event Time")
        self.event_tree.column("#4", width=150, anchor="center")
        self.event_tree.heading("#5", text="Event Location")
        self.event_tree.column("#5", width=150, anchor="center")
        self.event_tree.heading("#6", text="Event Description")
        self.event_tree.column("#6", width=150, anchor="center")


        # Connect to the MySQL database
        with self.database.cursor() as cursor:
            # Retrieve event data from the 'event' table in MySQL
            cursor.execute("SELECT * FROM eventhub.event")
            events = cursor.fetchall()

        # Populate the Treeview with event data
        #insert all info exceptdescription and organizerID
        for event in events:
            self.event_tree.insert("", "end", values=event[0:1] + event[2:])

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

    #registerOrganizer
    def registerOrganizer(self):
        # Get the user's input
        organizerName = self.organizer_name_entry.get()
        organizationEmail = self.organizer_email_entry.get()
        organizerPhone = self.organizer_phone_entry.get()
        organizationName = self.organization_name_entry.get()
        password = self.organizer_password_entry.get()

        #verify email
        if not organizationEmail.endswith("@gmail.com"):
            messagebox.showerror("Error", "Please enter a valid gmail address")
            return
        
        #verify phone number and count of digits
        if len(organizerPhone) != 12:
            messagebox.showerror("Error", "Please enter a valid phone number")
            return
        
        #verify password length and special characters
        if len(password) < 8:
            messagebox.showerror("Error", "Password must be at least 8 characters long")
            return
        
        if not any(char.isdigit() for char in password):
            messagebox.showerror("Error", "Password must contain at least one number")
            return
        
        if not any(char.isupper() for char in password):
            messagebox.showerror("Error", "Password must contain at least one uppercase letter")
            return
        
        if not any(char.islower() for char in password):
            messagebox.showerror("Error", "Password must contain at least one lowercase letter")
            return
        
        if not any(char in "!@#$%^&*()-+?_=,<>/;:[]{}" for char in password):
            messagebox.showerror("Error", "Password must contain at least one special character")
            return
        

        
        # Validate the user's input
        if organizerName == "" or organizationEmail == "" or organizerPhone == "" or organizationName == "" or password == "":
            messagebox.showerror("Error", "Please fill in all fields")
        else:
            # Insert the user's input into the database
            query = "INSERT INTO eventhub.organizer(organizerName, organizationEmail, organizerPhone, organizationName,password) VALUES (%s, %s, %s, %s,%s)"
            data = (organizerName, organizationEmail, organizerPhone, organizationName,password)

            try:
                self.cursor.execute(query, data)
                self.database.commit()
                messagebox.showinfo("Success", "You have registered successfully!")
                self.show_login_page()
            except mysql.Error as err:
                messagebox.showerror("Error", f"MySQL Error: {err}")

    def send_otp(self,gmail):
        #generate a random 6-digit OTP
        self.current_otp = random.randint(100000,999999)

        #setting up server
        server = smtplib.SMTP('smtp.gmail.com',587)
        server.starttls()

        password = "ecyvohyivtvbawwy"
        sendermail = "bis698eventhub@gmail.com"
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
            return
        

        self.user_type = ""
        #check with the database if the email exists
        query = "SELECT * FROM eventhub.user WHERE email = %s"
        data = (self.current_email,)
        try:
            self.cursor.execute(query, data)
            user = self.cursor.fetchone()
        except mysql.Error as err:
            messagebox.showerror("Error", f"MySQL Error: {err}")
            return
        
        #check with the organizer database if the email exists
        query = "SELECT * FROM eventhub.organizer WHERE organizationEmail = %s"
        data = (self.current_email,)
        try:
            self.cursor.execute(query, data)
            organizer = self.cursor.fetchone()
        except mysql.Error as err:
            messagebox.showerror("Error", f"MySQL Error: {err}")
            return
        
        self.current_user_object = None
        
        if user is not None:
            self.user_type = "user"
            self.current_user_object = user
            #testuser 
            if self.current_email == "user@gmail.com":
                self.user_dashboard()
                return

            #send OTP to the user's email
            self.send_otp(self.current_email)

        elif organizer is not None:

            self.user_type = "organizer"
            self.current_user_object = organizer
            #testorganizer
            if self.current_email == "organizer@gmail.com":
                self.organizer_dashboard()
                return
            #send OTP to the organizer's email
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
            # Get the eventid
            event_data = self.event_tree.item(selected_event, "values")

            event_id=event_data[0]

            #get the whole event data with eventID
            query = "SELECT * FROM eventhub.event WHERE eventID = %s"
            data = (event_id,)
            try:
                self.cursor.execute(query, data)
                event_data = self.cursor.fetchone()
            except mysql.Error as err:
                messagebox.showerror("Error", f"MySQL Error: {err}")
                return
            

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
            
            #get 

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
                    query = "INSERT INTO eventhub.eventRegistration(eventID, userID,organizerID) VALUES (%s, %s,%s)"
                    data = (event_data[0], user_id[0],event_data[1])
                    #increment query
                    query2 = "UPDATE eventhub.event SET registeredCount = registeredCount + 1 WHERE eventID = %s"
                    data2 = (event_data[0],)
                    try:
                        self.cursor.execute(query, data)
                        self.cursor.execute(query2, data2)
                        self.database.commit()
                        #send gmail confirmation method
                        self.sendEmailConfirmation(user_email,event_data)
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
            #insert all info except eventID
            for event in events:
                self.event_tree.insert("", "end", values=event[1:]) 


    def registerUser(self):
        # Get the user's input
        firstName = self.first_name_entry.get()
        lastName = self.last_name_entry.get()
        email = self.email_entry.get()
        password = self.user_password_entry.get()
        phone = self.user_phone_entry.get()

        #verify email

        if not email.endswith("@gmail.com"):
            messagebox.showerror("Error", "Please enter a valid gmail address")
            return
        
        #verify phone number and count of digits
        if len(phone) != 12:
            messagebox.showerror("Error", "Please enter a valid phone number")
            return
        
        print(len(password))
        
        #verify password length and special characters
        if len(password) < 8:
            messagebox.showerror("Error", "Password must be atleast 8 characters long")
            return
        
        if not any(char.isdigit() for char in password):
            messagebox.showerror("Error", "Password must contain atleast one digit")
            return
        
        if not any(char.isupper() for char in password):
            messagebox.showerror("Error", "Password must contain atleast one uppercase letter")
            return
        
        if not any(char.islower() for char in password):
            messagebox.showerror("Error", "Password must contain atleast one lowercase letter")
            return
        
        SpecialSym =['$', '@', '#', '%']
        
        if not any(char in SpecialSym for char in password):
            messagebox.showerror("Error", "Password must contain atleast one special character")
            return
        

        # Validate the user's input
        if firstName == "" or lastName == "" or email == "" or password == "":
            messagebox.showerror("Error", "Please fill in all fields")
        else:
            # Insert the user's input into the database
            query = "INSERT INTO eventhub.user(firstName, lastName, email, password,phone) VALUES (%s, %s, %s, %s,%s)"
            data = (firstName, lastName, email, password,phone)

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
                if self.user_type == "user":
                    self.user_dashboard()
                elif self.user_type == "organizer":
                    self.organizer_dashboard()
            else:
                messagebox.showerror("Error", "Invalid otp. Click on send otp again")


    #sendEmailConfirmation
    def sendEmailConfirmation(self,user_email,event_data):
        #setting up server
        server = smtplib.SMTP('smtp.gmail.com',587)
        server.starttls()
        
        password = "ecyvohyivtvbawwy"
        sendermail = "bis698eventhub@gmail.com"
        server.login(sendermail,password)

        body = f"Thank you for registering for {event_data[3]} event on {event_data[4]} at {event_data[5]}.\n\nEvent Description: {event_data[6]}"
        subject = "Event Registration Confirmation"
        message = f'subject:{subject}\n\n{body}'
        try:
            server.sendmail(sendermail,user_email,message)
            #show message box otp sent
            messagebox.showinfo("Email Sent", "Confirmation email has been sent to your email")
        except Exception as e:
            print(e)
            messagebox.showerror("Error", "Unable to send email")

        server.quit()


        



    def registerEvent(self):
        # Get the user's input
        eventName = self.event_name_entry.get()
        eventDate = self.event_date_entry.get()
        eventTime = self.event_time_entry.get()
        eventLocation = self.event_location_entry.get()
        eventDescription = self.event_description_entry.get()

        #get current organizer id from current_user_object
        organizer_id = self.current_user_object[0]



        # Validate the user's input
        if eventName == "" or eventDate == "" or eventTime == "" or eventLocation == "" or eventDescription == "":
            messagebox.showerror("Error", "Please fill in all fields")
        else:
            # Insert the user's input into the database with organizerID
            query = "INSERT INTO eventhub.event(eventName, eventDate, eventTime, eventLocation, eventDescription, organizerID) VALUES (%s, %s, %s, %s, %s, %s)"
            values = (eventName, eventDate, eventTime, eventLocation, eventDescription, organizer_id)


            self.cursor.execute(query, values)
            self.database.commit()

            messagebox.showinfo("Success", "You have registered successfully!")
            self.organizer_dashboard()


# -----------------------------------------------------------------------------------------------------------------------


if __name__ == "__main__":
    app = EventHub()
    app.tkn.mainloop()
