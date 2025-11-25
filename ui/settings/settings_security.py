from customtkinter import CTkLabel, CTkFrame, CTkSwitch


class SecuritySection:
    """Builds and attaches the security section widgets to a Settings owner."""
    def __init__(self, owner):
        self.owner = owner

    def build(self):
        # section title
        self.owner.section_title = CTkLabel(
            self.owner.main_frame,
            text="إعدادات الأمان",
            font=("Arial", 24, "bold"),
            text_color=self.owner.text_color,
        )
        self.owner.section_title.pack(anchor="e", pady=(0, 20), padx=10)

        # security frame
        self.owner.security_frame = CTkFrame(
            self.owner.main_frame,
            fg_color=self.owner.frame_bg,
            corner_radius=12,
        )
        self.owner.security_frame.pack(fill="x", pady=(0, 15))

        # switch
        self.owner.sec_switch = CTkSwitch(
            self.owner.security_frame,
            text="تفعيل الحماية",
            variable=self.owner.is_security,
            command=self.owner.toggle_security,
            font=("Arial", 18, "bold"),
            fg_color=self.owner.primary_color,
            progress_color=self.owner.primary_color,
            button_color="#f8fafc",
            button_hover_color="#e2e8f0",
        )
        self.owner.sec_switch.pack(anchor="e", padx=15, pady=15)
