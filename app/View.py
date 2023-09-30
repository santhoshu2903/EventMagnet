from tkinter import *
from tkinter import messagebox
import tkinter.ttk as ttk
import Controller
import Model

class View:
    def __init__(self, root=None):
        self.model= Model.Model()
        self.messagebox = messagebox
        self.root = root
        # self.controller = Controller.Controller()
        self.create_main_window()

    def set_window_size(self, width, height):
        # Set the window's dimensions dynamically
        self.root.geometry(f"{width}x{height}")

    def create_main_window(self):
        # Create the main window
        self.root.title("Event Hub")
        self.root.geometry("400x300")

        # Add buttons to navigate to different views
        welcome_button = Button(self.root, text="Welcome Page", command=self.welcome_page)
        login_button = Button(self.root, text="Login Page", command=self.login_page)
        register_button = Button(self.root, text="Register Page", command=self.register_page)

        welcome_button.pack(pady=20)
        login_button.pack(pady=10)
        register_button.pack(pady=10)

    def welcome_page(self):
        # Create or update the welcome page
        self.root.geometry("400x400")
        for widget in self.root.winfo_children():
            widget.destroy()

        label = Label(self.root, text="Welcome to Event Hub", font=("Helvetica", 20))
        label.pack(pady=20)

        info_label = Label(self.root, text="Discover and attend exciting events in your area.")
        info_label.pack()
        # self.set_window_size(400, self.root.winfo_reqheight())

    def login_page(self):
        self.root.geometry("500x500")
        # Create or update the login page
        for widget in self.root.winfo_children():
            widget.destroy()

        # Add login form elements
        label = Label(self.root, text="Login Page", font=("Helvetica", 20))
        label.pack(pady=20)

        # Email (Gmail ID) entry
        email_label = Label(self.root, text="Email (Gmail ID):")
        email_label.pack()
        email_entry = Entry(self.root)
        email_entry.pack()

        # Password entry
        password_label = Label(self.root, text="Password:")
        password_label.pack()
        password_entry = Entry(self.root, show="*")  # Passwords should be hidden
        password_entry.pack()

        # Login button
        login_button = Button(self.root, text="Login", command=lambda: self.handle_login(email_entry.get(), password_entry.get()))
        login_button.pack(pady=10)

        # Back button to return to the welcome page
        back_button = Button(self.root, text="Back to Welcome", command=self.welcome_page)
        back_button.pack(pady=10)   
        # self.set_window_size(400, self.root.winfo_reqheight())

    def register_page(self):
        # Create or update the registration page
        self.root.geometry("500x600")
        for widget in self.root.winfo_children():
            widget.destroy()

        # Add registration form elements
        label = Label(self.root, text="Register Page", font=("Helvetica", 20))
        label.pack(pady=20)

        # First Name entry
        first_name_label = Label(self.root, text="First Name:")
        first_name_label.pack()
        first_name_entry = Entry(self.root)
        first_name_entry.pack()

        # Last Name entry
        last_name_label = Label(self.root, text="Last Name:")
        last_name_label.pack()
        last_name_entry = Entry(self.root)
        last_name_entry.pack()

        # Email (Gmail ID) entry
        email_label = Label(self.root, text="Email (Gmail ID):")
        email_label.pack()
        email_entry = Entry(self.root)
        email_entry.pack()

        # Phone Number entry
        phone_number_label = Label(self.root, text="Phone Number:")
        phone_number_label.pack()
        phone_number_entry = Entry(self.root)
        phone_number_entry.pack()

        # Date of Birth entry
        dob_label = Label(self.root, text="Date of Birth (YYYY-MM-DD):")
        dob_label.pack()
        dob_entry = Entry(self.root)
        dob_entry.pack()

        # Register button
        register_button = Button(self.root, text="Register", command=lambda: self.handle_registration(
            first_name_entry.get(), last_name_entry.get(), email_entry.get(), phone_number_entry.get(), dob_entry.get()
        ))
        register_button.pack(pady=10)

        # Back button to return to the welcome page
        back_button = Button(self.root, text="Back to Welcome", command=self.welcome_page)
        back_button.pack(pady=10)
        # self.set_window_size(600, self.root.winfo_reqheight())

    def handle_registration(self,firstName,lastName,gmail,phoneNumber,dob):
        self.model.registerUser(firstName,lastName,gmail,phoneNumber,dob)


if __name__ == "__main__":
    root = Tk()
    app = View(root)
    root.mainloop()
