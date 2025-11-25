from customtkinter import CTkButton
from utils.load_image import load_image


class SaveSection:
    """Attach a single save button to owner.main_frame and wire settings saving."""

    def __init__(self, owner):
        self.owner = owner

    def build(self):
        save_settings_img = load_image("assets/حفظ الأعدادات.png")

        self.owner.save_btn = CTkButton(
            self.owner.main_frame,
            text="حفظ الإعدادات",
            image=save_settings_img,
            command=self.owner.save_settings,
            font=("Arial", 18, "bold"),
            fg_color=self.owner.primary_color,
            hover_color=self.owner.hover_color,
            height=50,
            corner_radius=10,
        )
        self.owner.save_btn.pack(side="bottom", pady=(20, 0))
