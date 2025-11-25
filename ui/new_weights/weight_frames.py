from customtkinter import CTkLabel, CTkEntry, CTkFrame, CTkButton
from datetime import datetime
from utils.load_image import load_image

class WeightFrames:
    def __init__(self, parent, colors, main_font, title_font, entries, update_net_callback):
        self.parent = parent
        self.colors = colors
        self.main_font = main_font
        self.title_font = title_font
        self.entries = entries
        self.update_net_callback = update_net_callback
        self.weight_frames = []
        self.build_weight_frames()
    
    def build_weight_frames(self):
        weights_container = CTkFrame(self.parent, fg_color="transparent")
        weights_container.pack(fill="x", pady=(0, 10))

        weight_data = [
            ("الوزنة الأولى", "weight1"),
            ("الوزنة الثانية", "weight2")
        ]

        for i, (title, key) in enumerate(weight_data):
            self._create_weight_frame(weights_container, title, key, i)

    def _create_weight_frame(self, parent, title, key, column):
        frame_style = {
            "corner_radius": 12,
            "border_width": 2,
            "border_color": "#3b82f6",
            "fg_color": "#1e293b"
        }
        
        frame = CTkFrame(parent, **frame_style)
        frame.grid(row=0, column=column, padx=5, sticky="nsew")
        parent.grid_columnconfigure(column, weight=1)

        CTkLabel(
            frame,
            text=title,
            font=self.title_font,
            text_color=self.colors["text_primary"]
        ).pack(pady=(10, 5))

        fields_frame = CTkFrame(frame, fg_color="transparent")
        fields_frame.pack(fill="x", padx=10, pady=5)

        self._create_weight_fields(fields_frame, key)
        self._create_capture_button(frame, key)

        self.weight_frames.append(frame)

    def _create_weight_fields(self, parent, key):
        self.entries[f"{key}_weight"] = CTkEntry(
            parent,
            placeholder_text="الوزن",
            font=self.main_font,
            justify="center",
            height=35,
            corner_radius=8
        )
        self.entries[f"{key}_weight"].pack(fill="x", pady=2)
        self.entries[f"{key}_weight"].bind("<KeyRelease>", self.update_net_callback)

        time_date_frame = CTkFrame(parent, fg_color="transparent")
        time_date_frame.pack(fill="x", pady=2)

        self.entries[f"{key}_date"] = CTkEntry(
            time_date_frame,
            placeholder_text="التاريخ",
            font=self.main_font,
            justify="center",
            height=35,
            corner_radius=8
        )
        self.entries[f"{key}_date"].pack(side="left", fill="x", expand=True, padx=(0, 2))

        self.entries[f"{key}_time"] = CTkEntry(
            time_date_frame,
            placeholder_text="الوقت",
            font=self.main_font,
            justify="center",
            height=35,
            corner_radius=8
        )
        self.entries[f"{key}_time"].pack(side="right", fill="x", expand=True, padx=(2, 0))

    def _create_capture_button(self, parent, key):
        weight_img = load_image("assets/التقاط الوزن.png", (20, 20))
        
        CTkButton(
            parent,
            text="التقاط الوزن",
            font=("Arial", 13, "bold"),
            fg_color=self.colors["primary"],
            hover_color=self.colors["primary_hover"],
            height=35,
            corner_radius=8,
            image=weight_img,
            command=lambda k=key: self.capture_weight(k)
        ).pack(padx=10, pady=10, fill="x")

    def capture_weight(self, key):
        now = datetime.now()
        self._fill_entry(f"{key}_weight", self.entries["scale_var"].get())
        self._fill_entry(f"{key}_date", now.strftime("%Y-%m-%d"))
        self._fill_entry(f"{key}_time", now.strftime("%H:%M:%S"))
        self.update_net_callback()

    def _fill_entry(self, field_key, value):
        if field_key in self.entries:
            self.entries[field_key].delete(0, "end")
            self.entries[field_key].insert(0, value)