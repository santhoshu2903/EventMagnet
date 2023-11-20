import tkinter as tk
import re
from tkinter import ttk

class YourClass:
    def __init__(self):
        self.tkn = tk.Tk()
        self.tab_control = ttk.Notebook(self.tkn)
        self.tab_control.pack()

        # Create password labels
        self.password_label1 = tk.Label(self.tkn, text="Uppercase", fg="red")
        self.password_label1.pack()

        self.password_label2 = tk.Label(self.tkn, text="Lowercase", fg="red")
        self.password_label2.pack()

        self.password_label3 = tk.Label(self.tkn, text="Digit", fg="red")
        self.password_label3.pack()

        self.password_label4 = tk.Label(self.tkn, text="Special Char", fg="red")
        self.password_label4.pack()

        # Create password entry widgets
        self.user_password_entry = tk.Entry(self.tkn, show="*")
        self.user_password_entry.pack()

        self.organizer_password_entry = tk.Entry(self.tkn, show="*")
        self.organizer_password_entry.pack()

        # Bind KeyRelease event to password validation
        self.user_password_entry.bind("<KeyRelease>", lambda event: self.password_validation(event, "user"))
        self.organizer_password_entry.bind("<KeyRelease>", lambda event: self.password_validation(event, "organizer"))

        self.tkn.mainloop()

    def password_validation(self, event, user_type):
        # Determine the password based on the user type
        password_entry = getattr(self, f"{user_type}_password_entry")
        password = password_entry.get()

        # Check if 8 characters
        if len(password) >= 8:
            self.password_label1.config(fg="green")
        else:
            self.password_label1.config(fg="red")

        # At least one uppercase
        if re.search("[A-Z]", password):
            self.password_label2.config(fg="green")
        else:
            self.password_label2.config(fg="red")

        # At least one lowercase
        if re.search("[a-z]", password):
            self.password_label3.config(fg="green")
        else:
            self.password_label3.config(fg="red")

        # At least one digit
        if re.search("[0-9]", password):
            self.password_label4.config(fg="green")
        else:
            self.password_label4.config(fg="red")

# Create an instance of YourClass
your_instance = YourClass()
