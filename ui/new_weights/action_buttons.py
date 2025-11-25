from customtkinter import CTkButton, CTkFrame
from utils.load_image import load_image

class ActionButtons:
    def __init__(self, parent, colors, main_font, actions):
        self.parent = parent
        self.colors = colors
        self.main_font = main_font
        self.actions = actions  # Dictionary of action functions
        self.build_action_buttons()
    
    def build_action_buttons(self):
        frame_style = {
            "corner_radius": 12,
            "border_width": 2,
            "border_color": "#3b82f6",
            "fg_color": "#1e293b"
        }
        
        frame = CTkFrame(self.parent, **frame_style)
        frame.pack(fill="x")

        buttons_frame = CTkFrame(frame, fg_color="transparent")
        buttons_frame.pack(padx=15, pady=15)

        buttons_config = [
            ("حفظ وطباعة", "assets/حفظ و طباعة.png", self.actions['save_and_print'], self.colors["purple"], self.colors["purple_hover"]),
            ("حفظ", "assets/حفظ.png", self.actions['save_scale'], self.colors["success"], self.colors["success_hover"]),
            ("طباعة", "assets/طباعة.png", self.actions['print_scale'], self.colors["warning"], self.colors["warning_hover"]),
            ("الغاء العملية", "assets/الغاء.png", self.actions['cancel_process'], self.colors["danger"], self.colors["danger_hover"])
        ]

        for text, img, command, color, hover_color in buttons_config:
            self._create_action_button(buttons_frame, text, img, command, color, hover_color)

    def _create_action_button(self, parent, text, image_path, command, color, hover_color):
        button = CTkButton(
            parent,
            text=text,
            image=load_image(image_path),
            font=self.main_font,
            fg_color=color,
            hover_color=hover_color,
            command=command,
            height=40,
            corner_radius=8,
            border_width=1,
            border_color="#334155"
        )
        button.pack(side="right", padx=5)