from customtkinter import CTkLabel, CTkFrame, CTkEntry


class CompanySection:
    """Builds company info section (name, phone, email) and attaches entries to owner."""

    def __init__(self, owner):
        self.owner = owner

    def build(self):
        self.owner.company_title = CTkLabel(
            self.owner.main_frame,
            text="شركتك",
            font=("Arial", 24, "bold"),
            text_color=self.owner.text_color,
        )
        self.owner.company_title.pack(anchor="e", padx=10)
        CTkLabel(
            self.owner.main_frame,
            text="!سيتم عرض هذه البيانات في الفاتوره",
            text_color="#00b3ad",
            font=("Arial", 14)
        ).pack(anchor="e", pady=(4, 10), padx=10)

        self.owner.company_frame = CTkFrame(
            self.owner.main_frame,
            fg_color=self.owner.frame_bg,
            corner_radius=12,
        )
        self.owner.company_frame.pack(fill="x", pady=(0, 15))

        from utils.settings_work import get_setting_by_key

        company_name = get_setting_by_key("company_name") or ""
        company_phone = get_setting_by_key("company_phone") or ""
        company_email = get_setting_by_key("company_email") or ""
        company_address = get_setting_by_key("company_address") or ""

        self._create_text_field(": اسم الشركة", "company_name_entry", company_name)
        self._create_text_field(": رقم الهاتف", "company_phone_entry", company_phone)
        self._create_text_field(": البريد الإلكتروني", "company_email_entry", company_email)
        self._create_text_field(": عنوان الشركة", "company_address_entry", company_address)

    # ----------------------
    def _create_text_field(self, label_text, entry_name, initial_text=""):
        field_frame = CTkFrame(self.owner.company_frame, fg_color="transparent")
        field_frame.pack(fill="x", pady=8, padx=10)

        CTkLabel(field_frame, text=label_text, font=("Arial", 16),
                 text_color=self.owner.text_color).pack(anchor="e", pady=(0, 5))

        input_frame = CTkFrame(field_frame, fg_color="transparent")
        input_frame.pack(fill="x")

        entry = CTkEntry(
            input_frame,
            width=300,
            height=40,
            justify="right",
            font=("Arial", 16),
            fg_color="#475569",
            border_color=self.owner.primary_color,
            text_color=self.owner.text_color,
            placeholder_text_color="#94a3b8",
        )
        entry.pack(side="right", fill="x", expand=True)
        if initial_text:
            entry.insert(0, initial_text)

        setattr(self.owner, entry_name, entry)