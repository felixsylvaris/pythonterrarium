"""
QR Code Generator (v2)

A small tkinter app that turns text into a QR code.

Features:
  - Text box for the message (Ctrl+Enter generates)
  - Optional live preview while you type
  - Error correction level (L/M/Q/H)
  - Adjustable pixel size per QR "box"
  - Pick foreground / background colors
  - Save as PNG or JPEG (opens in this script's folder)
  - Clear button, status bar, friendly error messages

Uses the qrcode library (pip install "qrcode[pil]") and Pillow.
"""
import io
import os
import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox, ttk

import qrcode
from qrcode.exceptions import DataOverflowError
from PIL import Image, ImageTk

# Folder where this script lives - the save dialog opens here.
DEFAULT_DIR = os.path.dirname(os.path.abspath(__file__))

# Max size (pixels) of the preview in the window.
# The saved file always uses the full-size image.
PREVIEW_SIZE = 300

# Map the friendly names in the dropdown to qrcode's constants.
# Higher correction = more damage-tolerant, but a denser (bigger) code.
ERROR_LEVELS = {
    "L (7%)": qrcode.constants.ERROR_CORRECT_L,
    "M (15%)": qrcode.constants.ERROR_CORRECT_M,
    "Q (25%)": qrcode.constants.ERROR_CORRECT_Q,
    "H (30%)": qrcode.constants.ERROR_CORRECT_H,
}


class QRApp:
    """The whole app lives in one class so we don't need globals."""

    def __init__(self, root):
        self.root = root
        root.title("QR Code Generator")
        root.geometry("420x720")
        root.minsize(380, 640)

        # State: the last full-size QR image (None = nothing generated yet).
        self.img = None
        # Keep a reference to the PhotoImage, or Tk shows a blank label.
        self.photo = None
        # Current colors.
        self.fg_color = "#000000"
        self.bg_color = "#ffffff"

        self.build_ui()
        self.bind_events()

    # ---------- UI ----------

    def build_ui(self):
        """Create and place all the widgets."""
        pad = {"padx": 10, "pady": 4}

        # --- Text input ---
        ttk.Label(self.root, text="Message:").pack(anchor="w", **pad)
        self.text_box = tk.Text(self.root, height=5, width=40, wrap="word")
        self.text_box.pack(fill="x", **pad)
        self.text_box.focus_set()

        # --- Options row: error correction + box size ---
        options = ttk.LabelFrame(self.root, text="Options")
        options.pack(fill="x", **pad)

        ttk.Label(options, text="Error correction:").grid(row=0, column=0, sticky="w", padx=6, pady=4)
        self.level_var = tk.StringVar(value="M (15%)")
        level_box = ttk.Combobox(
            options, textvariable=self.level_var,
            values=list(ERROR_LEVELS), state="readonly", width=10,
        )
        level_box.grid(row=0, column=1, sticky="w", padx=6, pady=4)

        ttk.Label(options, text="Box size (px):").grid(row=1, column=0, sticky="w", padx=6, pady=4)
        self.size_var = tk.IntVar(value=10)
        size_spin = ttk.Spinbox(options, from_=1, to=40, textvariable=self.size_var, width=8)
        size_spin.grid(row=1, column=1, sticky="w", padx=6, pady=4)

        # Color buttons (they show the current color via a small swatch label).
        ttk.Button(options, text="Foreground...", command=self.pick_fg).grid(row=2, column=0, padx=6, pady=4, sticky="w")
        self.fg_swatch = tk.Label(options, width=4, bg=self.fg_color, relief="sunken")
        self.fg_swatch.grid(row=2, column=1, sticky="w", padx=6)

        ttk.Button(options, text="Background...", command=self.pick_bg).grid(row=3, column=0, padx=6, pady=4, sticky="w")
        self.bg_swatch = tk.Label(options, width=4, bg=self.bg_color, relief="sunken")
        self.bg_swatch.grid(row=3, column=1, sticky="w", padx=6)

        # Live preview checkbox: regenerate on every keystroke.
        self.live_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(options, text="Live preview", variable=self.live_var).grid(
            row=4, column=0, columnspan=2, sticky="w", padx=6, pady=4
        )

        # Remember the widgets that should re-trigger a live update.
        self.level_box = level_box
        self.size_spin = size_spin

        # --- Action buttons ---
        buttons = ttk.Frame(self.root)
        buttons.pack(fill="x", **pad)
        ttk.Button(buttons, text="Generate", command=self.generate_qr).pack(side="left", expand=True, fill="x", padx=2)
        ttk.Button(buttons, text="Save...", command=self.save_qr).pack(side="left", expand=True, fill="x", padx=2)
        ttk.Button(buttons, text="Clear", command=self.clear_qr).pack(side="left", expand=True, fill="x", padx=2)

        # --- QR image display ---
        self.imgspot = tk.Label(self.root, bg="#f0f0f0")
        self.imgspot.pack(expand=True, fill="both", **pad)

        # --- Status bar ---
        self.status_var = tk.StringVar(value="Type something and press Generate (or Ctrl+Enter).")
        ttk.Label(self.root, textvariable=self.status_var, relief="sunken", anchor="w").pack(
            side="bottom", fill="x"
        )

    def bind_events(self):
        """Keyboard shortcuts and live-preview hooks."""
        self.root.bind("<Control-Return>", lambda e: self.generate_qr())
        self.root.bind("<Control-s>", lambda e: self.save_qr())
        # <<Modified>> fires when text changes; we must reset the flag each time.
        self.text_box.bind("<<Modified>>", self.on_text_change)
        # Changing options also refreshes the preview if live mode is on.
        self.level_box.bind("<<ComboboxSelected>>", lambda e: self.maybe_live_update())
        self.size_spin.bind("<KeyRelease>", lambda e: self.maybe_live_update())
        self.size_spin.bind("<<Increment>>", lambda e: self.root.after(1, self.maybe_live_update))
        self.size_spin.bind("<<Decrement>>", lambda e: self.root.after(1, self.maybe_live_update))

    # ---------- Helpers ----------

    def set_status(self, message):
        """Update the status bar text."""
        self.status_var.set(message)

    def on_text_change(self, event=None):
        """Called whenever the text box content changes."""
        if self.text_box.edit_modified():
            self.text_box.edit_modified(False)  # reset the flag so it fires again
            self.maybe_live_update()

    def maybe_live_update(self):
        """Regenerate only if live preview is on."""
        if self.live_var.get():
            self.generate_qr(quiet=True)

    def pick_fg(self):
        """Choose the QR code (dark squares) color."""
        _, hex_color = colorchooser.askcolor(color=self.fg_color, parent=self.root)
        if hex_color:  # None if the user cancelled
            self.fg_color = hex_color
            self.fg_swatch.config(bg=hex_color)
            self.maybe_live_update()

    def pick_bg(self):
        """Choose the background color."""
        _, hex_color = colorchooser.askcolor(color=self.bg_color, parent=self.root)
        if hex_color:
            self.bg_color = hex_color
            self.bg_swatch.config(bg=hex_color)
            self.maybe_live_update()

    # ---------- Actions ----------

    def generate_qr(self, quiet=False):
        """Read the text box, build the QR code, show a preview.

        quiet=True is used by live preview: no popups, just status messages.
        """
        text = self.text_box.get("1.0", "end-1c")

        # Nothing to encode.
        if not text.strip():
            if not quiet:
                messagebox.showwarning("Warning", "Enter some text first!")
            else:
                self.clear_image()
                self.set_status("Waiting for text...")
            return

        # Read box size safely (the spinbox could contain junk while typing).
        try:
            box_size = max(1, min(40, int(self.size_var.get())))
        except (tk.TclError, ValueError):
            box_size = 10

        try:
            qr = qrcode.QRCode(
                version=None,  # None + fit=True = pick the smallest size that fits
                error_correction=ERROR_LEVELS[self.level_var.get()],
                box_size=box_size,
                border=4,  # 4 boxes of quiet zone is the QR spec minimum
            )
            qr.add_data(text)
            qr.make(fit=True)
            qr_img = qr.make_image(fill_color=self.fg_color, back_color=self.bg_color)
        except (DataOverflowError, ValueError):
            # Text too long for even the biggest QR code at this error level.
            self.set_status("Text is too long for a QR code. Try a lower error correction.")
            if not quiet:
                messagebox.showerror("Too much text", "That text doesn't fit in a QR code.\nShorten it or lower the error correction level.")
            return

        # Round-trip through memory to get a plain Pillow image
        # (works the same across qrcode versions).
        buffer = io.BytesIO()
        qr_img.save(buffer, format="PNG")
        buffer.seek(0)
        self.img = Image.open(buffer).convert("RGB")

        self.show_preview()
        self.set_status(f"QR generated: {self.img.width}x{self.img.height}px, {len(text)} characters.")

    def show_preview(self):
        """Show a scaled-down copy so big codes still fit the window."""
        preview = self.img.copy()
        # NEAREST keeps the squares crisp instead of blurry.
        preview.thumbnail((PREVIEW_SIZE, PREVIEW_SIZE), Image.NEAREST)
        self.photo = ImageTk.PhotoImage(preview)
        self.imgspot.config(image=self.photo)

    def clear_image(self):
        """Remove the QR image (but leave the text)."""
        self.img = None
        self.photo = None
        self.imgspot.config(image="")

    def clear_qr(self):
        """Clear the text box and the QR code display."""
        self.text_box.delete("1.0", "end")
        self.clear_image()
        self.set_status("Cleared.")
        self.text_box.focus_set()

    def save_qr(self):
        """Ask where to save, then write the full-size QR code to a file."""
        if self.img is None:
            messagebox.showwarning("Warning", "Generate a QR code first!")
            return

        # initialdir may be ignored by Windows (it reopens the last used folder).
        file_path = filedialog.asksaveasfilename(
            parent=self.root,
            initialdir=DEFAULT_DIR,
            initialfile="qrcode.png",
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")],
        )

        # Empty string means the user cancelled.
        if not file_path:
            return

        try:
            self.img.save(file_path)  # format is picked from the file extension
        except (OSError, ValueError) as error:
            messagebox.showerror("Save failed", f"Could not save the file:\n{error}")
            return

        self.set_status(f"Saved to {file_path}")
        messagebox.showinfo("QR Code Generator", f"QR code saved as\n{file_path}")


def main():
    """Create the window and run the app."""
    root = tk.Tk()
    QRApp(root)
    root.mainloop()


# Only run when executed directly (not when imported).
if __name__ == "__main__":
    main()
