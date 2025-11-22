from customtkinter import (
    CTkLabel, CTkEntry, CTkFrame, CTkButton,
    StringVar, CTkTextbox
)
from tkinter.messagebox import askokcancel
from datetime import datetime
import serial
import time
from threading import Thread
from utils.load_image import load_image


class RecordingWeights:
    def __init__(self, root):
        self.root = root
        self.main_font = ("Arial", 20, "bold")
        self.is_last_weight = False
        self.scale_var = StringVar(value="0.00")

        # Style config
        self.frame_style = {
            "corner_radius": 12,
            "border_width": 1,
            "border_color": "#3b82f6"
        }

        # تخزين حقول الإدخال
        self.entries = {}

        # تشغيل قراءة الميزان في الخلفية
        self.start_serial_thread()

        # بناء الواجهة
        self.build_ui()

    def build_ui(self):
        self.build_scale_display()
        self.build_form_fields()
        self.build_action_buttons()

    # -----------------------------
    # شاشة الوزن الرقمية
    # -----------------------------
    def build_scale_display(self):
        frame = CTkFrame(self.root, **self.frame_style)
        frame.pack(fill="x", padx=10, pady=10)

        CTkLabel(frame, text="الوزن الحالي", font=("Arial", 22, "bold")).pack(pady=5)

        display = CTkFrame(frame, corner_radius=12, fg_color="black")
        display.pack(padx=20, pady=10, fill="x")

        self.weight_label = CTkEntry(
            display, textvariable=self.scale_var, state="readonly",
            fg_color="transparent", border_width=0, justify="center",
            font=("DS-Digital", 80), text_color="#32ff32"
        )
        self.weight_label.pack(pady=10, fill="x")

        CTkButton(
            display,
            text="التقاط الوزن",
            image=load_image("assets/التقاط الوزن.png"),
            font=self.main_font,
            fg_color="#3b82f6",
            hover_color="#60a5fa",
            command=self.get_scale
        ).pack(pady=10)

    # -----------------------------
    # نموذج الإدخال
    # -----------------------------
    def build_form_fields(self):
        frame = CTkFrame(self.root, **self.frame_style)
        frame.pack(pady=10, padx=10, fill="x")

        fields = [
            ("اسم العميل", 0, 0),
            ("رقم السيارة", 0, 2),
            ("نوع الحموله", 1, 0),
            ("المحافظة", 1, 2),
            ("التاريخ", 2, 0),
            ("الوقت", 2, 2),
            ("الوزن", 3, 0),
            ("ملاحظات", 4, 0)
        ]

        for label_text, row, col in fields:
            self.create_field(frame, label_text, row, col)

    def create_field(self, parent, text, row, col):
        """ينشئ حقل (Label + Entry/Textbox)"""

        CTkLabel(parent, text=f":{text}", font=self.main_font)\
            .grid(row=row, column=col+1, padx=10, pady=7, sticky="e")

        # Textbox
        if text == "ملاحظات":
            widget = CTkTextbox(parent, width=250, height=80, font=self.main_font)
            widget.grid(row=row, column=col, padx=10, pady=7, sticky="w", columnspan=3)

        else:  # Entry
            widget = CTkEntry(
                parent, width=250,
                placeholder_text="..." + text,
                font=self.main_font,
                justify="right"
            )
            widget.grid(row=row, column=col, padx=10, pady=7, sticky="w")

        self.entries[text] = widget

    # -----------------------------
    # أزرار الإجراءات
    # -----------------------------
    def build_action_buttons(self):
        frame = CTkFrame(self.root, **self.frame_style)
        frame.pack(fill="x", padx=10, pady=10)

        buttons = [
            ("حفظ", "assets/حفظ.png", None, self.is_last_weight),
            ("طباعة", "assets/طباعة.png", None, self.is_last_weight),
            ("حفظ و طباعة", "assets/حفظ و طباعة.png", None, self.is_last_weight),
            ("الوزنة الثانية", "assets/الوزنة الثانية.png", None, not self.is_last_weight),
            ("الغاء العملية", "assets/الغاء.png", self.cancel_process, True)
        ]

        for text, img, cmd, disabled in buttons:
            CTkButton(
                frame,
                text=text,
                image=load_image(img),
                font=self.main_font,
                fg_color="#3b82f6",
                hover_color="#60a5fa",
                command=cmd,
                state="normal" if disabled else "disabled"
            ).pack(side="right", padx=10, pady=10)

    # ====================================================
    # Logic
    # ====================================================
    def get_scale(self):
        """تعبئة الوزن والتاريخ والوقت تلقائيًا."""
        now = datetime.now()

        self.fill_entry("الوزن", self.scale_var.get())
        self.fill_entry("التاريخ", now.strftime("%Y-%m-%d"))
        self.fill_entry("الوقت", now.strftime("%H:%M:%S"))

    def fill_entry(self, field, value):
        """Helper: تعبئة أي حقل."""
        entry = self.entries[field]
        if isinstance(entry, CTkTextbox):
            entry.delete("1.0", "end")
            entry.insert("1.0", value)
        else:
            entry.delete(0, "end")
            entry.insert(0, value)

    def cancel_process(self):
        """مسح الحقول بعد التأكيد."""
        if askokcancel("الغاء العملية", "سيتم الغاء العملية ولن يمكنك التراجع."):
            for widget in self.entries.values():
                if isinstance(widget, CTkTextbox):
                    widget.delete("1.0", "end")
                else:
                    widget.delete(0, "end")

    # ====================================================
    # Serial Reader
    # ====================================================
    def start_serial_thread(self):
        Thread(target=self.serial_worker, daemon=True).start()

    def serial_worker(self):
        """قراءة الميزان بشكل مستمر"""
        while True:
            self.ensure_serial_connected()

            try:
                line = self.ser.readline().decode().strip()
                if line:
                    self.process_scale_line(line)
            except serial.SerialException:
                self.ser = None

            time.sleep(0.05)

    def ensure_serial_connected(self):
        """محاولة فتح منفذ الميزان"""
        if hasattr(self, "ser") and self.ser:
            return

        try:
            self.ser = serial.Serial(
                port="COM1",
                baudrate=9600,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=1
            )
            print("scale connected")
        except Exception:
            time.sleep(3)

    def process_scale_line(self, line):
        """تنظيف واستخراج الوزن"""
        parts = line.split(",")
        if len(parts) < 3:
            return

        cleaned = parts[2].replace("+", "").replace("kg", "").strip()

        try:
            weight = float(cleaned)
            self.root.after(0, lambda: self.scale_var.set(f"{weight:.2f}"))
        except:
            pass