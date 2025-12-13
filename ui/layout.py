from customtkinter import CTkFrame, CTkButton
from tkinter.messagebox import askokcancel
from utils.load_image import load_image
from utils.clear_frame import clear_frame
from ui.placeholderUI import PlaceholderUI
from ui.new_weights.new_weights_main import NewWeights
from ui.record_weights.record_weights import RecordWeights
from ui.reports.dashboard import ScaleDashboard
from ui.settings.settings import Settings

class Layout:
    def __init__(self, root):
        self.root = root
        self.main_frame = CTkFrame(self.root, fg_color="transparent", border_width=1, border_color="#3b82f6", corner_radius=12)
        self.main_frame.pack(expand=True, side="left", fill="both")

        self.tabs = [
            {"title": "وزنة جديده", "icon": "assets/وزنة جديده.png", "com": lambda: self.toggle_ui(NewWeights)},
            {"title": "سجل الأوزان", "icon": "assets/سجل الأوزان.png", "com": lambda: self.toggle_ui(RecordWeights)},
            {"title": "التقارير", "icon": "assets/التقارير.png", "com": lambda: self.toggle_ui(ScaleDashboard)},
            {"title": "الأعدادات", "icon": "assets/الأعدادات.png", "com": lambda: self.toggle_ui(Settings)}
        ]

        PlaceholderUI(self.main_frame)

        self.build_sidebar()
        
    def toggle_ui(self, target_ui):
        clear_frame(self.main_frame)
        target_ui(self.main_frame)

    def logout(self):
        if askokcancel("تسجيل الخروج", "هل تريد تسجيل الخروج"):
            self.root.quit()
    
    def build_sidebar(self):
        sidebar = CTkFrame(self.root)
        sidebar.pack(side="right", fill="y")

        button_style = {
            "font": ("Arial", 18),
            "fg_color": "#3b82f6",
            "hover_color": "#60a5fa",
            "corner_radius": 12,
            "height": 50
        }

        for tab in self.tabs:
            icon = load_image(tab["icon"])
            CTkButton(
                sidebar,
                text=tab["title"],
                image=icon,
                command=tab["com"],
                **button_style
            ).pack(padx=10, pady=8, fill="x")

        # Exit button
        exit_icon = load_image("assets/خروج.png")
        CTkButton(
            sidebar,
            text="خروج",
            image=exit_icon,
            command=self.logout,
            **button_style
        ).pack(padx=10, pady=15, side="bottom", fill="x")
