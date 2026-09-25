import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

import cv2
from PIL import Image, ImageTk


VIDEO_EXTENSIONS = {".mp4", ".mov", ".avi", ".mkv", ".wmv", ".mpeg", ".mpg", ".m4v"}


class MediaGalleryApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Rip-Off YouTube")
        self.geometry("1320x860")
        self.minsize(1100, 700)
        self.configure(bg="#0f172a")

        self.column_count = 4
        self.media_items = [
            {"id": 1, "title": "Demo Clip 1", "path": "", "file_type": "video"},
            {"id": 2, "title": "Demo Clip 2", "path": "", "file_type": "video"},
            {"id": 3, "title": "Demo Clip 3", "path": "", "file_type": "video"},
            {"id": 4, "title": "Demo Clip 4", "path": "", "file_type": "video"},
            {"id": 5, "title": "Demo Clip 5", "path": "", "file_type": "video"},
            {"id": 6, "title": "Demo Clip 6", "path": "", "file_type": "video"},
        ]

        self.main_frame = ttk.Frame(self, padding=18)
        self.main_frame.pack(fill="both", expand=True)

        self.toolbar = tk.Frame(self.main_frame, bg="#0f172a")
        self.toolbar.pack(fill="x", pady=16)

        self.title_label = tk.Label(
            self.toolbar,
            text="Media Library",
            fg="white",
            bg="#0f172a",
            font=("Segoe UI", 24, "bold"),
        )
        self.title_label.pack(side="left")

        upload_button = tk.Button(
            self.toolbar,
            text="Upload Video",
            command=self.upload_media,
            bg="#2563eb",
            fg="white",
            activebackground="#1d4ed8",
            font=("Segoe UI", 11, "bold"),
            padx=16,
            pady=8,
            borderwidth=0,
            cursor="hand2",
        )
        upload_button.pack(side="right")

        self.canvas = tk.Canvas(self.main_frame, bg="#0f172a", highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.gallery = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.gallery, anchor="nw")
        self.gallery.bind("<Configure>", self._update_scroll_region)
        self.bind("<Configure>", self._update_scroll_region)

        self.refresh_gallery()

    def _update_scroll_region(self, event=None):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def get_card_color(self, media_id):
        palette = [
            "#2563eb",
            "#7c3aed",
            "#10b981",
            "#f59e0b",
            "#ef4444",
            "#14b8a6",
            "#f97316",
            "#84cc16",
            "#ec4899",
        ]
        return palette[(media_id - 1) % len(palette)]

    def refresh_gallery(self):
        for child in self.gallery.winfo_children():
            child.destroy()

        for col_index in range(self.column_count):
            self.gallery.columnconfigure(col_index, weight=1)

        for index, media in enumerate(self.media_items):
            row = index // self.column_count
            col = index % self.column_count
            self.create_media_card(self.gallery, media, row, col)

        self.update_idletasks()
        self._update_scroll_region()

    def create_media_card(self, parent, media, row, col):
        card = tk.Frame(parent, bg="#1f2937", padx=10, pady=8, bd=0)
        card.grid(row=row, column=col, padx=10, pady=12, sticky="nsew")
        card.configure(cursor="hand2")

        def open_selected(event=None):
            self.open_media_window(media)

        def on_enter(event):
            card.configure(bg="#334155")

        def on_leave(event):
            card.configure(bg="#1f2937")

        card.bind("<Button-1>", open_selected)
        card.bind("<Enter>", on_enter)
        card.bind("<Leave>", on_leave)

        thumbnail = tk.Label(
            card,
            bg=self.get_card_color(media["id"]),
            anchor="center",
            text="",
            compound="center",
            width=24,
            height=12,
        )
        thumbnail.pack(fill="x")
        thumbnail.bind("<Button-1>", open_selected)
        thumbnail.bind("<Enter>", on_enter)
        thumbnail.bind("<Leave>", on_leave)

        self.draw_video_placeholder(thumbnail, media["id"])

        title = tk.Label(
            card,
            text=media["title"],
            bg="#1f2937",
            fg="white",
            font=("Segoe UI", 11, "bold"),
            anchor="w",
            justify="left",
            padx=4,
            pady=8,
        )
        title.pack(fill="x")
        title.bind("<Button-1>", open_selected)
        title.bind("<Enter>", on_enter)
        title.bind("<Leave>", on_leave)

        detail_text = "Uploaded clip" if media["path"] else "Demo clip"
        subtitle = tk.Label(
            card,
            text=f"Video • {detail_text}",
            bg="#1f2937",
            fg="#cbd5e1",
            anchor="w",
            justify="left",
            padx=4,
            pady=8,
        )
        subtitle.pack(fill="x")
        subtitle.bind("<Button-1>", open_selected)
        subtitle.bind("<Enter>", on_enter)
        subtitle.bind("<Leave>", on_leave)

    def draw_video_placeholder(self, widget, media_id):
        canvas = tk.Canvas(widget, width=240, height=150, bg=self.get_card_color(media_id), highlightthickness=0)
        canvas.pack(fill="both", expand=True)
        canvas.create_rectangle(18, 18, 222, 132, fill="#111827", outline="#475569", width=2)
        canvas.create_polygon(90, 54, 90, 96, 150, 75, fill="#f8fafc")
        canvas.create_text(120, 110, text="VIDEO", fill="white", font=("Segoe UI", 16, "bold"))

    def open_video_file(self, file_path):
        if not file_path or not os.path.exists(file_path):
            return False

        try:
            cap = cv2.VideoCapture(file_path)
            if not cap.isOpened():
                return False

            frame_label = None
            for widget in self.winfo_children():
                pass

            return True
        except Exception:
            return False

    def upload_media(self):
        file_path = filedialog.askopenfilename(
            title="Select a video",
            filetypes=[
                ("Video files", "*.mp4 *.mov *.avi *.mkv *.wmv *.mpeg *.mpg *.m4v"),
                ("All supported video files", "*.mp4 *.mov *.avi *.mkv *.wmv *.mpeg *.mpg *.m4v"),
            ],
        )
        if not file_path:
            return

        extension = os.path.splitext(file_path)[1].lower()
        if extension not in VIDEO_EXTENSIONS:
            tk.messagebox.showerror("Unsupported file", "Please choose a valid video file.")
            return

        title = os.path.splitext(os.path.basename(file_path))[0]
        self.media_items.append(
            {"id": len(self.media_items) + 1, "title": title, "path": file_path, "file_type": "video"}
        )
        self.refresh_gallery()

    def open_media_window(self, media):
        media_window = tk.Toplevel(self)
        media_window.title(f"{media['title']} - Video")
        media_window.geometry("940x640")
        media_window.minsize(700, 500)
        media_window.configure(bg="#020617")

        heading = tk.Label(
            media_window,
            text=media["title"],
            fg="white",
            bg="#020617",
            font=("Segoe UI", 23, "bold"),
        )
        heading.pack(pady=12)

        video_frame = tk.LabelFrame(media_window, text="Now playing", bg="#0f172a", fg="white", padx=10, pady=10)
        video_frame.pack(padx=18, pady=8, fill="both", expand=True)

        player_label = tk.Label(video_frame, bg="#111827", width=80, height=20)
        player_label.pack(fill="both", expand=True)

        details = tk.Label(
            media_window,
            text=(
                f"Media type: Video\n"
                f"File path: {media['path'] if media['path'] else 'Demo video placeholder'}\n"
                "The video plays directly inside this Python window."
            ),
            wraplength=700,
            justify="left",
            bg="#020617",
            fg="#e2e8f0",
            font=("Segoe UI", 11),
            padx=24,
            pady=18,
        )
        details.pack(fill="x")

        if media["path"]:
            self.start_video_playback(media["path"], player_label)
        else:
            player_label.configure(text="Demo clip placeholder", fg="white", font=("Segoe UI", 18, "bold"))

    def start_video_playback(self, file_path, player_label):
        try:
            cap = cv2.VideoCapture(file_path)
        except Exception:
            player_label.configure(text="Unable to load video", fg="white", font=("Segoe UI", 16, "bold"))
            return

        def update_frame():
            if not cap.isOpened():
                player_label.configure(text="Video unavailable", fg="white", font=("Segoe UI", 16, "bold"))
                return

            ret, frame = cap.read()
            if not ret:
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                ret, frame = cap.read()
                if not ret:
                    player_label.configure(text="Video ended", fg="white", font=("Segoe UI", 16, "bold"))
                    return

            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(rgb)
            image = image.resize((720, 360), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(image=image)
            player_label.configure(image=photo)
            player_label.image = photo
            player_label.after(33, update_frame)

        update_frame()


if __name__ == "__main__":
    app = MediaGalleryApp()
    app.mainloop()
