from customtkinter import CTkLabel, CTkEntry, CTkFrame

class FormFields:
    def __init__(self, parent, colors, main_font, title_font, entries):
        self.parent = parent
        self.colors = colors
        self.main_font = main_font
        self.title_font = title_font
        self.entries = entries
        self.build_form_fields()
    
    def build_form_fields(self):
        frame_style = {
            "corner_radius": 12,
            "border_width": 2,
            "border_color": "#3b82f6",
            "fg_color": "#1e293b"
        }
        
        frame = CTkFrame(self.parent, **frame_style)
        frame.pack(fill="x", pady=(0, 10))

        CTkLabel(
            frame,
            text="بيانات العملية",
            font=self.title_font,
            text_color=self.colors["text_primary"]
        ).pack(pady=(10, 5))

        form_container = CTkFrame(frame, fg_color="transparent")
        form_container.pack(fill="x", padx=15, pady=10)

        form_fields = [
            ("اسم العميل", 0),
            ("رقم السيارة", 1),
            ("نوع الحمولة", 2),
            ("المحافظة", 3),
        ]

        for label_text, row in form_fields:
            self._create_form_field(form_container, label_text, row)

    def _create_form_field(self, parent, text, row):
        widget = CTkEntry(
            parent,
            height=35,
            placeholder_text=f"...أدخل {text}",
            font=self.main_font,
            justify="right",
            corner_radius=8,
            border_width=1,
            border_color="#475569"
        )
        widget.grid(row=row, column=0, padx=(0, 10), pady=5, sticky="ew")

        self.entries[text] = widget

        CTkLabel(
            parent,
            text=f":{text}",
            font=self.main_font,
            text_color=self.colors["text_secondary"]
        ).grid(row=row, column=1, padx=(10, 0), pady=5, sticky="w")

        parent.grid_columnconfigure(0, weight=3)
        parent.grid_columnconfigure(1, weight=1)