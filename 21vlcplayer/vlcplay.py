import os
import tkinter as tk
from tkinter import filedialog, ttk

import vlc

POLL_MS = 250
VIDEO_TYPES = [("Video files", "*.mp4 *.mkv *.avi *.webm *.mov"), ("All files", "*.*")]


class Player(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("MP4 Player")
        self.geometry("800x500")

        # default VLC settings (extra flags removed while debugging)
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()

        self.video_frame = tk.Frame(self, bg="black")
        self.video_frame.pack(fill=tk.BOTH, expand=True)

        bar = tk.Frame(self)
        bar.pack(fill=tk.X)

        self.open_btn = tk.Button(bar, text="\U0001F4C2", width=3, command=self.open_file)
        self.open_btn.pack(side=tk.LEFT, padx=4, pady=4)

        self.play_btn = tk.Button(bar, text="Play", width=6, command=self.toggle_play)
        self.play_btn.pack(side=tk.LEFT, padx=2)

        self.progress = ttk.Scale(bar, from_=0, to=1, orient=tk.HORIZONTAL)
        self.progress.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=4)
        # seek once on release instead of on every drag event (seeks are expensive)
        self.progress.bind("<ButtonPress-1>", self._seek_press)
        self.progress.bind("<ButtonRelease-1>", self._seek_release)

        self.status = tk.Label(bar, text="No file loaded")
        self.status.pack(side=tk.LEFT, padx=4)

        self.seeking = False
        self.poll_id = None

        self.bind("<space>", lambda e: self.toggle_play())
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def open_file(self):
        path = filedialog.askopenfilename(filetypes=VIDEO_TYPES)
        if not path:
            return
        self.player.set_media(self.instance.media_new(path))
        # embed VLC into the video frame (same order as the original, which worked)
        win_id = self.video_frame.winfo_id()
        if os.name == "nt":
            self.player.set_hwnd(win_id)
        else:
            self.player.set_xwindow(win_id)
        self.player.play()
        self.status.config(text=os.path.basename(path))
        self._set_playing_ui(True)
        self._start_poll()

    def toggle_play(self):
        if not self.player.get_media():
            return
        if self.player.get_state() == vlc.State.Ended:
            self.player.stop()
            self.player.play()
        else:
            self.player.pause()  # toggles
        self._set_playing_ui(self.player.get_state() != vlc.State.Paused)
        self._start_poll()

    def _set_playing_ui(self, playing):
        self.play_btn.config(text="Pause" if playing else "Play")

    def _seek_press(self, event):
        self.seeking = True
        self._jump_to(event)

    def _seek_release(self, event):
        self.seeking = False
        if self.player.get_media() and self.player.is_seekable():
            self.player.set_position(self._ratio(event))

    def _ratio(self, event):
        w = self.progress.winfo_width()
        return min(max(event.x / w, 0.0), 1.0) if w else 0.0

    def _jump_to(self, event):
        self.progress.set(self._ratio(event))

    # poll only while playing; stops itself when paused/ended
    def _start_poll(self):
        if self.poll_id is None:
            self.poll_id = self.after(POLL_MS, self._poll)

    def _poll(self):
        self.poll_id = None
        state = self.player.get_state()
        if state == vlc.State.Ended:
            self.progress.set(1)
            self._set_playing_ui(False)
        elif state in (vlc.State.Paused, vlc.State.Stopped, vlc.State.Error):
            return
        else:  # NothingSpecial, Opening, Buffering, Playing
            if state == vlc.State.Playing and not self.seeking:
                self.progress.set(self.player.get_position())
            self.poll_id = self.after(POLL_MS, self._poll)

    def on_close(self):
        if self.poll_id is not None:
            self.after_cancel(self.poll_id)
        self.player.stop()
        self.player.release()
        self.instance.release()
        self.destroy()


if __name__ == "__main__":
    Player().mainloop()
