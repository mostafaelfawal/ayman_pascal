from customtkinter import CTkLabel, CTkFrame, CTkEntry, CTkOptionMenu
from utils.check_ports import get_serial_ports
from utils.settings_work import get_setting_by_key


class ScaleSection:
    """Builds scale/serial settings UI: port selector + baudrate input.

    - Populates the OptionMenu with values from check_ports.get_serial_ports()
    - Loads saved values (scale_port, scale_baudrate) from settings.json
    - Attaches widgets to the owner so Settings.save_settings can read them
    """

    def __init__(self, owner):
        self.owner = owner

    def build(self):
        # title
        CTkLabel(self.owner.main_frame, text="إعدادات الميزان", font=("Arial", 24, "bold"), text_color=self.owner.text_color).pack(anchor="e", pady=(10, 8), padx=10)

        # explanatory hint about baudrate
        CTkLabel(self.owner.main_frame, text=".يمكنك اختيار منفذ USB/COM الذي يتصل به الميزان، وأدخل سرعة النقل (معدل البود)", text_color="#cbd5e1", font=("Arial", 13)).pack(anchor="e", padx=10)

        # container
        self.frame = CTkFrame(self.owner.main_frame, fg_color=self.owner.frame_bg, corner_radius=12)
        self.frame.pack(fill="x", pady=(10, 15))

        # available ports
        available = get_serial_ports()

        # load saved settings (fallback sensible defaults)
        selected_port = get_setting_by_key("scale_port") if get_setting_by_key("scale_port") is not None else (available[0] if available else "")
        saved_baud = get_setting_by_key("scale_baudrate") or "9600"

        # option menu for ports
        self.owner.scale_port_option = CTkOptionMenu(self.frame, values=available or ["(لا توجد منافذ متاحة)"], width=400)
        if selected_port in available:
            self.owner.scale_port_option.set(selected_port)
        else:
            # If saved port not present, show hint
            if selected_port:
                self.owner.scale_port_option.set(selected_port + "  (غير موصول حاليا)")
            else:
                self.owner.scale_port_option.set(available[0] if available else "(لا توجد منافذ متاحة)")
        self.owner.scale_port_option.pack(anchor="e", padx=12, pady=(12, 8))

        # baudrate field + hint
        CTkLabel(self.frame, text=":Baud Rate - سرعة البود", font=("Arial", 14), text_color=self.owner.text_color).pack(anchor="e", padx=12, pady=(6, 0))

        self.owner.scale_baud_entry = CTkEntry(self.frame, width=240, height=40, justify="center", font=("Arial", 16))
        self.owner.scale_baud_entry.pack(anchor="e", padx=12, pady=(6, 12))
        self.owner.scale_baud_entry.insert(0, str(saved_baud))

        # friendly help: how to find Baud Rate on the scale
        CTkLabel(self.frame, text="كيف تعرف سرعة البود من الميزان؟\n عادة يكون في دليل المستخدم أو قائمة إعدادات الميزان،\n أو اطبع مواصفات الشركة. إذا لم تعرفه جرب 9600 أو 115200.", text_color="#94a3b8", font=("Arial", 12)).pack(anchor="e", padx=12, pady=(0, 8))
