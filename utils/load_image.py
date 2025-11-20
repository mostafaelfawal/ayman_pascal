from PIL import Image
from customtkinter import CTkImage

def load_image(path: str, size: tuple = (40, 40)):
        """Load and return a CTkImage from file."""
        img = Image.open(path)
        return CTkImage(img, size=size)