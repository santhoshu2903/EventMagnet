import tkinter as tk
from tkinter import ttk

class CenteredTabsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Centered Tabs")

        self.notebook = ttk.Notebook(self.root)

        # Create tabs
        tab1 = ttk.Frame(self.notebook)
        tab2 = ttk.Frame(self.notebook)

        # Add tabs to the notebook
        self.notebook.add(tab1, text="Tab 1")
        self.notebook.add(tab2, text="Tab 2")

        # Add content to tabs (optional)
        label1 = tk.Label(tab1, text="Content for Tab 1")
        label1.pack(padx=10, pady=10)

        label2 = tk.Label(tab2, text="Content for Tab 2")
        label2.pack(padx=10, pady=10)

        # Pack the notebook to the root window, centering it
        self.notebook.pack(side="top", anchor="center", pady=50)

if __name__ == "__main__":
    root = tk.Tk()
    app = CenteredTabsApp(root)
    root.geometry("400x300")
    root.mainloop()
