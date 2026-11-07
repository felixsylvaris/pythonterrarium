"""
This project is a simple QR code generator.
We want a tkinter app window.
With a text box to write our message.
A button to generate the QR code.
We will use the qrcode library to generate the QR code.
And a button to save the QR code to a file.
"""
import os
import tkinter as tk
from tkinter import filedialog, messagebox

import qrcode
from PIL import ImageTk

# Folder where this script lives - the save dialog will open here.
DEFAULT_DIR = os.path.dirname(os.path.abspath(__file__))

# Global variable to hold the last generated QR code image.
# None means "nothing generated yet".
img = None


# ---------- Button actions ----------

def generate_qr():
    """Read the text box, make a QR code, show it in the window."""
    global img

    # Get all the text from the text box ("end-1c" drops the trailing newline).
    text = text_box.get("1.0", "end-1c")

    # Don't generate a QR code for empty text.
    if not text.strip():
        messagebox.showwarning("Warning", "Enter some text first!")
        return

    # Generate the QR code (returns an image object we can save later).
    img = qrcode.make(text)

    # Convert it to a format Tkinter can display.
    photo = ImageTk.PhotoImage(img)

    # Show it in the label.
    # Keep a reference on the label too, otherwise Python garbage-collects
    # the image and the label shows up blank.
    imgspot.image = photo
    imgspot.config(image=photo)


def save_qr():
    """Ask where to save, then write the QR code to a PNG file."""
    # Check that we have a QR code first.
    if img is None:
        messagebox.showwarning("Warning", "Generate a QR code first!")
        return

    # Ask the user for a file name.
    # - initialdir: folder the dialog opens in (our script folder).
    #   NOTE: on Windows the OS sometimes ignores this and reopens the last
    #   folder you used. That is probably why it "didn't work" for you.
    #   Passing parent=root helps it behave more reliably.
    # - initialfile: suggested file name.
    file_path = filedialog.asksaveasfilename(
        parent=root,
        initialdir=DEFAULT_DIR,
        initialfile="qrcode.png",
        defaultextension=".png",
        filetypes=[("PNG files", "*.png")],
    )

    # If the user cancels, file_path is empty and we do nothing.
    if file_path:
        img.save(file_path)
        messagebox.showinfo("QR Code Generator", f"QR code saved as {file_path}")


# ---------- Build the window ----------

root = tk.Tk()
root.geometry("400x600")
root.title("QR Code Generator")

# Text box where the user types the message for the QR code.
text_box = tk.Text(root, height=5, width=40)
text_box.pack()

# Generate button.
generate_button = tk.Button(root, text="Generate QR Code", command=generate_qr)
generate_button.pack()

# Save button.
save_button = tk.Button(root, text="Save QR Code", command=save_qr)
save_button.pack()

# Label used to display the QR code picture.
imgspot = tk.Label(root)
imgspot.pack()

# Start the app.
root.mainloop()
