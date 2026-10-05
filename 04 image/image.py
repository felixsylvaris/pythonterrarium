
# tkinter is Python's built-in GUI library.
import tkinter as tk

# filedialog gives us a Windows file-selection window.
from tkinter import filedialog

# Image is used to open and resize pictures.
# ImageTk converts the picture into a format Tkinter can display.
from PIL import Image, ImageTk


# This function opens a file and displays the selected picture.
def open_picture():

    # Open the Windows file explorer so the user can choose a picture.
    path = filedialog.askopenfilename(
        filetypes=[("Pictures", "*.jpg *.jpeg *.png")]
    )

    # If the user actually selected a file, continue.
    if path:

        # Load the selected picture.
        image = Image.open(path)

        # Resize the picture so it fits inside our window.
        image.thumbnail((1000, 700))

        # Convert the Pillow image into a Tkinter-compatible image.
        photo = ImageTk.PhotoImage(image)

        # Put the picture inside our label.
        label.config(image=photo)

        # Keep a reference to the image so Python doesn't remove it.
        label.image = photo


# --- Main program starts here ---

# Create the main application window.
root = tk.Tk()
# Set the window size.
root.geometry("1200x00")
# Set the window title.
root.title("Photo")


# Create a button.
# When the button is clicked, open_picture() will run.
button = tk.Button(
    root,
    text="Open picture",
    command=open_picture
)

# Put the button into the window.
button.pack()


# Create an empty label.
# We will use this space to display the picture.
label = tk.Label(root)

# Put the label into the window.
label.pack()


# Start the GUI.
# The program now waits for the user to click something.
root.mainloop()

