"""
This is analog clock with hands, numbers. 
"""

import tkinter as tk
from datetime import datetime
import math

# Create a Tkinter window
root = tk.Tk()
root.title("Analog Clock")

# Constants for clock size
CLOCK_WIDTH = 400
CLOCK_HEIGHT = 400
CLOCK_CENTER_X = CLOCK_WIDTH // 2
CLOCK_CENTER_Y = CLOCK_HEIGHT // 2
CLOCK_RADIUS = min(CLOCK_WIDTH, CLOCK_HEIGHT) // 2 - 20

ROMAN_NUMERALS = ["XII", "I", "II", "III", "IV", "V",
                  "VI", "VII", "VIII", "IX", "X", "XI"]

# Function to draw the clock
def draw_clock():
    current_time = datetime.now()
    hour = current_time.hour
    minute = current_time.minute
    second = current_time.second

    # Clear canvas
    canvas.delete("all")

    # Draw clock outline
    canvas.create_oval(CLOCK_CENTER_X - CLOCK_RADIUS, CLOCK_CENTER_Y - CLOCK_RADIUS,
                       CLOCK_CENTER_X + CLOCK_RADIUS, CLOCK_CENTER_Y + CLOCK_RADIUS, width=5)

    # Draw Roman numeral hour markers
    for i in range(12):
        angle = math.radians(i * 30 - 90)
        num_x = CLOCK_CENTER_X + 0.78 * CLOCK_RADIUS * math.cos(angle)
        num_y = CLOCK_CENTER_Y + 0.78 * CLOCK_RADIUS * math.sin(angle)
        canvas.create_text(num_x, num_y, text=ROMAN_NUMERALS[i],
                           fill="silver", font=("Times New Roman", 16, "bold"))

    # Draw 12 big dots marking exact hour positions (outside the numerals)
    for i in range(12):
        angle = math.radians(i * 30 - 90)
        dot_x = CLOCK_CENTER_X + 0.93 * CLOCK_RADIUS * math.cos(angle)
        dot_y = CLOCK_CENTER_Y + 0.93 * CLOCK_RADIUS * math.sin(angle)
        size = 5
        canvas.create_oval(dot_x - size, dot_y - size,
                           dot_x + size, dot_y + size, fill="silver")

    # Draw small dots for minute marks between hours
    for i in range(60):
        if i % 5 == 0:
            continue  # hour positions use the big dots above
        angle = math.radians(i * 6 - 90)
        dot_x = CLOCK_CENTER_X + 0.92 * CLOCK_RADIUS * math.cos(angle)
        dot_y = CLOCK_CENTER_Y + 0.92 * CLOCK_RADIUS * math.sin(angle)
        size = 2
        canvas.create_oval(dot_x - size, dot_y - size,
                           dot_x + size, dot_y + size, fill="silver")

    # Draw hour hand
    hour_angle = math.radians( (hour % 12) * 30 + minute * 0.5 - 90)
    hour_x = CLOCK_CENTER_X + 0.6 * CLOCK_RADIUS * math.cos(hour_angle)
    hour_y = CLOCK_CENTER_Y + 0.6 * CLOCK_RADIUS * math.sin(hour_angle)
    canvas.create_line(CLOCK_CENTER_X, CLOCK_CENTER_Y, hour_x, hour_y, width=6)

    # Draw minute hand
    minute_angle = math.radians(minute * 6 + second * 0.1 - 90)
    minute_x = CLOCK_CENTER_X + 0.8 * CLOCK_RADIUS * math.cos(minute_angle)
    minute_y = CLOCK_CENTER_Y + 0.8 * CLOCK_RADIUS * math.sin(minute_angle)
    canvas.create_line(CLOCK_CENTER_X, CLOCK_CENTER_Y, minute_x, minute_y, fill="white", width=3)

    # Draw second hand
    second_angle = math.radians(second * 6 - 90)
    second_x = CLOCK_CENTER_X + 0.9 * CLOCK_RADIUS * math.cos(second_angle)
    second_y = CLOCK_CENTER_Y + 0.9 * CLOCK_RADIUS * math.sin(second_angle)
    canvas.create_line(CLOCK_CENTER_X, CLOCK_CENTER_Y, second_x, second_y, fill="red", width=2)

    # Draw clock center
    canvas.create_oval(CLOCK_CENTER_X - 5, CLOCK_CENTER_Y - 5,
                       CLOCK_CENTER_X + 5, CLOCK_CENTER_Y + 5, fill="black")

    # Schedule next clock update after 1000 milliseconds (1 second)
    root.after(1000, draw_clock)

# Create a canvas to draw the clock
canvas = tk.Canvas(root, width=CLOCK_WIDTH, height=CLOCK_HEIGHT, bg="blue")
canvas.pack()

# Start drawing the clock
draw_clock()

# Run the Tkinter event loop
root.mainloop()
