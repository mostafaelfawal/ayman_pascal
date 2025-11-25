from customtkinter import CTkLabel, CTkEntry, CTkFrame, StringVar

class ScaleDisplay:
    def __init__(self, parent, colors, title_font, digital_font):
        self.parent = parent
        self.colors = colors
        self.title_font = title_font
        self.digital_font = digital_font
        self.scale_var = StringVar(value="0.00")
        self.build_display()
    
    def build_display(self):
        display_frame = CTkFrame(
            self.parent, 
            corner_radius=12, 
            fg_color="#0f172a", 
            border_width=2, 
            border_color=self.colors["primary"]
        )
        display_frame.pack(padx=15, pady=10, fill="x")

        CTkLabel(
            display_frame, 
            text="الوزن الحالي", 
            font=self.title_font, 
            text_color=self.colors["text_primary"]
        ).pack(pady=5)

        self.weight_label = CTkEntry(
            display_frame,
            textvariable=self.scale_var,
            state="readonly",
            fg_color="transparent",
            border_width=0,
            justify="center",
            font=self.digital_font,
            text_color=self.colors["accent"]
        )
        self.weight_label.pack(fill="x", padx=10, pady=5)

        self.net_weight = CTkLabel(
            display_frame,
            text=f"الصافي = 0.00 كجم",
            font=("Arial", 12, "bold"),
            text_color=self.colors["muted"]
        )
        self.net_weight.pack(pady=(0, 2))
    
    def update_net_weight(self, w1, w2):
        try:
            if w1 > w2:
                net = w1 - w2
            else:
                net = w2 - w1
            self.net_weight.configure(text=f"الصافي = {net:.2f} كجم")
        except ValueError:
            self.net_weight.configure(text="الصافي = 0.00 كجم")