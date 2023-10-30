import tkinter as tk
from PIL import Image, ImageTk

class MyApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("400x400")

        # Load an image
        image = Image.open("images/welcome.jpg")
        self.photo = ImageTk.PhotoImage(image)

        # Create a label to display the image
        image_label = tk.Label(self.root, image=self.photo)
        image_label.grid(row=0, column=0, rowspan=4, columnspan=4)

        # Create a label with text
        text_label = tk.Label(self.root, text="Your text goes here", font=("Helvetica", 16))
        text_label.grid(row=0, column=1)

if __name__ == "__main__":
    root = tk.Tk()
    app = MyApp(root)
    root.mainloop()
