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
        frame = CTkFrame(
            self.parent,
            corner_radius=12,
            border_width=2,
            border_color="#3b82f6",
            fg_color="#1e293b"
        )
        frame.pack(fill="x", pady=(0, 10))

        CTkLabel(
            frame,
            text="بيانات العملية",
            font=self.title_font,
            text_color=self.colors["text_primary"]
        ).pack(pady=(10, 5))

        container = CTkFrame(frame, fg_color="transparent")
        container.pack(fill="x", padx=15, pady=10)

        labels = [
            "اسم العميل",
            "رقم السيارة",
            "نوع الحمولة",
            "المحافظة"
        ]

        row = 0
        for label_text in labels:
            # Entry أولاً
            entry = CTkEntry(
                container,
                height=35,
                placeholder_text=f"...أدخل {label_text}",
                font=self.main_font,
                justify="right",
                corner_radius=8,
                border_width=1,
                border_color="#475569"
            )
            entry.grid(row=row, column=0, padx=(0, 10), pady=5, sticky="ew")
            self.entries[label_text] = entry

            # Label بعد Entry
            CTkLabel(
                container,
                text=f": {label_text}",
                font=self.main_font,
                text_color=self.colors["text_secondary"]
            ).grid(row=row, column=1, padx=(0, 10), pady=5, sticky="w")

            row += 1

        # جعل الأعمدة تتمدد بالتساوي
        container.grid_columnconfigure(0, weight=1)
