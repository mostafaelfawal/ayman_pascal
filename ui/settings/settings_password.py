from customtkinter import CTkFrame, CTkLabel, CTkEntry, CTkButton


class PasswordSection:
    """Builds the password-change UI and attaches inputs to the Settings owner.

    The logic (checking/saving) stays in the owner; this class only creates
    widgets and wires their commands to owner methods.
    """

    def __init__(self, owner):
        self.owner = owner

    def build(self):
        # create the container frame inside the security frame
        self.owner.pass_frame = CTkFrame(self.owner.security_frame, fg_color="transparent")

        # title
        title_frame = CTkFrame(self.owner.pass_frame, fg_color="transparent")
        title_frame.pack(fill="x", pady=(0, 15), padx=10)

        CTkLabel(
            title_frame,
            text="تغيير كلمة المرور",
            font=("Arial", 18, "bold"),
            text_color=self.owner.text_color,
        ).pack(anchor="e")

        # old password field + verify button
        self._create_password_field(": كلمة المرور القديمة", "old_pass_entry", verify=True)

        # new password field
        self._create_password_field(": كلمة المرور الجديدة", "new_pass_entry", verify=False)

        # action buttons (change / cancel)
        self._create_action_buttons()

    def _create_password_field(self, label_text, entry_name, verify=False):
        field_frame = CTkFrame(self.owner.pass_frame, fg_color="transparent")
        field_frame.pack(fill="x", pady=8, padx=10)

        CTkLabel(field_frame, text=label_text, font=("Arial", 16), text_color=self.owner.text_color).pack(anchor="e", pady=(0, 5))

        input_frame = CTkFrame(field_frame, fg_color="transparent")
        input_frame.pack(fill="x")

        entry = CTkEntry(
            input_frame,
            width=300,
            height=40,
            justify="right",
            show="•",
            font=("Arial", 16),
            fg_color="#475569",
            border_color=self.owner.primary_color,
            text_color=self.owner.text_color,
            placeholder_text_color="#94a3b8",
        )
        entry.pack(side="right", fill="x", expand=True)

        setattr(self.owner, entry_name, entry)

        if verify:
            CTkButton(
                input_frame,
                text="تحقق",
                command=self.owner.check_old_password,
                font=("Arial", 14, "bold"),
                fg_color=self.owner.primary_color,
                hover_color=self.owner.hover_color,
                height=40,
                width=80,
            ).pack(side="right", padx=10)

    def _create_action_buttons(self):
        buttons_frame = CTkFrame(self.owner.pass_frame, fg_color="transparent")
        buttons_frame.pack(anchor="e", pady=15)

        self.owner.change_btn = CTkButton(
            buttons_frame,
            text="تغيير كلمة المرور",
            command=self.owner.change_password,
            font=("Arial", 16, "bold"),
            fg_color=self.owner.primary_color,
            hover_color=self.owner.hover_color,
            height=45,
            width=150,
        )
        self.owner.change_btn.pack(side="right", padx=10)

        self.owner.cancel_btn = CTkButton(
            buttons_frame,
            text="إلغاء",
            command=self.owner.cancel_process,
            font=("Arial", 16),
            fg_color="#64748b",
            hover_color="#475569",
            height=45,
            width=100,
        )
        self.owner.cancel_btn.pack(side="right")
