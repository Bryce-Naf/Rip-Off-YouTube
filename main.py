import os
import tkinter as tk
from datetime import datetime, timedelta
from tkinter import filedialog, messagebox, simpledialog, ttk

import cv2
from PIL import Image, ImageTk


VIDEO_EXTENSIONS = {".mp4", ".mov", ".avi", ".mkv", ".wmv", ".mpeg", ".mpg", ".m4v"}


class MediaGalleryApp(tk.Tk):
    def __init__(self, search_query=""):
        super().__init__()
        self.title("Rip-Off YouTube")
        self.geometry("1320x860")
        self.minsize(1100, 700)
        self.configure(bg="#0f172a")

        self.column_count = 4
        self.search_var = tk.StringVar(value=search_query)
        self.search_query = search_query.strip()
        self.media_items = [
            {
                "id": 1,
                "title": "Demo Clip 1",
                "path": "",
                "file_type": "video",
                "uploader": "Ava Brooks",
                "uploaded_at": datetime.now() - timedelta(minutes=18),
                "click_count": 42,
            },
            {
                "id": 2,
                "title": "Demo Clip 2",
                "path": "",
                "file_type": "video",
                "uploader": "Marcus Lee",
                "uploaded_at": datetime.now() - timedelta(minutes=52),
                "click_count": 71,
            },
            {
                "id": 3,
                "title": "Demo Clip 3",
                "path": "",
                "file_type": "video",
                "uploader": "Nina Patel",
                "uploaded_at": datetime.now() - timedelta(minutes=87),
                "click_count": 33,
            },
            {
                "id": 4,
                "title": "Demo Clip 4",
                "path": "",
                "file_type": "video",
                "uploader": "Leo Martinez",
                "uploaded_at": datetime.now() - timedelta(minutes=165),
                "click_count": 19,
            },
            {
                "id": 5,
                "title": "Demo Clip 5",
                "path": "",
                "file_type": "video",
                "uploader": "Sofia Nguyen",
                "uploaded_at": datetime.now() - timedelta(minutes=210),
                "click_count": 47,
            },
            {
                "id": 6,
                "title": "Demo Clip 6",
                "path": "",
                "file_type": "video",
                "uploader": "Ethan Ross",
                "uploaded_at": datetime.now() - timedelta(minutes=315),
                "click_count": 64,
            },
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

        self.search_frame = tk.Frame(self.toolbar, bg="#0f172a")
        self.search_frame.pack(side="left", expand=True, padx=24, fill="x")

        self.search_entry = tk.Entry(
            self.search_frame,
            textvariable=self.search_var,
            width=32,
            bg="#1e293b",
            fg="white",
            insertbackground="white",
            font=("Segoe UI", 11),
            relief="flat",
            highlightthickness=1,
            highlightbackground="#475569",
            highlightcolor="#60a5fa",
        )
        self.search_entry.pack(fill="x", padx=12, pady=6, ipady=8)
        self.search_entry.bind("<Return>", self.submit_search)
        self.search_entry.bind("<KP_Enter>", self.submit_search)

        self.search_placeholder = tk.Label(
            self.search_frame,
            text="Search...",
            fg="#94a3b8",
            bg="#1e293b",
            font=("Segoe UI", 11),
            padx=12,
        )
        self.search_placeholder.place(in_=self.search_entry, x=0, y=0, relwidth=1, relheight=1)
        self.search_entry.bind("<FocusIn>", self.hide_search_placeholder)
        self.search_entry.bind("<FocusOut>", self.show_search_placeholder_if_empty)
        self.search_entry.bind("<KeyRelease>", self.update_search_placeholder)

        self.show_search_placeholder_if_empty()

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

        self.sidebar = tk.Frame(self.main_frame, bg="#111827", width=220)
        self.sidebar.pack(side="left", fill="y", padx=16)
        self.sidebar.pack_propagate(False)

        sidebar_label = tk.Label(
            self.sidebar,
            text="Uploaders",
            fg="white",
            bg="#111827",
            font=("Segoe UI", 16, "bold"),
            pady=12,
        )
        sidebar_label.pack(fill="x")

        self.sidebar_list = tk.Frame(self.sidebar, bg="#111827")
        self.sidebar_list.pack(fill="both", expand=True, padx=10, pady=10)

        self.content_panel = tk.Frame(self.main_frame, bg="#0f172a")
        self.content_panel.pack(side="left", fill="both", expand=True)

        self.canvas = tk.Canvas(self.content_panel, bg="#0f172a", highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.content_panel, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.gallery = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.gallery, anchor="nw")
        self.gallery.bind("<Configure>", self._update_scroll_region)
        self.bind("<Configure>", self._update_scroll_region)

        self.refresh_sidebar()
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

    def format_minutes_ago(self, media):
        uploaded_at = media.get("uploaded_at")
        if uploaded_at is None:
            minutes = media.get("minutes_ago", 0)
        else:
            minutes = round((datetime.now() - uploaded_at).total_seconds() / 60)
            minutes = max(1, minutes)
        return minutes

    def get_filtered_media(self):
        query = self.search_var.get().strip().lower()
        if not query:
            return list(self.media_items)
        return [
            media
            for media in self.media_items
            if query in media["title"].lower() or query in media.get("uploader", "").lower()
        ]

    def submit_search(self, event=None):
        query = self.search_var.get().strip()
        if not query:
            self.refresh_gallery()
            return

        self.destroy()
        search_app = MediaGalleryApp(search_query=query)
        search_app.mainloop()

    def get_uploader_media(self, uploader_name):
        return [
            media for media in self.media_items if media.get("uploader", "Unknown") == uploader_name
        ]

    def open_uploader_window(self, uploader_name):
        uploader_media = self.get_uploader_media(uploader_name)
        uploader_window = tk.Toplevel(self)
        uploader_window.title(f"{uploader_name} - uploads")
        uploader_window.geometry("980x700")
        uploader_window.minsize(780, 520)
        uploader_window.configure(bg="#0f172a")

        header = tk.Label(
            uploader_window,
            text=f"{uploader_name}'s media",
            fg="white",
            bg="#0f172a",
            font=("Segoe UI", 22, "bold"),
            pady=14,
        )
        header.pack(fill="x")

        if not uploader_media:
            empty_label = tk.Label(
                uploader_window,
                text="No media uploaded yet.",
                fg="#cbd5e1",
                bg="#0f172a",
                font=("Segoe UI", 12),
                pady=20,
            )
            empty_label.pack()
            return

        canvas = tk.Canvas(uploader_window, bg="#0f172a", highlightthickness=0)
        scrollbar = ttk.Scrollbar(uploader_window, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True, padx=18, pady=18)
        scrollbar.pack(side="right", fill="y", pady=18)

        gallery = ttk.Frame(canvas)
        canvas.create_window((0, 0), window=gallery, anchor="nw")
        gallery.bind("<Configure>", lambda event: canvas.configure(scrollregion=canvas.bbox("all")))
        uploader_window.bind("<Configure>", lambda event: canvas.configure(scrollregion=canvas.bbox("all")))

        for col_index in range(self.column_count):
            gallery.columnconfigure(col_index, weight=1)

        for index, media in enumerate(uploader_media):
            row = index // self.column_count
            col = index % self.column_count
            self.create_media_card(gallery, media, row, col)

        uploader_window.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))

    def refresh_sidebar(self):
        for child in self.sidebar_list.winfo_children():
            child.destroy()

        uploader_names = sorted({media.get("uploader", "Unknown") for media in self.media_items})
        for name in uploader_names:
            uploader_button = tk.Button(
                self.sidebar_list,
                text=name,
                fg="#e2e8f0",
                bg="#111827",
                activebackground="#1f2937",
                activeforeground="white",
                anchor="w",
                justify="left",
                font=("Segoe UI", 10, "bold"),
                padx=8,
                pady=8,
                borderwidth=0,
                cursor="hand2",
                command=lambda selected_name=name: self.open_uploader_window(selected_name),
            )
            uploader_button.pack(fill="x", pady=2)

    def refresh_gallery(self):
        for child in self.gallery.winfo_children():
            child.destroy()

        filtered_media = self.get_filtered_media()

        for col_index in range(self.column_count):
            self.gallery.columnconfigure(col_index, weight=1)

        if not filtered_media:
            no_results = tk.Label(
                self.gallery,
                text="No media found",
                fg="#e2e8f0",
                bg="#0f172a",
                font=("Segoe UI", 20, "bold"),
                pady=30,
            )
            no_results.grid(row=0, column=0, columnspan=self.column_count, sticky="nsew")
            self.update_idletasks()
            self._update_scroll_region()
            return

        for index, media in enumerate(filtered_media):
            row = index // self.column_count
            col = index % self.column_count
            self.create_media_card(self.gallery, media, row, col)

        self.update_idletasks()
        self._update_scroll_region()

    def filter_gallery(self, event=None):
        self.refresh_gallery()
        self.update_search_placeholder(event)

    def hide_search_placeholder(self, event=None):
        if self.search_placeholder.winfo_exists():
            self.search_placeholder.place_forget()

    def show_search_placeholder_if_empty(self, event=None):
        if self.search_var.get() == "":
            if self.search_placeholder.winfo_exists():
                self.search_placeholder.place(in_=self.search_entry, x=0, y=0, relwidth=1, relheight=1)
        else:
            if self.search_placeholder.winfo_exists():
                self.search_placeholder.place_forget()

    def update_search_placeholder(self, event=None):
        if self.search_var.get() == "":
            self.search_placeholder.place(in_=self.search_entry, x=0, y=0, relwidth=1, relheight=1)
        else:
            self.search_placeholder.place_forget()

    def create_media_card(self, parent, media, row, col):
        card = tk.Frame(parent, bg="#1f2937", padx=10, pady=8, bd=0)
        card.grid(row=row, column=col, padx=10, pady=12, sticky="nsew")
        card.configure(cursor="hand2")

        def open_selected(event=None):
            media["click_count"] = media.get("click_count", 0) + 1
            self.refresh_gallery()
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

        minutes_ago = self.format_minutes_ago(media)
        metadata = f"{media.get('uploader', 'Unknown')} • {minutes_ago} min ago • {media.get('click_count', 0)} clicks"
        subtitle = tk.Label(
            card,
            text=metadata,
            bg="#1f2937",
            fg="#cbd5e1",
            anchor="w",
            justify="left",
            padx=4,
            pady=8,
            wraplength=220,
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
            messagebox.showerror("Unsupported file", "Please choose a valid video file.")
            return

        uploader_name = simpledialog.askstring("Uploader name", "Who uploaded this video?", initialvalue="Anonymous")
        if uploader_name is None:
            uploader_name = "Anonymous"
        uploader_name = uploader_name.strip() or "Anonymous"

        title = os.path.splitext(os.path.basename(file_path))[0]
        self.media_items.append(
            {
                "id": len(self.media_items) + 1,
                "title": title,
                "path": file_path,
                "file_type": "video",
                "uploader": uploader_name,
                "uploaded_at": datetime.now(),
                "click_count": 0,
            }
        )
        self.refresh_sidebar()
        self.refresh_gallery()

    def open_media_window(self, media):
        media["click_count"] = media.get("click_count", 0) + 1

        media_window = tk.Toplevel(self)
        media_window.title(f"{media['title']} - Video")
        media_window.geometry("940x640")
        media_window.minsize(700, 500)
        media_window.configure(bg="#020617")

        video_frame = tk.LabelFrame(media_window, text="Now playing", bg="#0f172a", fg="white", padx=10, pady=10)
        video_frame.pack(padx=18, pady=8, fill="both", expand=True)

        player_label = tk.Label(video_frame, bg="#111827", width=80, height=20)
        player_label.pack(fill="both", expand=True)

        controls = tk.Frame(media_window, bg="#020617")
        controls.pack(pady=10)

        rewind_button = tk.Button(
            controls,
            text="⏪ 5s",
            command=lambda: None,
            bg="#374151",
            fg="white",
            activebackground="#4b5563",
            font=("Segoe UI", 10, "bold"),
            padx=12,
            pady=8,
            borderwidth=0,
            cursor="hand2",
        )
        rewind_button.pack(side="left", padx=6)

        toggle_button = tk.Button(
            controls,
            text="Pause",
            command=lambda: None,
            bg="#2563eb",
            fg="white",
            activebackground="#1d4ed8",
            font=("Segoe UI", 10, "bold"),
            padx=16,
            pady=8,
            borderwidth=0,
            cursor="hand2",
        )
        toggle_button.pack(side="left", padx=6)

        skip_button = tk.Button(
            controls,
            text="5s ⏩",
            command=lambda: None,
            bg="#374151",
            fg="white",
            activebackground="#4b5563",
            font=("Segoe UI", 10, "bold"),
            padx=12,
            pady=8,
            borderwidth=0,
            cursor="hand2",
        )
        skip_button.pack(side="left", padx=6)

        full_button = tk.Button(
            controls,
            text="Full Screen",
            command=lambda: None,
            bg="#16a34a",
            fg="white",
            activebackground="#15803d",
            font=("Segoe UI", 10, "bold"),
            padx=14,
            pady=8,
            borderwidth=0,
            cursor="hand2",
        )
        full_button.pack(side="left", padx=6)

        progress_var = tk.DoubleVar(value=0)
        progress_bar = ttk.Progressbar(media_window, orient="horizontal", mode="determinate", length=720, variable=progress_var, maximum=100)
        progress_bar.pack(pady=12, padx=18, fill="x")

        info_row = tk.Frame(media_window, bg="#020617")
        info_row.pack(fill="x", padx=24, pady=18)

        heading = tk.Label(
            info_row,
            text=media["title"],
            fg="white",
            bg="#020617",
            font=("Segoe UI", 23, "bold"),
            anchor="w",
            justify="left",
        )
        heading.pack(side="left")

        minutes_ago = self.format_minutes_ago(media)
        details = tk.Label(
            info_row,
            text=(
                f"{media.get('uploader', 'Unknown')} • {minutes_ago} min ago • {media.get('click_count', 0)} clicks"
            ),
            wraplength=420,
            justify="left",
            bg="#020617",
            fg="#e2e8f0",
            font=("Segoe UI", 11),
            padx=18,
            pady=8,
        )
        details.pack(side="left", anchor="s")

        if media["path"]:
            self.start_video_playback(
                media["path"],
                player_label,
                toggle_button,
                rewind_button,
                skip_button,
                full_button,
                progress_bar,
                progress_var,
            )
        else:
            player_label.configure(text="Demo clip placeholder", fg="white", font=("Segoe UI", 18, "bold"))

    def start_video_playback(self, file_path, player_label, toggle_button, rewind_button, skip_button, full_button, progress_bar, progress_var):
        try:
            cap = cv2.VideoCapture(file_path)
        except Exception:
            player_label.configure(text="Unable to load video", fg="white", font=("Segoe UI", 16, "bold"))
            return

        player_label.video_capture = cap
        player_label.is_playing = True
        player_label.fullscreen_mode = False
        player_label.video_length = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        player_label.last_frame_time = 0

        window = player_label.master.winfo_toplevel()

        def toggle_playback():
            player_label.is_playing = not getattr(player_label, "is_playing", True)
            button_text = "Pause" if player_label.is_playing else "Play"
            toggle_button.configure(text=button_text)
            if player_label.is_playing:
                update_frame()

        def rewind_video():
            if not player_label.video_capture.isOpened():
                return
            current_pos = int(player_label.video_capture.get(cv2.CAP_PROP_POS_FRAMES))
            target = max(0, current_pos - 150)
            player_label.video_capture.set(cv2.CAP_PROP_POS_FRAMES, target)

        def skip_video():
            if not player_label.video_capture.isOpened():
                return
            current_pos = int(player_label.video_capture.get(cv2.CAP_PROP_POS_FRAMES))
            total_frames = int(player_label.video_length)
            target = min(total_frames - 1, current_pos + 150)
            player_label.video_capture.set(cv2.CAP_PROP_POS_FRAMES, target)

        def toggle_fullscreen():
            player_label.fullscreen_mode = not getattr(player_label, "fullscreen_mode", False)
            window.attributes("-fullscreen", player_label.fullscreen_mode)
            full_button.configure(text="Window" if player_label.fullscreen_mode else "Full Screen")

        toggle_button.configure(command=toggle_playback)
        rewind_button.configure(command=rewind_video)
        skip_button.configure(command=skip_video)
        full_button.configure(command=toggle_fullscreen)

        def update_frame():
            if not getattr(player_label, "is_playing", False):
                return

            if not player_label.video_capture.isOpened():
                player_label.configure(text="Video unavailable", fg="white", font=("Segoe UI", 16, "bold"))
                return

            ret, frame = player_label.video_capture.read()
            if not ret:
                player_label.video_capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
                ret, frame = player_label.video_capture.read()
                if not ret:
                    player_label.configure(text="Video ended", fg="white", font=("Segoe UI", 16, "bold"))
                    player_label.is_playing = False
                    toggle_button.configure(text="Play")
                    return

            if player_label.video_length > 0:
                current_frame = int(player_label.video_capture.get(cv2.CAP_PROP_POS_FRAMES))
                progress_value = (current_frame / player_label.video_length) * 100
                progress_var.set(progress_value)

            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(rgb)
            image = image.resize((720, 360), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(image=image)
            player_label.configure(image=photo)
            player_label.image = photo
            player_label.after(33, update_frame)

        player_label.after(33, update_frame)


if __name__ == "__main__":
    app = MediaGalleryApp()
    app.mainloop()
