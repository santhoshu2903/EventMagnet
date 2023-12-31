from datetime import datetime
import os
import re
import tkinter
from tkinter import messagebox
from tkinter import filedialog
import tkinter.ttk as ttk
from PIL import ImageTk, Image
import mysql.connector as mysql
import random
import smtplib
from tkcalendar import Calendar, DateEntry
import sv_ttk
from fpdf import FPDF

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
            eventDate DATE NOT NULL,
            eventTime TIME NOT NULL,
            eventLocation VARCHAR(255) NOT NULL,
            eventDescription TEXT NOT NULL,
            eventImage VARCHAR(255) NOT NULL,
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
        CREATE TABLE IF NOT EXISTS eventfeedback     (
            eventCommentID INT AUTO_INCREMENT PRIMARY KEY,
            eventID INT NOT NULL,
            userID INT NOT NULL,
            rating TEXT NOT NULL,
            feedback TEXT NOT NULL,
            FOREIGN KEY (eventID) REFERENCES event (eventID),
            FOREIGN KEY (userID) REFERENCES user (userID)
        );
        """
        self.cursor.execute(create_event_comment_table)

        # Commit the changes to the database
        self.database.commit()

    def __del__(self):
        self.database.close()



    def configure_button(self, button):
        #curver border
        button.configure(bg="#0078d4", fg="white", font=("Verdana", 12), relief="raised")
        #button rounded border
        button.configure(borderwidth=3, highlightthickness=3, width=20, height=1)
    

    def configure_entry(self, entry_widget):
        entry_widget.config(
            font=("Arial", 12),  # Font and font size
            bd=2,  # Border widt
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
        self.tkn.geometry("900x600")
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

        self.tkn.geometry("700x500")

        # #Event Hub label
        # event_hub_label = tkinter.Label(self.tkn, text="Event Hub", font=("Helvetica", 20))
        # event_hub_label.configure(bg="white")
        # event_hub_label.pack(pady=10)

        #create frame for the main page
        main_page_frame = tkinter.Frame(self.tkn)
        #bg
        main_page_frame.configure(bg="white")
        main_page_frame.pack()

        #display bg image in the main page
        #display the image in images/welcome.jpg 900x600
        main_page_image= Image.open("images/bg.jpeg")
        main_page_image = main_page_image.resize((700, 500), Image.LANCZOS)
        main_page_image = ImageTk.PhotoImage(main_page_image)
        #resize the image
        main_page_image_label = tkinter.Label(main_page_frame, image=main_page_image)
        main_page_image_label.photo = main_page_image
        main_page_image_label.pack()

        #display login, register and back to welcome page buttons upon the image

        #login button
        login_button = tkinter.Button(main_page_frame, text="Login", command=self.show_login_page,)
        self.configure_button(login_button)
        login_button=login_button\
            .place(relx=0.5, rely=0.2, anchor="center")

        #register button
        register_button = tkinter.Button(main_page_frame, text="Register", command=self.show_register_page)
        self.configure_button(register_button)  
        register_button=register_button\
            .place(relx=0.5, rely=0.4, anchor="center")

        #back to welcome page button
        back_button = tkinter.Button(main_page_frame, text="Back to Welcome", command=self.show_welcome_page)
        self.configure_button(back_button)
        back_button=back_button\
            .place(relx=0.5, rely=0.6, anchor="center")



    def show_login_page(self):
        for widget in self.tkn.winfo_children():
            widget.destroy()

        # Add login form elements
        label = tkinter.Label(self.tkn, text="Welcome to Login", font=("Helvetica", 20))
        label.configure(bg="white")
        label.pack(pady=20)


        # First Name entry

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
        self.tkn.geometry("900x600")
        for widget in self.tkn.winfo_children():
            widget.destroy()

        # Add registration form elements
        label = tkinter.Label(self.tkn, text="Register here for Event hub", font=("Helvetica", 20))
        label.configure(bg="white")
        label.pack(pady=20)

        # Create tabs
        self.tab_control = ttk.Notebook(self.tkn)
        tab1 = ttk.Frame(self.tab_control, width=200, height=200)
        tab2 = ttk.Frame(self.tab_control, width=200, height=100)
        self.tab_control.add(tab1, text='Register as User', sticky="nsew")
        self.tab_control.add(tab2, text='Register as Organizer', sticky="nsew")
        self.tab_control.pack(expand=1, fill='both')

        # Tab 1: Register as User
        tab1_frame = tkinter.Frame(tab1)
        tab1_frame.pack(padx=20, pady=20)

        # First Name entry
        self.first_name_label = tkinter.Label(tab1_frame, text="First Name:")
        self.configure_label(self.first_name_label)
        self.first_name_label.grid(row=0, column=0)
        self.first_name_entry = tkinter.Entry(tab1_frame)
        self.configure_entry(self.first_name_entry)
        self.first_name_entry.grid(row=0, column=1)

        # Last Name entry
        self.last_name_label = tkinter.Label(tab1_frame, text="Last Name:")
        self.configure_label(self.last_name_label)
        self.last_name_label.grid(row=1, column=0)
        self.last_name_entry = tkinter.Entry(tab1_frame)
        self.configure_entry(self.last_name_entry)
        self.last_name_entry.grid(row=1, column=1)

        # Email (Gmail ID) entry
        self.email_entry = tkinter.Label(tab1_frame, text="Email :")
        self.configure_label(self.email_entry)
        self.email_entry.grid(row=2, column=0)
        self.email_entry = tkinter.Entry(tab1_frame)
        self.configure_entry(self.email_entry)
        self.email_entry.grid(row=2, column=1)

        # Phone Number entry
        self.phone_label = tkinter.Label(tab1_frame, text="Phone Number:")
        self.configure_label(self.phone_label)
        self.phone_label.grid(row=3, column=0)
        self.user_phone_entry = tkinter.Entry(tab1_frame)
        self.configure_entry(self.user_phone_entry)
        self.user_phone_entry.grid(row=3, column=1)

        self.user_phone_entry.insert(0, "+1")

        # Password entry
        self.password_label = tkinter.Label(tab1_frame, text="Password:")
        self.configure_label(self.password_label)
        self.password_label.grid(row=4, column=0)
        self.user_password_entry = tkinter.Entry(tab1_frame, show="*")
        self.configure_entry(self.user_password_entry)
        self.user_password_entry.grid(row=4, column=1)

                #password valodation's
        # Password must be atleast 8 characters long
        # Password must contain atleast one digit
        # Password must contain atleast one uppercase letter
        # Password must contain atleast one lowercase letter
        # Special characters like $&@#%*
        #show then in green if valid else red
        # Password entry
        self.password_label0 = tkinter.Label(tab1_frame, text="Password must be atleast 8 characters long",font=("Helvetica", 8),fg="red")
        self.password_label0.grid(row=5, column=0, columnspan=2)

        self.password_label1 = tkinter.Label(tab1_frame, text="Password must contain atleast one digit",font=("Helvetica", 8),fg="red")
        self.password_label1.grid(row=6, column=0, columnspan=2)

        self.password_label2 = tkinter.Label(tab1_frame, text="Password must contain atleast one uppercase letter",font=("Helvetica", 8),fg="red")
        self.password_label2.grid(row=7, column=0, columnspan=2)

        self.password_label3 = tkinter.Label(tab1_frame, text="Password must contain atleast one lowercase letter",font=("Helvetica", 8),fg="red")
        self.password_label3.grid(row=8, column=0, columnspan=2)

        self.password_label4 = tkinter.Label(tab1_frame, text="Password must contain atleast one special character",font=("Helvetica", 8),fg="red")
        self.password_label4.grid(row=9, column=0, columnspan=2)

        # Check if passentry is 8 characters long
        self.user_password_entry.bind("<KeyRelease>", lambda event: self.password_validation(event))

        # Register button
        self.register_button = tkinter.Button(tab1_frame, text="Register", command=self.registerUser)
        self.configure_button(self.register_button)
        self.register_button.grid(row=10, column=0, columnspan=2, pady=20)

        # Back button to return to the welcome page
        self.back_button = tkinter.Button(tab1_frame, text="Back to Welcome", command=self.show_welcome_page)
        self.configure_button(self.back_button)
        self.back_button.grid(row=11, column=0, columnspan=2, pady=10)

        # Tab 2: Register as Organizer
        tab2_frame = tkinter.Frame(tab2)
        tab2_frame.pack(padx=20, pady=20)

        # Organizer full name entry
        self.organizer_name_label = tkinter.Label(tab2_frame, text="Organizer Full Name:")
        self.configure_label(self.organizer_name_label)
        self.organizer_name_label.grid(row=0, column=0)
        self.organizer_name_entry = tkinter.Entry(tab2_frame)
        self.configure_entry(self.organizer_name_entry)
        self.organizer_name_entry.grid(row=0, column=1)

        # Organization name entry
        self.organization_name_label = tkinter.Label(tab2_frame, text="Organization Name:")
        self.configure_label(self.organization_name_label)
        self.organization_name_label.grid(row=1, column=0)
        self.organization_name_entry = tkinter.Entry(tab2_frame)
        self.configure_entry(self.organization_name_entry)
        self.organization_name_entry.grid(row=1, column=1)

        # Organizer email entry
        self.organizer_email_label = tkinter.Label(tab2_frame, text="Organization Email:")
        self.configure_label(self.organizer_email_label)
        self.organizer_email_label.grid(row=2, column=0)
        self.organizer_email_entry = tkinter.Entry(tab2_frame)
        self.configure_entry(self.organizer_email_entry)
        self.organizer_email_entry.grid(row=2, column=1)

        # Organizer phone number entry
        self.organizer_phone_label = tkinter.Label(tab2_frame, text="Organizer Phone Number:")
        self.configure_label(self.organizer_phone_label)
        self.organizer_phone_label.grid(row=3, column=0)
        self.organizer_phone_entry = tkinter.Entry(tab2_frame)
        self.configure_entry(self.organizer_phone_entry)
        self.organizer_phone_entry.grid(row=3, column=1)

        self.organizer_phone_entry.insert(0, "+1")

        # Password entry
        self.password_label = tkinter.Label(tab2_frame, text="Password:")
        self.configure_label(self.password_label)
        self.password_label.grid(row=4, column=0)
        self.organizer_password_entry = tkinter.Entry(tab2_frame, show="*")
        self.configure_entry(self.organizer_password_entry)
        self.organizer_password_entry.grid(row=4, column=1)

        #similar to user password validation
        # Password must be atleast 8 characters long
        # Password must contain atleast one digit
        # Password must contain atleast one uppercase letter
        # Password must contain atleast one lowercase letter
        # Special characters like $&@#%*

        # Password entry
        self.password_label6 = tkinter.Label(tab2_frame, text="Password must be atleast 8 characters long",font=("Helvetica", 8),fg="red")
        self.password_label6.grid(row=5, column=0, columnspan=2)

        self.password_label7 = tkinter.Label(tab2_frame, text="Password must contain atleast one digit",font=("Helvetica", 8),fg="red")
        self.password_label7.grid(row=6, column=0, columnspan=2)

        self.password_label8 = tkinter.Label(tab2_frame, text="Password must contain atleast one uppercase letter",font=("Helvetica", 8),fg="red")
        self.password_label8.grid(row=7, column=0, columnspan=2)

        self.password_label9 = tkinter.Label(tab2_frame, text="Password must contain atleast one lowercase letter",font=("Helvetica", 8),fg="red")
        self.password_label9.grid(row=8, column=0, columnspan=2)

        self.password_label10 = tkinter.Label(tab2_frame, text="Password must contain atleast one special character",font=("Helvetica", 8),fg="red")
        self.password_label10.grid(row=9, column=0, columnspan=2)

        # Check if passentry is 8 characters long
        self.organizer_password_entry.bind("<KeyRelease>", lambda event: self.password_validation(event))

        # Register button
        self.register_button = tkinter.Button(tab2_frame, text="Register", command=self.registerOrganizer)
        self.configure_button(self.register_button)
        self.register_button.grid(row=10, column=0, columnspan=2, pady=20)

        # Back button to return to the welcome page
        self.back_button = tkinter.Button(tab2_frame, text="Back to Welcome", command=self.show_welcome_page)
        self.configure_button(self.back_button)
        self.back_button.grid(row=11, column=0, columnspan=2, pady=10)

    #organizerdashboard
    def organizer_dashboard(self):
        self.tkn.geometry("1000x700")
        for widget in self.tkn.winfo_children():
            widget.destroy()

        # Add organizer dashboard elements
        label = tkinter.Label(self.tkn, text="Organizer Dashboard", font=("Helvetica", 20))
        label.configure(bg="white")
        label.pack(pady=10)

        #notebook for organizer dashboard
        #create tabs
        organizer_notebook = ttk.Notebook(self.tkn)

        #events tab
        self.events_tab = ttk.Frame(organizer_notebook,width=200, height=200)
        #font century gothic
        organizer_notebook.add(self.events_tab, text='Events',sticky="nsew")
        #configure the font to times
        self.style.configure('TNotebook.Tab', font=('Calibri', '14', 'bold'))        

        #create event tab
        create_event_tab = ttk.Frame(organizer_notebook,width=200, height=200)
        organizer_notebook.add(create_event_tab, text='Create Event',sticky="nsew")

        # #event rsvp details tab
        # event_rsvp_details_tab = ttk.Frame(organizer_notebook,width=200, height=200)
        # organizer_notebook.add(event_rsvp_details_tab, text='Event RSVP Details',sticky="nsew")

        #pack the notebook
        organizer_notebook.pack(expand=1, fill='both')

        #tab text and position to center
        organizer_notebook.tab(0, text="Events",compound=tkinter.CENTER)
        organizer_notebook.tab(1, text="Create Event",compound=tkinter.CENTER)
        # organizer_notebook.tab(2, text="Event RSVP Details",compound=tkinter.CENTER)

        #events tab
        #display images of events in the events tab
        #display the image in images/welcome.jpg 900x600
        #create canvas for the images to display
        self.organzier_events_canvas = tkinter.Canvas(self.events_tab)
        self.organzier_events_canvas.pack(expand=True, fill='both')

        #create scrollbar for the canvas
        organizer_events_scrollbar = ttk.Scrollbar(self.events_tab, orient='vertical', command=self.organzier_events_canvas.yview)
        organizer_events_scrollbar.pack(side=tkinter.RIGHT, fill='y')
        #extend the scrollbar to the while frame
        self.organzier_events_canvas.configure(yscrollcommand=organizer_events_scrollbar.set)

        #configure the canvas
        self.organzier_events_canvas.configure(yscrollcommand=organizer_events_scrollbar.set)
        self.organzier_events_canvas.bind('<Configure>', lambda e: self.organzier_events_canvas.configure(scrollregion=self.organzier_events_canvas.bbox("all")))

        #create another frame inside the canvas
        organizer_events_frame = tkinter.Frame(self.organzier_events_canvas)
        self.organzier_events_canvas.create_window((0,0), window=organizer_events_frame, anchor="nw")

        #display the images in the frame
        self.display_events(organizer_events_frame)


        #create event tab
        # create frame for the create event tab
        create_event_frame = tkinter.Frame(create_event_tab)
        create_event_frame.pack(expand=True, fill='both',anchor="center")

        # create two sections in the frame
        event_details_frame = tkinter.Frame(create_event_frame)
        event_details_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        event_images_frame = tkinter.Frame(create_event_frame)
        event_images_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # take event details from the organizer
        # Event Name label and entry side by side
        self.event_name_label = tkinter.Label(event_details_frame, text="Event Name:")
        self.configure_label(self.event_name_label)
        self.event_name_label.grid(row=0, column=0, pady=10,padx=30,sticky="w")
        self.event_name_entry = tkinter.Entry(event_details_frame)
        self.configure_entry(self.event_name_entry)
        self.event_name_entry.grid(row=0, column=1, pady=10,sticky="w",padx=30)

        # Event Date label and entry side by side
        self.event_date_label = tkinter.Label(event_details_frame, text="Event Date: MM/DD/YYYY")
        self.configure_label(self.event_date_label)
        self.event_date_label.grid(row=1, column=0, pady=10,sticky="w",padx=30)
        self.event_date_entry = DateEntry(event_details_frame, width=13, background="darkblue", foreground="white", date_pattern="MM/dd/yyyy", font=("Arial", 15))
        #dateentry width and height
        # self.configure_entry(self.event_date_entry)
        self.event_date_entry.grid(row=1, column=1, pady=10,sticky="w",padx=30)

        # Event Time label and entry side by side
        self.event_time_label = tkinter.Label(event_details_frame, text="Event Time: HH:MM AM/PM")
        self.configure_label(self.event_time_label)
        self.event_time_label.grid(row=2, column=0, pady=10,sticky="w",padx=30)
        self.event_time_entry = tkinter.Entry(event_details_frame)
        self.configure_entry(self.event_time_entry)
        self.event_time_entry.grid(row=2, column=1, pady=10,sticky="w",padx=30)

        # Event Location label and entry side by side
        self.event_location_label = tkinter.Label(event_details_frame, text="Event Location:")
        self.configure_label(self.event_location_label)
        self.event_location_label.grid(row=3, column=0, pady=10,sticky="w",padx=30)
        self.event_location_entry = tkinter.Entry(event_details_frame)
        self.configure_entry(self.event_location_entry)
        self.event_location_entry.grid(row=3, column=1, pady=10,sticky="w",padx=30)

        # Event Description label and entry side by side
        self.event_description_label = tkinter.Label(event_details_frame, text="Event Description:")
        self.configure_label(self.event_description_label)
        self.event_description_label.grid(row=4, column=0, pady=10,sticky="w",padx=30)
        self.event_description_entry = tkinter.Entry(event_details_frame)
        self.configure_entry(self.event_description_entry)
        self.event_description_entry.grid(row=4, column=1, pady=10,sticky="w",padx=30)
        # Event Description entry height increase


        # sbmit button
        self.submit_button = tkinter.Button(create_event_frame, text="Submit", command=self.registerEvent)
        self.configure_button(self.submit_button)
        #packm bottom center
        self.submit_button.grid(row=1, column=0, pady=10,sticky="nsew",padx=30)

        # create a canvas for the event images upload by the organizer in column 3
        # create canvas for the images to display
        self.organzier_create_events_canvas = tkinter.Canvas(event_images_frame)
        self.organzier_create_events_canvas.pack(expand=True, fill='both')

        # frame for the canvas
        organizer_events_frame = tkinter.Frame(self.organzier_create_events_canvas)
        self.organzier_create_events_canvas.create_window((0, 0), window=organizer_events_frame, anchor="nw")

        # upload button end of column 3
        self.upload_button = tkinter.Button(event_images_frame, text="Upload Event Image", command=self.uploadEventImage)
        self.configure_button(self.upload_button)
        self.upload_button.pack(pady=10)


        logout_button = tkinter.Button(self.tkn, text="Logout", command=self.show_welcome_page)
        self.configure_button(logout_button)
        logout_button.pack(pady=10)


    #org_show_event_rsvp_details_page
    def org_show_event_rsvp_details_page(self):
        
        #get values of the selected row
        selected_row = self.org_event_tree.focus()
        org_page_current_event = list(self.org_event_tree.item(selected_row, 'values'))



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

        print(org_page_current_event)

        #get users id that are registered to the event and then get their details
        # Connect to the MySQL database
        with self.database.cursor() as cursor:
                # Query the event table in MySQL to get the eventID based on eventName
                cursor.execute("SELECT eventID FROM eventhub.event WHERE eventID=%s", (org_page_current_event[0],))
                event_id = cursor.fetchone()
                print(event_id)
    
                if event_id:
                    # Query the eventRegistration table in MySQL to get userID associated with the event
                    cursor.execute("SELECT userID FROM eventhub.eventRegistration WHERE eventID=%s", (event_id[0],))
                    user_ids = cursor.fetchall()
                else:
                    user_ids = []
                
                cursor.close()
            
        print(user_ids)
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
        self.configure_button(self.back_button)
        self.back_button.configure(width=30)
        self.back_button.pack(pady=10)






        

        
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

        self.tkn.geometry("1000x700")
        for widget in self.tkn.winfo_children():
            widget.destroy()

        # Add admin dashboard elements
        label = tkinter.Label(self.tkn, text="Admin Dashboard", font=("Helvetica", 20))

        label.configure(bg="white")
        label.pack(pady=20)

        #notebook for admin dashboard

        #create tabs
        self.admin_notebook = ttk.Notebook(self.tkn)

        #Events reports tab
        self.events_reports_tab = ttk.Frame(self.admin_notebook,width=200, height=200)
        #font century gothic
        self.admin_notebook.add(self.events_reports_tab, text='Events Reports',sticky="nsew")
        #configure the font to times
        self.style.configure('TNotebook.Tab', font=('Calibri', '14', 'bold'))

        #Users reports tab
        users_reports_tab = ttk.Frame(self.admin_notebook,width=200, height=200)
        self.admin_notebook.add(users_reports_tab, text='Users Reports',sticky="nsew")

        #Organizers reports tab
        organizers_reports_tab = ttk.Frame(self.admin_notebook,width=200, height=200)
        self.admin_notebook.add(organizers_reports_tab, text='Organizers Reports',sticky="nsew")


        #pack the notebook
        self.admin_notebook.pack(expand=1, fill='both')

        #tab text and position to center
        self.admin_notebook.tab(0, text="Events Reports",compound=tkinter.CENTER)
        self.admin_notebook.tab(1, text="Users Reports",compound=tkinter.CENTER)
        self.admin_notebook.tab(2, text="Organizers Reports",compound=tkinter.CENTER)

        #events reports tab
        # create treeview for the events reports tab
        self.events_tree = ttk.Treeview(self.events_reports_tab, columns=(
            "Event Name", "Event Date", "Event Time", "Event Location", "Event Description","Registered Count"), show="headings")
        self.events_tree.heading("#1", text="Event Name")
        self.events_tree.column("#1", width=150)
        self.events_tree.heading("#2", text="Event Date")
        self.events_tree.column("#2", width=150)
        self.events_tree.heading("#3", text="Event Time")
        self.events_tree.column("#3", width=150)
        self.events_tree.heading("#4", text="Event Location")
        self.events_tree.column("#4", width=150)
        self.events_tree.heading("#5", text="Event Description")
        self.events_tree.column("#5", width=150)
        self.events_tree.heading("#6", text="Registered Count")
        self.events_tree.column("#6", width=150)

        # Populate the Treeview with events
        # Connect to the MySQL database
        with self.database.cursor() as cursor:
            # Retrieve all events from the event table in MySQL 
            cursor.execute("SELECT * FROM eventhub.event")
            events = cursor.fetchall()
            cursor.close()

        # Populate the Treeview with events 
        for event in events:
            #insert all columns except eventimage
            self.events_tree.insert("", "end", values=event[2:7] +event[8:9])

        # Pack the Treeview widget
        self.events_tree.pack()

        #users registered to the event detials button
        self.event_rsvp_details_button = tkinter.Button(self.events_reports_tab, text="Event RSVP Details", command=self.admin_event_rsvp_details_page)
        self.configure_button(self.event_rsvp_details_button)
        self.event_rsvp_details_button.pack(pady=10)


        #print events reports tab
        print_events_button = tkinter.Button(self.events_reports_tab, text="Print Events Report", command=self.events_report_pdf)
        self.configure_button(print_events_button)
        print_events_button.pack(pady=10)


        #users reports tab
        # create treeview for the users reports tab
        self.users_tree = ttk.Treeview(users_reports_tab, columns=(
            "User Name", "User Email", "User Phone"), show="headings")
        self.users_tree.heading("#1", text="User Name")
        self.users_tree.column("#1", width=150)
        self.users_tree.heading("#2", text="User Email")
        self.users_tree.column("#2", width=250)
        self.users_tree.heading("#3", text="User Phone")
        self.users_tree.column("#3", width=150, anchor="center")

        # Populate the Treeview with users
        # Connect to the MySQL database
        with self.database.cursor() as cursor:
            # Retrieve all users from the user table in MySQL
            cursor.execute("SELECT * FROM eventhub.user")
            users = cursor.fetchall()
            cursor.close()

        # Populate the Treeview with users
        for user in users:
            #insert all columns except userID and password
            user_name = user[1] + " " + user[2]
            user_email = user[3]
            user_phone = user[4]
            self.users_tree.insert("", "end", values=(user_name, user_email, user_phone))

        # Pack the Treeview widget
        self.users_tree.pack()

        #print users reports tab
        print_users_button = tkinter.Button(users_reports_tab, text="Print Users Report", command=self.users_report_pdf)
        self.configure_button(print_users_button)
        print_users_button.pack(pady=10)


        #organizers reports tab
        # create treeview for the organizers reports tab
        self.organizers_tree = ttk.Treeview(organizers_reports_tab, columns=(
            "Organizer Name", "Organization Name", "Organizer Email", "Organizer Phone"), show="headings")
        self.organizers_tree.heading("#1", text="Organizer Name")
        self.organizers_tree.column("#1", width=150)
        self.organizers_tree.heading("#2", text="Organization Name")
        self.organizers_tree.column("#2", width=250)
        self.organizers_tree.heading("#3", text="Organizer Email")
        self.organizers_tree.column("#3", width=250)
        self.organizers_tree.heading("#4", text="Organizer Phone")
        self.organizers_tree.column("#4", width=150, anchor="center")

        # Populate the Treeview with organizers
        # Connect to the MySQL database
        with self.database.cursor() as cursor:
            # Retrieve all organizers from the organizer table in MySQL
            cursor.execute("SELECT * FROM eventhub.organizer")
            organizers = cursor.fetchall()
            cursor.close()

        # Populate the Treeview with organizers
        for organizer in organizers:
            #insert all columns except organizerID and password
            organizer_name = organizer[1]
            organization_name = organizer[2]
            organizer_email = organizer[4]
            organizer_phone = organizer[3]
            self.organizers_tree.insert("", "end", values=(organizer_name, organization_name, organizer_email, organizer_phone))

        # Pack the Treeview widget
        self.organizers_tree.pack()

        #print organizers reports tab
        print_organizers_button = tkinter.Button(organizers_reports_tab, text="Print Organizers Report", command=self.organizers_report_pdf)
        self.configure_button(print_organizers_button)
        print_organizers_button.pack(pady=10)


        logout_button = tkinter.Button(self.tkn, text="Logout", command=self.show_welcome_page)
        self.configure_button(logout_button)
        logout_button.pack(pady=10)

    #admin_event_rsvp_details_page
    def admin_event_rsvp_details_page(self):
        #clear events reports tab
        selected_row = self.events_tree.focus()
        admin_page_current_event = list(self.events_tree.item(selected_row, 'values'))

        print(selected_row)

        for widget in self.events_reports_tab.winfo_children():
            widget.destroy()

        #Event RSVP Details Page
        #get selected row

        #display event name
        label = tkinter.Label(self.events_reports_tab, text="Event Name: "+admin_page_current_event[0], font=("Helvetica", 20))
        label.configure(bg="white")
        label.pack(pady=20)

        #treeview of users registered to that particular event
        # Create a Treeview widget to display events
        event_tree = ttk.Treeview(self.events_reports_tab, columns=(
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
            cursor.execute("SELECT eventID FROM eventhub.event WHERE eventName=%s", (admin_page_current_event[0],))
            event_id = cursor.fetchone()
            print(event_id)

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

        # Pack the Treeview widget 
        event_tree.pack()

        #back to admin dashboard button
        self.back_button = tkinter.Button(self.events_reports_tab, text="Back to Admin Dashboard", command=self.admin_dashboard)
        self.configure_button(self.back_button)
        self.back_button.configure(width=30)
        self.back_button.pack(pady=10)



    def user_dashboard(self):
        for widget in self.tkn.winfo_children():
            widget.destroy()

        #geometry of the window
        self.tkn.geometry("1000x700")

        # Add user dashboard elements
        label = tkinter.Label(self.tkn, text="User Dashboard", font=("Helvetica", 20))
        label.configure(bg="white")
        label.pack(pady=20)

        #notebook for user dashboard
        #create tabs
        self.user_notebook = ttk.Notebook(self.tkn)


        
        #All Events tab
        all_events_tab = ttk.Frame(self.user_notebook,width=200, height=200)
        #font century gothic
        self.user_notebook.add(all_events_tab, text='All Events',sticky="nsew")
        #configure the font to times
        self.style.configure('TNotebook.Tab', font=('Calibri', '14', 'bold'))

        #My Events tab
        my_events_tab = ttk.Frame(self.user_notebook,width=200, height=200)
        self.user_notebook.add(my_events_tab, text='My Events',sticky="nsew")
        #pack the notebook
        self.user_notebook.pack(expand=1, fill='both')

        #all events tab
        # create canvas for the images to display
        self.user_all_events_canvas = tkinter.Canvas(all_events_tab)
        self.user_all_events_canvas.pack(expand=True, fill='both')

        #create scrollbar for the canvas
        user_all_events_scrollbar = ttk.Scrollbar(all_events_tab, orient='vertical', command=self.user_all_events_canvas.yview)
        user_all_events_scrollbar.pack(side=tkinter.RIGHT, fill='y')
        #extend the scrollbar to the total frame

        #configure the canvas
        self.user_all_events_canvas.configure(yscrollcommand=user_all_events_scrollbar.set)
        self.user_all_events_canvas.bind('<Configure>', lambda e: self.user_all_events_canvas.configure(scrollregion=self.user_all_events_canvas.bbox("all")))

        #create another frame inside the canvas
        user_all_events_frame = tkinter.Frame(self.user_all_events_canvas)
        self.user_all_events_canvas.create_window((0,0), window=user_all_events_frame, anchor="nw")

        #display the images in the frame
        self.display_events(user_all_events_frame)

        #my events tab
        # create canvas for the images to display
        self.user_my_events_canvas = tkinter.Canvas(my_events_tab)
        self.user_my_events_canvas.pack(expand=True, fill='both')

        #create scrollbar for the canvas
        user_my_events_scrollbar = ttk.Scrollbar(my_events_tab, orient='vertical', command=self.user_my_events_canvas.yview)
        user_my_events_scrollbar.pack(side=tkinter.RIGHT, fill='y')

        #configure the canvas
        self.user_my_events_canvas.configure(yscrollcommand=user_my_events_scrollbar.set)
        self.user_my_events_canvas.bind('<Configure>', lambda e: self.user_my_events_canvas.configure(scrollregion=self.user_my_events_canvas.bbox("all")))

        #create another frame inside the canvas
        user_my_events_frame = tkinter.Frame(self.user_my_events_canvas)
        self.user_my_events_canvas.create_window((0,0), window=user_my_events_frame, anchor="nw")

        #display the images in the frame
        self.display_events(user_my_events_frame,self.current_user_object)

        #feedback tab
        feedback_tab = ttk.Frame(self.user_notebook,width=200, height=200)
        self.user_notebook.add(feedback_tab, text='Feedback',sticky="nsew")

        #pack the notebook
        self.user_notebook.pack(expand=1, fill='both')

        #feedback tab
        # create canvas for the images to display
        self.user_feedback_canvas = tkinter.Canvas(feedback_tab)
        self.user_feedback_canvas.pack(expand=True, fill='both')

        #create scrollbar for the canvas
        user_feedback_scrollbar = ttk.Scrollbar(feedback_tab, orient='vertical', command=self.user_feedback_canvas.yview)
        user_feedback_scrollbar.pack(side=tkinter.RIGHT, fill='y')

        #configure the canvas
        self.user_feedback_canvas.configure(yscrollcommand=user_feedback_scrollbar.set)
        self.user_feedback_canvas.bind('<Configure>', lambda e: self.user_feedback_canvas.configure(scrollregion=self.user_feedback_canvas.bbox("all")))

        #create another frame inside the canvas
        user_feedback_frame = tkinter.Frame(self.user_feedback_canvas)
        self.user_feedback_canvas.create_window((0,0), window=user_feedback_frame, anchor="nw")

        #display the images in the frame
        self.display_events(user_feedback_frame,self.current_user_object,True)
        



        #logout button
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

        #my events tab
        # create canvas for the images to display
        self.user_my_events_canvas = tkinter.Canvas(self.tkn)
        self.user_my_events_canvas.grid(row=4, column=0, columnspan=3, padx=30,pady=10,sticky="nsew")

        #create scrollbar for the canvas
        user_my_events_scrollbar = ttk.Scrollbar(self.tkn, orient='vertical', command=self.user_my_events_canvas.yview)
        user_my_events_scrollbar.grid(row=4, column=3, sticky="ns")

        #configure the canvas
        self.user_my_events_canvas.configure(yscrollcommand=user_my_events_scrollbar.set)
        self.user_my_events_canvas.bind('<Configure>', lambda e: self.user_my_events_canvas.configure(scrollregion=self.user_my_events_canvas.bbox("all")))

        #create another frame inside the canvas
        user_my_events_frame = tkinter.Frame(self.user_my_events_canvas)
        self.user_my_events_canvas.create_window((0,0), window=user_my_events_frame, anchor="nw")

        #display the images in the frame
        self.display_events(user_my_events_frame,self.current_user_object)


        # Back button to return to the main page
        back_button = tkinter.Button(self.tkn, text="Logout", command=self.show_main_page)
        self.configure_button(back_button)
        back_button.grid(row=3, column=2, pady=10)



    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    #password_validation
    def password_validation(self,event):

       
        #get current tab from  tab_control = ttk.Notebook(self.tkn)
        self.current_tab = self.tab_control.tab(self.tab_control.select(), "text")


        #check register tab 
        if self.current_tab == "Register as User":
            password = self.user_password_entry.get()

                    #check if 8 characters
            if len(password) >= 8:
                #change the self.password_label to green'
                self.password_label0.config(fg="green")
            
            #atleast one uppercase
            if re.search("[A-Z]", password):
                #change the self.password_label to green'
                self.password_label2.config(fg="green")
            
            #atleast one lowercase
            if re.search("[a-z]", password):
                #change the self.password_label to green'
                self.password_label3.config(fg="green")

            #atleast one digit
            if re.search("[0-9]", password):
                #change the self.password_label to green'
                self.password_label1.config(fg="green")

            #atleast one special character
            if re.search("[!@#$%^&*]", password):
                #change the self.password_label to green'
                self.password_label4.config(fg="green")

            #if all conditions are met
            #remove the password validation labels
            if len(password) >= 8 and re.search("[A-Z]", password) and re.search("[a-z]", password) and re.search("[0-9]", password) and re.search("[!@#$%^&*]", password):
                self.password_label0.destroy()
                self.password_label1.destroy()
                self.password_label2.destroy()
                self.password_label3.destroy()
                self.password_label4.destroy()
            
        elif self.current_tab == "Register as Organizer":
            password = self.organizer_password_entry.get()

            #similar to user password validation
            #check if 8 characters
            if len(password) >= 8:
                #change the self.password_label to green'
                self.password_label6.config(fg="green")

            #atleast one uppercase
            if re.search("[A-Z]", password):
                #change the self.password_label to green'
                self.password_label7.config(fg="green")

            #atleast one lowercase
            if re.search("[a-z]", password):
                #change the self.password_label to green'
                self.password_label8.config(fg="green") 
            
            #atleast one digit
            if re.search("[0-9]", password):
                #change the self.password_label to green'
                self.password_label9.config(fg="green")

            #atleast one special character
            if re.search("[!@#$%^&*]", password):
                #change the self.password_label to green'
                self.password_label10.config(fg="green")

            #if all conditions are met
            #remove the password validation labels  
            if len(password) >= 8 and re.search("[A-Z]", password) and re.search("[a-z]", password) and re.search("[0-9]", password) and re.search("[!@#$%^&*]", password):
                self.password_label6.destroy()
                self.password_label7.destroy()
                self.password_label8.destroy()
                self.password_label9.destroy()
                self.password_label10.destroy()

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            


            



        

        

    #unregister_for_event
    def unregister_for_event(self):
        #get values of the selected row
        selected_event = self.current_event

        #delete the event from the database
        with self.database.cursor() as cursor:
            #delete the event from the eventRegistration table
            cursor.execute("DELETE FROM eventhub.eventRegistration WHERE eventID=%s AND userID=%s", (selected_event[0],self.current_user_object[0],))
            #reduced the registered count by 1
            cursor.execute("UPDATE eventhub.event SET registeredCount=registeredCount-1 WHERE eventID=%s", (selected_event[0],))

            self.database.commit()

            cursor.close()

        #display the events page
        self.user_dashboard()

    #delete_event
    def delete_event(self):
        #current event
        selectedevent = self.current_event

        #delete all the registrations of the event from the eventRegistration table
        with self.database.cursor() as cursor:
            cursor.execute("DELETE FROM eventhub.eventRegistration WHERE eventID=%s", (selectedevent[0],))
            self.database.commit()
            cursor.close()


        #delete the event from the database
        with self.database.cursor() as cursor:
            #delete the event from the event table
            cursor.execute("DELETE FROM eventhub.event WHERE eventID=%s", (selectedevent[0],))
            self.database.commit()

            #delete the event from the eventRegistration table
            cursor.execute("DELETE FROM eventhub.eventRegistration WHERE eventID=%s", (selectedevent[0],))
            self.database.commit()

            cursor.close()

        #display the events page
        self.organizer_dashboard()
    #uploadEventImage
    def uploadEventImage(self,update=False):
        #get the event name
        event_name = self.event_name_entry.get()

        #get the image file
        self.current_image_path = filedialog.askopenfilename(initialdir="/", title="Select a File", filetypes=(("jpg files", "*.jpg"), ("png files", "*.png"), ("all files", "*.*")))

        #get the image name
        image_name = self.current_image_path.split("/")[-1]

        #get the image extension
        image_extension = image_name.split(".")[-1]

        #check if the image is jpg or png
        if image_extension not in ["jpg","png,""JPG","PNG","jpeg","JPEG"]:
            messagebox.showerror("Error", "Please upload a jpg or png file")
            return

        #display the image in the organzier_create_events_canvas
        event_image = Image.open(self.current_image_path)
        event_image = event_image.resize((200, 300), Image.LANCZOS)
        event_image = ImageTk.PhotoImage(event_image)

        if update:
            #delete the previous image
            #clear the frame event_image_frame
            for widget in self.event_image_frame.winfo_children():
                widget.destroy()

            #display image there
            event_image_label = tkinter.Label(self.event_image_frame, image=event_image)
            event_image_label.image = event_image
            event_image_label.pack()

        else:
            #create a label to display the image
            event_image_label = tkinter.Label(self.organzier_create_events_canvas, image=event_image)
            event_image_label.image = event_image
            event_image_label.pack()

        #update the upload event image button to uploaded 
        self.upload_button.configure(text="Uploaded")


    #display_orgainzer_events
    def display_events(self,frame,current_user_object=None,feedback=False):
        # Connect to the MySQL database
        # print("display events")
        print(self.user_type)
        events=[]
        if self.user_type == "organizer":
            with self.database.cursor() as cursor:
                # Retrieve event data from the 'event' table in MySQL
                cursor.execute("SELECT * FROM eventhub.event WHERE organizerID=%s", (self.current_user_object[0],))
                events = cursor.fetchall()
        elif current_user_object:
            with self.database.cursor() as cursor:
                #retrieve the event ids of the events registered by the user
                cursor.execute("SELECT eventID FROM eventhub.eventRegistration WHERE userID=%s", (self.current_user_object[0],))
                event_ids = cursor.fetchall()
                for event_id in event_ids:
                    #retrieve the event details of the events registered by the user
                    cursor.execute("SELECT * FROM eventhub.event WHERE eventID=%s", (event_id[0],))
                    event = cursor.fetchone()
                    events.append(event)
        else:
            with self.database.cursor() as cursor:
                # Retrieve event data from the 'event' table in MySQL
                cursor.execute("SELECT * FROM eventhub.event")
                events = cursor.fetchall()
        
        print(events)

        for i, event in enumerate(events):
            # print(event)
            eventdetails = event[1:7]
            displayImage=Image.open(event[7])
            displayImage=displayImage.resize((200,250),Image.LANCZOS)
            displayImage=ImageTk.PhotoImage(displayImage)
            if feedback:
                eventdetails_button = tkinter.Button(frame, image=displayImage,compound=tkinter.TOP,command=lambda event=event: self.show_event_feedback_page(event,frame))
            else:
                eventdetails_button = tkinter.Button(frame, image=displayImage,compound=tkinter.TOP,command=lambda event=event: self.show_event_details_page(event,frame))
            eventdetails_button.image = displayImage

            if self.user_type == "organizer":
                eventdetails_button.configure(text=str(event[8])+" User Registered")

            eventdetails_button.grid(row=i//4, column=i%4, padx=10, pady=10)

    #show_event_feedback_page
    def show_event_feedback_page(self,event,frame):
        # clear the frame
        for widget in frame.winfo_children():
            widget.destroy()

        # display the event details
        eventdetails = event
        displayImage = Image.open(event[7])
        displayImage = displayImage.resize((200, 250), Image.LANCZOS)
        displayImage = ImageTk.PhotoImage(displayImage)
        image_label = tkinter.Label(frame, image=displayImage)
        image_label.image = displayImage
        image_label.grid(row=0, column=0, padx=10, pady=10)

        # print(eventdetails)

        self.current_event = eventdetails


        #display event name
        


        # frame from column 1
        eventdetails_frame = tkinter.Frame(frame)
        eventdetails_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        event_name_label = tkinter.Label(eventdetails_frame, text="Event Name: " + str(eventdetails[2]))
        self.configure_label(event_name_label)
        event_name_label.grid(row=0, column=0, pady=10, padx=30, sticky="w")

        #feedback label
        feedback_label = tkinter.Label(eventdetails_frame, text="Feedback")
        self.configure_label(feedback_label)
        feedback_label.grid(row=1, column=0, pady=10, sticky="w", padx=30)

        #combobox for feedback
        self.feedback_combobox = ttk.Combobox(eventdetails_frame, values=["Good","Average","Bad"])
        self.feedback_combobox.grid(row=1, column=1, pady=10, sticky="w", padx=30)


        #additonal comments label
        additional_comments_label = tkinter.Label(eventdetails_frame, text="Additional Comments")
        self.configure_label(additional_comments_label)
        additional_comments_label.grid(row=2, column=0, pady=10, sticky="w", padx=30)


        #feedback entry
        self.feedback_entry = tkinter.Entry(eventdetails_frame)
        self.configure_entry(self.feedback_entry)
        self.feedback_entry.grid(row=2, column=1, pady=10, sticky="w", padx=30)

        #feedback submit button
        self.feedback_submit_button = tkinter.Button(eventdetails_frame, text="Submit", command=self.submit_feedback)
        self.configure_button(self.feedback_submit_button)
        self.feedback_submit_button.grid(row=3, column=0, pady=10, sticky="w", padx=30)

        #back to user dashboard button
        self.back_button = tkinter.Button(eventdetails_frame, text="Back to User Dashboard", command=self.user_dashboard)
        self.configure_button(self.back_button)
        #deep bottom center
        self.back_button.grid(row=4, column=0, pady=10,sticky="w",padx=30)
        #configure button width
        self.back_button.configure(width=30)



    #update_event_details
    def update_event_details(self,frame,event):
        #clear frame  
        for widget in frame.winfo_children():
            widget.destroy()

        #display event name
        label = tkinter.Label(frame, text="Update Event Details", font=("Helvetica", 20))
        label.configure(bg="white")
        label.grid(row=0, column=0, columnspan=2, pady=20)

        #display event image frame to right
        self.event_image_frame = tkinter.Frame(frame)
        self.event_image_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        #display event image
        displayImage = Image.open(event[7])
        displayImage = displayImage.resize((200, 250), Image.LANCZOS)
        displayImage = ImageTk.PhotoImage(displayImage)
        image_label = tkinter.Label(self.event_image_frame, image=displayImage)
        image_label.image = displayImage
        image_label.grid(row=0, column=0, padx=10, pady=10)

        #change image button to upload new image    
        self.upload_button = tkinter.Button(self.event_image_frame, text="Upload Event Image", command=lambda: self.uploadEventImage(True))
        self.configure_button(self.upload_button)
        self.upload_button.grid(row=1, column=0, pady=10, sticky="w", padx=30)
        #width of the button
        self.upload_button.configure(width=30)

        #frame from column 1
        eventdetails_frame = tkinter.Frame(frame)
        eventdetails_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Event Name label and entry filled with details to updated 
        self.event_name_label = tkinter.Label(eventdetails_frame, text="Event Name: ")
        self.configure_label(self.event_name_label)
        self.event_name_label.grid(row=0, column=0, pady=10, padx=30, sticky="w")

        self.event_name_entry = tkinter.Entry(eventdetails_frame)
        self.configure_entry(self.event_name_entry)
        self.event_name_entry.grid(row=0, column=1, pady=10, sticky="w", padx=30)

        # Event Date label and entry filled with details to updated
        self.event_date_label = tkinter.Label(eventdetails_frame, text="Event Date: ")
        self.configure_label(self.event_date_label)
        self.event_date_label.grid(row=1, column=0, pady=10, sticky="w", padx=30)

        self.event_date_entry = DateEntry(eventdetails_frame)
        self.event_date_entry.grid(row=1, column=1, pady=10, sticky="w", padx=30)

        # Event Time label and entry filled with details to updated
        self.event_time_label = tkinter.Label(eventdetails_frame, text="Event Time: ")
        self.configure_label(self.event_time_label)
        self.event_time_label.grid(row=2, column=0, pady=10, sticky="w", padx=30)

        self.event_time_entry = tkinter.Entry(eventdetails_frame)
        self.configure_entry(self.event_time_entry)
        self.event_time_entry.grid(row=2, column=1, pady=10, sticky="w", padx=30)

        # Event Location label and entry filled with details to updated
        self.event_location_label = tkinter.Label(eventdetails_frame, text="Event Location: ")
        self.configure_label(self.event_location_label)
        self.event_location_label.grid(row=3, column=0, pady=10, sticky="w", padx=30)

        self.event_location_entry = tkinter.Entry(eventdetails_frame)
        self.configure_entry(self.event_location_entry)
        self.event_location_entry.grid(row=3, column=1, pady=10, sticky="w", padx=30)

        # Event Description label and entry filled with details to updated
        self.event_description_label = tkinter.Label(eventdetails_frame, text="Event Description: ")
        self.configure_label(self.event_description_label)
        self.event_description_label.grid(row=4, column=0, pady=10, sticky="w", padx=30)

        self.event_description_entry = tkinter.Entry(eventdetails_frame)
        self.configure_entry(self.event_description_entry)
        self.event_description_entry.grid(row=4, column=1, pady=10, sticky="w", padx=30)

        #fill the entry with the current event details
        self.event_name_entry.insert(0,event[2])
        #set date from the details
        self.event_date_entry.set_date(event[3])
        self.event_time_entry.insert(0,event[4])
        self.event_location_entry.insert(0,event[5])
        self.event_description_entry.insert(0,event[6])

        #update event button
        self.update_event_button = tkinter.Button(eventdetails_frame, text="Update Event", command=self.update_event)
        self.configure_button(self.update_event_button)
        self.update_event_button.grid(row=5, column=0, pady=10, sticky="w", padx=30)
        #width of the button
        self.update_event_button.configure(width=30)

        #back to organizer dashboard show event details button
        self.back_button = tkinter.Button(eventdetails_frame, text="Back to Organizer Dashboard", command=self.organizer_dashboard)
        self.configure_button(self.back_button)
        #deep bottom center
        self.back_button.grid(row=6, column=0, pady=10,sticky="w",padx=30)
        #configure button width
        self.back_button.configure(width=30)

    #update_event
    def update_event(self):
        #get the event details
        event_name = self.event_name_entry.get()
        event_date = self.event_date_entry.get()
        event_date = datetime.strptime(event_date, '%m/%d/%y').date()
        event_time = self.event_time_entry.get()
        event_location = self.event_location_entry.get()
        event_description = self.event_description_entry.get()
        image_path =""
        try:
            image_path = self.current_image_path
        except:
            pass

        #check if all the fields are filled
        if event_name == "" or event_date == "" or event_time == "" or event_location == "" or event_description == "":
            messagebox.showerror("Error", "Please fill all the fields")
            return

        #get the event id
        event_id = self.current_event[0]

        if image_path == "":
            image_path = self.current_event[7]
        #update the event details in the database with path too
        with self.database.cursor() as cursor:
            cursor.execute("UPDATE eventhub.event SET eventName=%s,eventDate=%s,eventTime=%s,eventLocation=%s,eventDescription=%s,eventImage=%s WHERE eventID=%s", (event_name,event_date,event_time,event_location,event_description,image_path,event_id,))
            self.database.commit()

            cursor.close()

        #update the event details in the current event
        self.current_event = (event_id,self.current_event[1],event_name,event_date,event_time,event_location,event_description,image_path,self.current_event[8])

        #event successfully updated
        messagebox.showinfo("Success", "Event Successfully Updated")


        #display the event details page
        self.show_event_details_page(self.current_event,self.organzier_events_canvas)


        


    #show_event_details_page
    def show_event_details_page(self, event, frame,feedback=False):
        # clear the frame
        for widget in frame.winfo_children():
            widget.destroy()

        # display the event details
        eventdetails = event
        displayImage = Image.open(event[7])
        displayImage = displayImage.resize((200, 250), Image.LANCZOS)
        displayImage = ImageTk.PhotoImage(displayImage)
        image_label = tkinter.Label(frame, image=displayImage)
        image_label.image = displayImage
        image_label.grid(row=0, column=0, padx=10, pady=10)

        # print(eventdetails)

        self.current_event = eventdetails

        # frame from column 1
        eventdetails_frame = tkinter.Frame(frame)
        eventdetails_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.event_name_label = tkinter.Label(eventdetails_frame, text="Event Name: " + str(eventdetails[2]))
        self.configure_label(self.event_name_label)
        self.event_name_label.grid(row=0, column=0, pady=10, padx=30, sticky="w")

        # Event Date label + event date
        self.event_date_label = tkinter.Label(eventdetails_frame, text="Event Date: " + str(eventdetails[3]))
        self.configure_label(self.event_date_label)
        self.event_date_label.grid(row=1, column=0, pady=10, sticky="w", padx=30)

        # Event Time label + event time
        self.event_time_label = tkinter.Label(eventdetails_frame, text="Event Time: " + str(eventdetails[4]))
        self.configure_label(self.event_time_label)
        self.event_time_label.grid(row=2, column=0, pady=10, sticky="w", padx=30)

        # Event Location label + event location
        self.event_location_label = tkinter.Label(eventdetails_frame, text="Event Location: " + str(eventdetails[5]))
        self.configure_label(self.event_location_label)
        self.event_location_label.grid(row=3, column=0, pady=10, sticky="w", padx=30)

        # Event Description label + event description
        self.event_description_label = tkinter.Label(eventdetails_frame, text="Event Description: " + str(eventdetails[6]))
        self.configure_label(self.event_description_label)
        self.event_description_label.grid(row=4, column=0, pady=10, sticky="w", padx=30)


        if self.user_type == "organizer":

            #update event dteails button
            self.update_event_button = tkinter.Button(eventdetails_frame, text="Update Event Details", command=lambda: self.update_event_details(frame,eventdetails))
            self.configure_button(self.update_event_button)
            self.update_event_button.grid(row=5, column=0, pady=10, sticky="w", padx=30)
            #width of the button    
            self.update_event_button.configure(width=30)
            #show registered users details button
            self.show_event_rsvp_details_button = tkinter.Button(eventdetails_frame, text="Show RSVP Details", command=self.show_event_rsvp_details_page)
            self.configure_button(self.show_event_rsvp_details_button)
            self.show_event_rsvp_details_button.grid(row=5, column=1, pady=10, sticky="w", padx=30)
            #width of the button
            self.show_event_rsvp_details_button.configure(width=30)

            #delete event button
            self.delete_event_button = tkinter.Button(eventdetails_frame, text="Delete Event", command=self.delete_event)
            self.configure_button(self.delete_event_button)
            self.delete_event_button.grid(row=6, column=0, pady=10, sticky="w", padx=30)
            #width of the button

            self.delete_event_button.configure(width=30)

        elif self.user_type == "user":
            # Register button to register for selected event
            #check if the user is already registered for the event
            with self.database.cursor() as cursor:
                # Retrieve event data from the 'event' table in MySQL
                cursor.execute("SELECT * FROM eventhub.eventRegistration WHERE userID=%s AND eventID=%s", (self.current_user_object[0],eventdetails[0]))
                event_registrations = cursor.fetchall()

            if not event_registrations:
                self.register_button = tkinter.Button(eventdetails_frame, text="Register", command=self.register_for_event)
                self.configure_button(self.register_button)
                self.register_button.grid(row=5, column=0, pady=10, sticky="w", padx=30)
                #width of the button
                self.register_button.configure(width=30)
            else:
                #unregister button
                self.unregister_button = tkinter.Button(eventdetails_frame, text="Unregister", command=self.unregister_for_event)
                self.configure_button(self.unregister_button)
                self.unregister_button.grid(row=5, column=0, pady=10, sticky="w", padx=30)
                #width of the button
                self.unregister_button.configure(width=30)




        if self.user_type == "organizer":
            #back to organizer dashboard button
            self.back_button = tkinter.Button(eventdetails_frame, text="Back to Organizer Dashboard", command=self.organizer_dashboard)
            self.configure_button(self.back_button)
            #deep bottom center
            self.back_button.grid(row=7, column=0, pady=10,sticky="w",padx=30)
            #configure button width
            self.back_button.configure(width=30)
        elif self.user_type == "user":
            
            # #feedbackpage button
            # self.feedback_button = tkinter.Button(eventdetails_frame, text="Feedback", command=self.show_event_details_page(eventdetails,frame,True))
            # self.configure_button(self.feedback_button)
            # #deep bottom center
            # self.feedback_button.grid(row=6, column=0, pady=10,sticky="w",padx=30)
            # #configure button width
            # self.feedback_button.configure(width=30)


            #back to user dashboard button
            self.back_button = tkinter.Button(eventdetails_frame, text="Back to User Dashboard", command=self.user_dashboard)
            self.configure_button(self.back_button)
            #deep bottom center
            self.back_button.grid(row=6, column=0, pady=10,sticky="w",padx=30)
            #configure button width
            self.back_button.configure(width=30)


    #show_event_rsvp_details_page
    def show_event_rsvp_details_page(self):
            
            page_current_event = self.current_event
            for widget in self.organzier_events_canvas.winfo_children():
                widget.destroy()
    
            #Event RSVP Details Page
            label = tkinter.Label(self.organzier_events_canvas, text="Users Registered to "+str(page_current_event[2]), font=("Helvetica", 20))
            label.configure(bg="white")
            label.pack(pady=20)
    
            #treeview of users registered to that particular event
            # Create a Treeview widget to display events
            event_tree = ttk.Treeview(self.organzier_events_canvas, columns=(
                "First Name", "Last Name", "Email","Phone"), show="headings")
            event_tree.heading("#1", text="First Name")
            event_tree.column("#1", width=150,anchor="center")
            event_tree.heading("#2", text="Last Name")
            event_tree.column("#2", width=150,anchor="center")
            event_tree.heading("#3", text="Email")
            event_tree.column("#3", width=150, anchor="center")
            event_tree.heading("#4", text="Phone")
            event_tree.column("#4", width=150, anchor="center")

            #treeview font size




            #increase the width of the treeview
            event_tree.column("#0", width=0, stretch=tkinter.NO)

    
            # print(page_current_event)
    
            #get users id that are registered to the event and then get their details
            # Connect to the MySQL database
            with self.database.cursor() as cursor:
                    # Query the event table in MySQL to get the eventID based on eventName
                    cursor.execute("SELECT eventID FROM eventhub.event WHERE eventID=%s", (page_current_event[0],))
                    event_id = cursor.fetchone()
                    print(event_id)
        
                    if event_id:
                        # Query the eventRegistration table in MySQL to get userID associated with the event
                        cursor.execute("SELECT userID FROM eventhub.eventRegistration WHERE eventID=%s", (event_id[0],))
                        user_ids = cursor.fetchall()
                    else:
                        user_ids = []
                    
                    cursor.close()
                
            print(user_ids)
            # Connect to the MySQL database
            with self.database.cursor() as cursor:
                    # Retrieve user data for the users registered to the event
                    users = []
                    for user_id in user_ids:
                        cursor.execute("SELECT * FROM eventhub.user WHERE userID=%s", user_id)
                        user_data = cursor.fetchone()
                        #append all info except userID and password
                        users.append(user_data[1:5])
    
                    cursor.close()
    
            # Populate the Treeview with users registered to the event
            #testing
            for user in users:
                event_tree.insert("", "end", values=user)

            event_tree.pack()

            #print this event users pdf button
            self.print_pdf_button = tkinter.Button(self.organzier_events_canvas, text="Print PDF of Users Registered", command=lambda event=page_current_event: self.print_event_users_pdf(users, page_current_event))
            self.configure_button(self.print_pdf_button)
            self.print_pdf_button.configure(width=30)
            self.print_pdf_button.pack(pady=10)


            #back to event details page button
            self.back_button = tkinter.Button(self.organzier_events_canvas, text="Back to Event Details Page", command=lambda event=page_current_event: self.show_event_details_page(event,self.organzier_events_canvas))
            self.configure_button(self.back_button)
            self.back_button.configure(width=30)
            self.back_button.pack(pady=10)

            #back to organizer dashboard button
            self.back_button = tkinter.Button(self.organzier_events_canvas, text="Back to Organizer Dashboard", command=self.organizer_dashboard)
            self.configure_button(self.back_button)
            self.back_button.configure(width=30)
            self.back_button.pack(pady=10)

            #show_event_details_page


    #submit_feedback
    def submit_feedback(self):
        #get the feedback
        feedback = self.feedback_entry.get()

        #combobox value
        feedback_value = self.feedback_combobox.get()
    

        #get the event id
        event_id = self.current_event[0]

        #get the user id
        user_id = self.current_user_object[0]

        #check if user has already submitted feedback
        with self.database.cursor() as cursor:
            cursor.execute("SELECT * FROM eventhub.eventfeedback WHERE eventID=%s AND userID=%s", (event_id,user_id,))
            feedbacks = cursor.fetchall()
            cursor.close()

        if feedbacks:
            messagebox.showerror("Error", "You have already submitted feedback for this event")
            return
        

        #insert the feedback into the database
        with self.database.cursor() as cursor:
            cursor.execute("INSERT INTO eventhub.eventfeedback(eventID,userID,rating,feedback) VALUES (%s,%s,%s,%s)", (event_id,user_id,feedback_value,feedback))
            self.database.commit()
            cursor.close()

        #show success message
        messagebox.showinfo("Success", "Feedback submitted successfully")

        #display the event details page
        self.user_dashboard()

        
    #print_event_users_pdf
    def print_event_users_pdf(self, users, event):

        # Create PDF
        pdf = FPDF(orientation='P')
        pdf.add_page()

        # Add a title to the page
        pdf.set_font("Arial", size=20)
        pdf.cell(200, 10, txt="Current Users Report", ln=1, align="C")

        # Add a header to the table
        pdf.set_font("Arial", size=12)
        pdf.cell(50, 10, txt="Name", border=1)
        pdf.cell(80, 10, txt="Email", border=1)
        pdf.cell(30, 10, txt="Phone", border=1)
        pdf.ln()

        # Add user data to the table
        for user in users:
            name = user[0] + " " + user[1]
            email = user[2]
            phone = user[3]

            pdf.cell(50, 10, txt=name)
            pdf.cell(80, 10, txt=email)
            pdf.cell(30, 10, txt=phone)

            pdf.ln()

        # Save PDF file name with event name
        pdf.output(event[2] + " Users.pdf")

        # Show success message
        messagebox.showinfo("Success", event[2]+" Users Report Generated Successfully")


       

    #show_organizer_events_page





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
        self.user_type = ""


        if self.current_email == "admin":
            self.admin_dashboard()
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
            if self.current_email == "user":
                self.user_dashboard()
                return
            
            if self.current_email != "laharireddy237@gmail.com":
                self.user_dashboard()
                return

            #send OTP to the user's email
            self.send_otp(self.current_email)

        elif organizer is not None:

            self.user_type = "organizer"
            self.current_user_object = organizer
            #testorganizer
            if self.current_email != "laharireddy237@gmail.com":
                self.organizer_dashboard()
                return
            #send OTP to the organizer's email
            self.send_otp(self.current_email)
        else:
            messagebox.showerror("Error", "User not found")

        self.otp_entry.configure(state="normal")
        self.login_button.configure(state="normal")


    #register_for_event
    def register_for_event(self):
        #current event details
        current_event = self.current_event
        #current user details
        current_user = self.current_user_object

        #check if the user is already registered for the event
        query = "SELECT * FROM eventhub.eventRegistration WHERE eventID = %s AND userID = %s"
        data = (current_event[0],current_user[0])
        try:
            self.cursor.execute(query, data)
            event = self.cursor.fetchone()
        except mysql.Error as err:
            messagebox.showerror("Error", f"MySQL Error: {err}")
            return
        
        if event is not None:
            messagebox.showerror("Error", "You are already registered for this event")
            return
        
        eventid = current_event[0]
        userid = current_user[0]
        organizerid = current_event[1]

        # Insert the user's input into the database
        query = "INSERT INTO eventhub.eventRegistration(eventID, userID, organizerID) VALUES (%s, %s, %s)"
        data = (eventid, userid, organizerid)

        try:
            self.cursor.execute(query, data)
            self.database.commit()
            messagebox.showinfo("Success", "You have registered successfully!")

            #increment the registered count of the event
            query = "UPDATE eventhub.event SET registeredCount = registeredCount + 1 WHERE eventID = %s"
            data = (current_event[0],)

            try:
                self.cursor.execute(query, data)
                self.database.commit()
            except mysql.Error as err:
                messagebox.showerror("Error", f"MySQL Error: {err}")
                return

            #show the user dashboard
            self.user_dashboard()
            #set default tab after registering for an event to my events
            self.user_notebook.select(1)
        except mysql.Error as err:
            messagebox.showerror("Error", f"MySQL Error: {err}")

        #send email confirmation to the user to organizer and current rsvp count
        #send email to the user that they have registered for the event
        #call sendemailConfirmation method with user and event details and organizer details
        self.sendEventsEmailConfirmation(current_user,current_event)

    #sendEmailConfirmation
    def sendEventsEmailConfirmation(self,current_user,current_event):
        
        #user mail
        usermail = current_user[3]
        #organizer mail
        query = "SELECT * FROM eventhub.organizer WHERE organizerID = %s"
        data = (current_event[1],)
        try:
            self.cursor.execute(query, data)
            organizer = self.cursor.fetchone()
        except mysql.Error as err:
            messagebox.showerror("Error", f"MySQL Error: {err}")
            return
        
        organizermail = organizer[2]
        rsvpcount = current_event[8]

        #send email to the user that they have registered for the event
         #setting up server
        server = smtplib.SMTP('smtp.gmail.com',587)
        server.starttls()
        
        password = "ecyvohyivtvbawwy"
        sendermail = "bis698eventhub@gmail.com"
        server.login(sendermail,password)

        body = f"Hi {current_user[1]},\n\nYou have successfully registered for the event {current_event[2]}.\n\nRegards,\nEventhub Team"
        subject = "Event Registration Confirmation"
        message = f'subject:{subject}\n\n{body}'
        try:
            server.sendmail(sendermail,usermail,message)
        except Exception as e:
            print(e)
            messagebox.showerror("Error", "Unable to send email")

        #send email to the organizer that a user has registered for the event and the current rsvp count
        body = f"Hi {organizer[1]},\n\nA user has registered for your event {current_event[2]}.\n\nCurrent RSVP count: {rsvpcount}\n\nRegards,\nEventhub Team"
        subject = "Event Registration Confirmation"
        message = f'subject:{subject}\n\n{body}'
        try:
            server.sendmail(sendermail,organizermail,message)
        except Exception as e:
            print(e)
            messagebox.showerror("Error", "Unable to send email")

        server.quit()

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

    #events_report_pdf
    def events_report_pdf(self):
        # Connect to the 'eventhub' database and retrieve event data
        query = "SELECT * FROM eventhub.event"
        try:
            self.cursor.execute(query)
            events = self.cursor.fetchall()
        except mysql.Error as err:
            messagebox.showerror("Error", f"MySQL Error: {err}")
            return

        # Create a PDF document
        pdf = FPDF()
        pdf.add_page()

        # Add a title to the page
        pdf.set_font("Arial", size=20)
        pdf.cell(200, 10, txt="Events Report", ln=1, align="C")

        # Add a header to the table
        pdf.set_font("Arial", size=12)
        pdf.cell(30, 10, txt="Event Name", border=1)
        pdf.cell(30, 10, txt="Event Date", border=1)
        pdf.cell(30, 10, txt="Event Time", border=1)
        pdf.cell(30, 10, txt="Event Location", border=1)
        pdf.cell(30, 10, txt="Event Description", border=1)
        pdf.cell(30, 10, txt="Registered Count", border=1)
        pdf.ln()

        # Add event data to the table
        for event in events:
            pdf.cell(30, 10, txt=str(event[1]), border=1)
            pdf.cell(30, 10, txt=event[2], border=1)
            pdf.cell(30, 10, txt=event[3], border=1)
            pdf.cell(30, 10, txt=event[4], border=1)
            pdf.cell(30, 10, txt=event[6], border=1)
            pdf.cell(30, 10, txt=str(event[7]), border=1)
            pdf.ln()

        # Save the PDF document
        pdf.output("reports/events_report.pdf")

        messagebox.showinfo("Success", "Events report generated successfully!")

    #users_report_pdf
    def users_report_pdf(self):
        # Connect to the 'eventhub' database and retrieve user data
        query = "SELECT * FROM eventhub.user"
        try:
            self.cursor.execute(query)
            users = self.cursor.fetchall()
        except mysql.Error as err:
            messagebox.showerror("Error", f"MySQL Error: {err}")
            return

        # Create a PDF document
        pdf = FPDF()
        pdf.add_page()

        # Add a title to the page
        pdf.set_font("Arial", size=20)
        pdf.cell(200, 10, txt="Users Report", ln=1, align="C")

        # Add a header to the table
        pdf.set_font("Arial", size=12)
        pdf.cell(30, 10, txt="First Name", border=1)
        pdf.cell(30, 10, txt="Last Name", border=1)
        pdf.cell(30, 10, txt="Email", border=1)
        pdf.cell(30, 10, txt="Phone", border=1)
        pdf.ln()

        # Add user data to the table
        for user in users:
            pdf.cell(30, 10, txt=user[1], border=1)
            pdf.cell(30, 10, txt=user[2], border=1)
            pdf.cell(30, 10, txt=user[3], border=1)
            pdf.cell(30, 10, txt=user[5], border=1)
            pdf.ln()

        # Save the PDF document
        pdf.output("reports/users_report.pdf")

        messagebox.showinfo("Success", "Users report generated successfully!")

    #organizers_report_pdf
    def organizers_report_pdf(self):
        # Connect to the 'eventhub' database and retrieve organizer data
        query = "SELECT * FROM eventhub.organizer"
        try:
            self.cursor.execute(query)
            organizers = self.cursor.fetchall()
        except mysql.Error as err:
            messagebox.showerror("Error", f"MySQL Error: {err}")
            return

        # Create a PDF document
        pdf = FPDF()
        pdf.add_page()

        # Add a title to the page
        pdf.set_font("Arial", size=20)
        pdf.cell(200, 10, txt="Organizers Report", ln=1, align="C")

        # Add a header to the table
        pdf.set_font("Arial", size=12)
        pdf.cell(30, 10, txt="Organizer Name", border=1)
        pdf.cell(30, 10, txt="Organization Email", border=1)
        pdf.cell(30, 10, txt="Organizer Phone", border=1)
        pdf.cell(30, 10, txt="Organization Name", border=1)
        pdf.ln()

        # Add organizer data to the table
        for organizer in organizers:
            pdf.cell(30, 10, txt=organizer[1], border=1)
            pdf.cell(30, 10, txt=organizer[2], border=1)
            pdf.cell(30, 10, txt=organizer[3], border=1)
            pdf.cell(30, 10, txt=organizer[4], border=1)
            pdf.ln()

        # Save the PDF document
        pdf.output("reports/organizers_report.pdf")

        messagebox.showinfo("Success", "Organizers report generated successfully!")
    
    #event_registrations_report_pdf
    def event_registrations_report_pdf(self):
        # Connect to the 'eventhub' database and retrieve event registration data
        query = "SELECT * FROM eventhub.eventRegistration"
        try:
            self.cursor.execute(query)
            event_registrations = self.cursor.fetchall()
        except mysql.Error as err:
            messagebox.showerror("Error", f"MySQL Error: {err}")
            return

        # Create a PDF document
        pdf = FPDF()
        pdf.add_page()

        # Add a title to the page
        pdf.set_font("Arial", size=20)
        pdf.cell(200, 10, txt="Event Registrations Report", ln=1, align="C")

        # Add a header to the table
        pdf.set_font("Arial", size=12)
        pdf.cell(30, 10, txt="Event ID", border=1)
        pdf.cell(30, 10, txt="User ID", border=1)
        pdf.cell(30, 10, txt="Organizer ID", border=1)
        pdf.ln()

        # Add event registration data to the table
        for event_registration in event_registrations:
            pdf.cell(30, 10, txt=str(event_registration[0]), border=1)
            pdf.cell(30, 10, txt=str(event_registration[1]), border=1)
            pdf.cell(30, 10, txt=str(event_registration[2]), border=1)
            pdf.ln()

        # Save the PDF document
        pdf.output("reports/event_registrations_report.pdf")

        messagebox.showinfo("Success", "Event registrations report generated successfully!")


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
        #take date from string and convert to date format
        eventDate = self.event_date_entry.get()
        eventDate = datetime.strptime(eventDate, '%m/%d/%Y').date()
        eventTime = self.event_time_entry.get()
        #convert time to time format HH:MM AM/PM
        eventTime = datetime.strptime(eventTime, '%I:%M %p').time()

        print(eventTime,type(eventTime))
        eventLocation = self.event_location_entry.get()
        eventDescription = self.event_description_entry.get()
        #path
        eventImage = self.current_image_path

        #get current organizer id from current_user_object
        organizer_id = self.current_user_object[0]

        # Validate the user's input
        if eventName == "" or eventDate == "" or eventTime == "" or eventLocation == "" or eventDescription == "":
            messagebox.showerror("Error", "Please fill in all fields")
        else:
            # Insert the user's input into the database with organizerID
            query = "INSERT INTO eventhub.event(eventName, eventDate, eventTime, eventLocation, eventDescription, organizerID,eventImage) VALUES (%s, %s, %s, %s, %s, %s,%s)"
            values = (eventName, eventDate, eventTime, eventLocation, eventDescription, organizer_id,eventImage)

            self.cursor.execute(query, values)
            self.database.commit()

            messagebox.showinfo("Success", "You have registered successfully!")
            self.organizer_dashboard()



 





# -----------------------------------------------------------------------------------------------------------------------


if __name__ == "__main__":
    app = EventHub()
    app.tkn.mainloop()
