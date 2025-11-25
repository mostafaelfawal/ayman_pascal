from customtkinter import CTkFrame, CTkButton


class RecordActions:
    """Builds the bottom action buttons for records list and wires owner callbacks."""

    def __init__(self, owner):
        self.owner = owner

    def build(self):
        action_frame = CTkFrame(self.owner.root, fg_color="#2d3748", corner_radius=15)
        action_frame.pack(fill="x", padx=10, pady=10)

        buttons_container = CTkFrame(action_frame, fg_color="transparent")
        buttons_container.pack(padx=15, pady=8)

        CTkButton(
            buttons_container,
            text="حذف الوزنة",
            image=self.owner.delete_icon,
            command=self.owner.delete_weight,
            font=("Arial", 16, "bold"),
            fg_color="#ef4444",
            hover_color="#dc2626",
            border_color="#fecaca",
            border_width=1,
            height=40,
            width=120
        ).pack(side="right", padx=8, pady=5)

        CTkButton(
            buttons_container,
            text="تعديل الوزنة",
            image=self.owner.edit_icon,
            command=self.owner.edit_weight,
            font=("Arial", 16, "bold"),
            fg_color="#3b82f6",
            hover_color="#2563eb",
            border_color="#93c5fd",
            border_width=1,
            height=40,
            width=120
        ).pack(side="right", padx=8, pady=5)

        CTkButton(
            buttons_container,
            text="وزنة جديدة",
            image=self.owner.add_icon,
            command=self.owner.to_new_record,
            font=("Arial", 16, "bold"),
            fg_color="#10b981",
            hover_color="#059669",
            border_color="#a7f3d0",
            border_width=1,
            height=40,
            width=120
        ).pack(side="right", padx=8, pady=5)

        CTkButton(
            buttons_container,
            text="تحديث البيانات",
            command=self.owner.reload_treeview,
            font=("Arial", 16, "bold"),
            fg_color="#8b5cf6",
            hover_color="#7c3aed",
            border_color="#ddd6fe",
            image=self.owner.update_data,
            border_width=1,
            height=40,
            width=120
        ).pack(side="left", padx=8, pady=5)
