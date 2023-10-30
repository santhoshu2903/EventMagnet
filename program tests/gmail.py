import tkinter as tk
from tkinter import messagebox
import smtplib
import random


class GmailLoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gmail Login")
        self.root.geometry("300x200")

        self.create_widgets()

    def create_widgets(self):
        # Create labels and entry fields for Gmail and authentication code
        gmail_label = tk.Label(self.root, text="Gmail:")
        gmail_label.pack()
        self.gmail_entry = tk.Entry(self.root)
        self.gmail_entry.pack()

        code_label = tk.Label(self.root, text="Authentication Code:")
        code_label.pack()
        self.code_entry = tk.Entry(self.root)
        self.code_entry.pack()

        # Create a "Login" button
        login_button = tk.Button(self.root, text="Login", command=self.login)
        login_button.pack()

    def login(self):
        # Get the Gmail address and authentication code from the entry fields
        gmail = self.gmail_entry.get()
        code = self.code_entry.get()

        # Generate a random 6-digit authentication code for demonstration purposes
        random_code = str(random.randint(100000, 999999))

        if gmail == "your@gmail.com" and code == random_code:
            messagebox.showinfo("Success", "Login successful!")
        else:
            messagebox.showerror("Error", "Invalid Gmail or authentication code. Please try again.")

def main():
    root = tk.Tk()
    app = GmailLoginApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
