from customtkinter import CTkLabel

class RecordWeights:
    def __init__(self, root):
        self.root = root
        CTkLabel(self.root, text="Hello from RecordWeights!").pack()