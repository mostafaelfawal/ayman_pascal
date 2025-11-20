from utils.load_image import load_image
from customtkinter import CTkLabel, CTkFrame
from time import strftime

class PlaceholderUI:
    def __init__(self, root):
        self.root = root
        self.year = strftime("%Y")
        # Load program icon
        icon = load_image("assets/icon.png", (200, 200))

        # Program Icon
        CTkLabel(self.root, image=icon, text="").pack(pady=10)

        # Title
        CTkLabel(
            self.root,
            text="لإدارة موازين باسكال",
            font=("Arial", 50, "bold"),
        ).pack(pady=20)

        # Copyright
        CTkLabel(
            self.root,
            text=f"{self.year} © جميع الحقوق محفوظة",
            font=("Arial", 18),
        ).pack(pady=5)

        # Version & Author
        CTkLabel(
            self.root,
            text="v1.0.0\nPowered By Mostafa Hamdi",
            text_color="#3b82f6",
            font=("Arial", 20),
        ).pack(pady=5)