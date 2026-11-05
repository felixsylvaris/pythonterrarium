"""
This is app which displays digital clock using tkinter module. 
"""


import tkinter as tk #this is the module which is used to create GUI applications in python.

import time # this module provides various time-related functions.


root = tk.Tk() # This line creates the main window of the application. The Tk() class is used to create a new instance of the Tkinter application.


root.title("Clock") # This line sets the title of the main window to "Clock". The title is displayed in the title bar of the window.

root.geometry("400x200") # This line sets the size of the main window to 400 pixels wide and 200 pixels tall. The geometry() method is used to specify the dimensions of the window.

# Create a label to display the time    
time_label = tk.Label(root, font=("Arial", 50)) # This line creates a label widget that will be used to display the current time. The font is set to Arial with a size of 50.
time_label.pack(pady=20) # This line adds the label to the main window and centers it vertically with a padding of 20 pixels.

def update_time():
    current_time = time.strftime("%H:%M:%S") # This line gets the current time in the format of hours, minutes, and seconds using the strftime() function from the time module.
    time_label.config(text=current_time) # This line updates the text of the time_label widget to display the current time.
    time_label.after(1000, update_time)  # Update every second


update_time()  #call the function to update the time every second.


root.mainloop() # This line starts the main event loop of the application. It waits for events such as button clicks or key presses and updates the GUI accordingly. The mainloop() method is called on the root window to start the event loop.
