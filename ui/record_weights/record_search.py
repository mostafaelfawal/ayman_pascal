from customtkinter import CTkFrame, CTkEntry, CTkButton


class RecordSearch:
    """Builds the search bar for RecordWeights and exposes search_var.

    The owner is expected to implement `search_records` and provide `load_image` icons
    as needed (this keeps logic in owner but UI in this helper).
    """

    def __init__(self, owner):
        self.owner = owner

    def build(self):
        self.owner.search_frame = CTkFrame(self.owner.root, fg_color="#2d3748", corner_radius=15)
        self.owner.search_frame.pack(fill="x", padx=10, pady=5)

        search_container = CTkFrame(self.owner.search_frame, fg_color="transparent")
        search_container.pack(fill="x", padx=15, pady=8)

        CTkButton(
            search_container,
            text="بحث",
            image=self.owner.search_icon,
            corner_radius=20,
            font=("Arial", 14, "bold"),
            fg_color="#3b82f6",
            hover_color="#2563eb",
            command=self.owner.search_records,
            height=35,
            width=80
        ).pack(padx=(5, 10), pady=5, side="right")

        self.owner.search_var = CTkEntry(
            search_container,
            corner_radius=20,
            justify="right",
            font=("Arial", 14),
            height=35,
            border_width=2,
            border_color="#3b82f6",
            placeholder_text="🔍 ابحث بالاسم أو الكود...",
            fg_color="#1e293b",
            text_color="#e2e8f0"
        )
        self.owner.search_var.pack(fill="x", expand=True, padx=(0, 5), pady=5, side="right")
        self.owner.search_var.bind("<Return>", lambda e: self.owner.search_records())
