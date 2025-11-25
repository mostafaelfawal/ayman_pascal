from customtkinter import CTkFrame, CTkScrollbar
from tkinter.ttk import Treeview, Style


class RecordTree:
    """Builds the treeview and provides helpers to (re)load rows.

    This attaches `tree` to the owner.
    """

    def __init__(self, owner):
        self.owner = owner

    def build(self):
        tree_container = CTkFrame(self.owner.container, fg_color="#1e293b", corner_radius=15)
        tree_container.pack(fill="both", expand=True, padx=5, pady=5)

        tree_scrollbar = CTkScrollbar(
            tree_container,
            orientation="vertical",
            button_color="#3b82f6",
            button_hover_color="#2563eb",
            fg_color="#1e293b"
        )
        tree_scrollbar.pack(side="right", fill="y")

        self.owner.tree = Treeview(
            tree_container,
            columns=("الكود", "اسم العميل", "نوع الحمولة", "الوزن الأول", "الوزن الثاني"),
            show="headings",
            yscrollcommand=tree_scrollbar.set,
            height=12
        )
        self.owner.tree.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        tree_scrollbar.configure(command=self.owner.tree.yview)

        columns_list = [
            {"title": "الكود", "width": 80},
            {"title": "اسم العميل", "width": 180},
            {"title": "نوع الحمولة", "width": 250},
            {"title": "الوزن الأول", "width": 120},
            {"title": "الوزن الثاني", "width": 120},
        ]

        for col in columns_list:
            self.owner.tree.heading(col["title"], text=col["title"])
            self.owner.tree.column(col["title"], width=col["width"], anchor="center")

        self.owner.tree.bind("<ButtonRelease-1>", self.owner.on_tree_click)
        self.owner.tree.bind("<Double-1>", lambda e: self.owner.edit_weight())

        self.apply_theme()

    def apply_theme(self):
        style = Style()
        style.theme_use('clam')

        style.configure(
            "Dark.Treeview.Heading",
            background="#3b82f6",
            foreground="#ffffff",
            relief="flat",
            borderwidth=0,
            font=("Arial", 12, "bold"),
            focuscolor="none"
        )

        style.configure(
            "Dark.Treeview",
            background="#1e293b",
            foreground="#e2e8f0",
            fieldbackground="#1e293b",
            borderwidth=0,
            rowheight=35,
            font=("Arial", 11)
        )

        style.map(
            "Dark.Treeview",
            background=[('selected', '#3b82f6')],
            foreground=[('selected', '#ffffff')]
        )

        style.map(
            "Dark.Treeview.Heading",
            background=[('active', '#2563eb')],
            relief=[('active', 'flat')]
        )

        self.owner.tree.configure(style="Dark.Treeview")
