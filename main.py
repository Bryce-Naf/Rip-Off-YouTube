import tkinter as tk
from tkinter import ttk


class MediaGalleryApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Rip-Off YouTube")
        self.geometry("1220x820")
        self.minsize(900, 600)
        self.configure(bg="#0f172a")

        self.media_items = [
            {"id": i, "title": f"Media {i}"}
            for i in range(1, 25)
        ]

        main_frame = ttk.Frame(self, padding=20)
        main_frame.pack(fill="both", expand=True)

        header = ttk.Label(
            main_frame,
            text="Media Library",
            font=("Segoe UI", 24, "bold"),
        )
        header.pack(anchor="w", pady=(0, 18))

        self.canvas = tk.Canvas(
            main_frame,
            bg="#0f172a",
            highlightthickness=0,
        )
        self.scrollbar = ttk.Scrollbar(
            main_frame,
            orient="vertical",
            command=self.canvas.yview,
        )
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.gallery = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.gallery, anchor="nw")

        columns = 4
        for col_index in range(columns):
            self.gallery.columnconfigure(col_index, weight=1)

        for index, media in enumerate(self.media_items):
            row = index // columns
            col = index % columns
            self.create_media_card(self.gallery, media, row, col)

        self.gallery.bind("<Configure>", self._update_scroll_region)
        self.bind("<Configure>", self._update_scroll_region)

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
        ]
        return palette[(media_id - 1) % len(palette)]

    def create_media_card(self, parent, media, row, col):
        card = tk.Frame(parent, bg="#1f2937", padx=12, pady=12, bd=0)
        card.grid(row=row, column=col, padx=12, pady=12, sticky="nsew")
        card.configure(cursor="hand2")

        def on_enter(event):
            card.configure(bg="#374151")

        def on_leave(event):
            card.configure(bg="#1f2937")

        def open_selected(event=None):
            self.open_media_window(media)

        card.bind("<Button-1>", open_selected)
        card.bind("<Enter>", on_enter)
        card.bind("<Leave>", on_leave)

        thumbnail = tk.Canvas(
            card,
            width=250,
            height=160,
            bg=self.get_card_color(media["id"]),
            highlightthickness=0,
        )
        thumbnail.pack(fill="x")
        thumbnail.bind("<Button-1>", open_selected)
        thumbnail.bind("<Enter>", on_enter)
        thumbnail.bind("<Leave>", on_leave)

        thumbnail.create_rectangle(
            18, 18, 232, 142,
            fill="#111827",
            outline="#475569",
            width=2,
        )
        thumbnail.create_text(
            125,
            80,
            text=f"MEDIA\n{media['id']}",
            fill="white",
            font=("Segoe UI", 18, "bold"),
        )

        title = tk.Label(
            card,
            text=media["title"],
            bg="#1f2937",
            fg="white",
            font=("Segoe UI", 12, "bold"),
            padx=4,
            pady=8,
            anchor="w",
        )
        title.pack(fill="x")
        title.bind("<Button-1>", open_selected)
        title.bind("<Enter>", on_enter)
        title.bind("<Leave>", on_leave)

        subtitle = tk.Label(
            card,
            text=f"Video • {media['id']}",
            bg="#1f2937",
            fg="#cbd5e1",
            padx=4,
            pady=8,
            anchor="w",
        )
        subtitle.pack(fill="x")
        subtitle.bind("<Button-1>", open_selected)
        subtitle.bind("<Enter>", on_enter)
        subtitle.bind("<Leave>", on_leave)

    def open_media_window(self, media):
        media_window = tk.Toplevel(self)
        media_window.title(f"{media['title']} - Player")
        media_window.geometry("920x620")
        media_window.minsize(700, 500)
        media_window.configure(bg="#020617")

        heading = tk.Label(
            media_window,
            text=media["title"],
            fg="white",
            bg="#020617",
            font=("Segoe UI", 22, "bold"),
        )
        heading.pack(pady=(18, 12))

        player_canvas = tk.Canvas(
            media_window,
            width=720,
            height=380,
            bg=self.get_card_color(media["id"]),
            highlightthickness=0,
        )
        player_canvas.pack(pady=8)
        player_canvas.create_rectangle(
            25, 25, 695, 355,
            fill="#0f172a",
            outline="#475569",
            width=3,
        )
        player_canvas.create_text(
            360,
            170,
            text=f"Playing\n{media['title']}",
            fill="white",
            font=("Segoe UI", 28, "bold"),
        )
        player_canvas.create_text(
            360,
            230,
            text="Unique video player for this selected media item",
            fill="#cbd5e1",
            font=("Segoe UI", 13),
        )

        details = tk.Label(
            media_window,
            text=(
                f"This window is ready to load a unique video for item {media['id']}. "
                "Replace this placeholder with the actual media file you upload."
            ),
            wraplength=700,
            justify="left",
            bg="#020617",
            fg="#e2e8f0",
            font=("Segoe UI", 11),
        )
        details.pack(padx=20, pady=(0, 18))


if __name__ == "__main__":
    app = MediaGalleryApp()
    app.mainloop()
