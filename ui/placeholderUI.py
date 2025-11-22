from utils.load_image import load_image
from customtkinter import CTkLabel

class PlaceholderUI:
    def __init__(self, root):
        self.root = root
        # Load program icon
        icon = load_image("assets/icon.png", (200, 200))

        # Program Icon
        CTkLabel(self.root, image=icon, text="").pack(pady=10)

        # Title
        CTkLabel(
            self.root,
            text="لإدارة موازين باسكول",
            font=("Arial", 50, "bold"),
        ).pack(pady=20)

        # Copyright
        CTkLabel(
            self.root,
            text=f"2025 © جميع الحقوق محفوظة",
            font=("Arial", 18),
        ).pack(pady=5)

        # Version & Author
        CTkLabel(
            self.root,
            text="v1.0.0\nPowered By Mostafa Hamdi",
            text_color="#3b82f6",
            font=("Arial", 20),
        ).pack(pady=5)