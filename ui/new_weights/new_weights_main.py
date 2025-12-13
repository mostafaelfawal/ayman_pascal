from customtkinter import CTkFrame
from tkinter.messagebox import askokcancel, showinfo, showerror, askquestion
from re import search
import serial
import time
from threading import Thread
from models.scale import ScaleDB
from utils.print_scale import print_scale
from utils.settings_work import get_setting_by_key
from utils.print_scale_thermal import print_scale_thermal
from ui.new_weights.scale_display import ScaleDisplay
from ui.new_weights.weight_frames import WeightFrames
from ui.new_weights.form_fields import FormFields
from ui.new_weights.action_buttons import ActionButtons

class NewWeights:
    def __init__(self, root):
        self.root = root
        self._setup_config()
        self._initialize_variables()
        self._start_serial_thread()
        self.build_ui()

    def _setup_config(self):
        self.main_font = ("Arial", 16, "bold")
        self.title_font = ("Arial", 20, "bold")
        self.digital_font = ("DS-Digital", 60)
        self.db = ScaleDB()
        
        self.colors = {
            "primary": "#3b82f6",
            "primary_hover": "#2563eb",
            "success": "#10b981",
            "success_hover": "#0da673",
            "warning": "#f59e0b",
            "warning_hover": "#bd7e10",
            "purple": "#8b5cf6",
            "purple_hover": "#6943c0",
            "danger": "#ef4444",
            "danger_hover": "#bf3636",
            "text_primary": "#60a5fa",
            "text_secondary": "#cbd5e1",
            "accent": "#22d3ee",
            "muted": "#94a3b8"
        }

    def _initialize_variables(self):
        self.is_last_weight = False
        self.entries = {}
        self.ser = None

    def build_ui(self):
        self.main_container = CTkFrame(self.root, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # بناء المكونات
        self.scale_display = ScaleDisplay(self.main_container, self.colors, self.title_font, self.digital_font)
        self.entries["scale_var"] = self.scale_display.scale_var
        
        self.weight_frames = WeightFrames(self.main_container, self.colors, self.main_font, self.title_font, self.entries, self.update_net_weight)
        
        self.form_fields = FormFields(self.main_container, self.colors, self.main_font, self.title_font, self.entries)
        
        actions = {
            'save_and_print': lambda: self.save_and_print(),
            'save_scale': lambda: self.save_scale(),
            'print_scale': lambda: self.chiose_printer_type(),
            'cancel_process': lambda: self.cancel_process()
        }
        self.action_buttons = ActionButtons(self.main_container, self.colors, self.main_font, actions)

    def update_net_weight(self, event=None):
        try:
            w1 = float(self.entries["weight1_weight"].get() or 0)
            w2 = float(self.entries["weight2_weight"].get() or 0)
            self.scale_display.update_net_weight(w1, w2)
        except ValueError:
            self.scale_display.net_weight.configure(text="الصافي = 0.00 كجم")

    def cancel_process(self):
        if askokcancel("الغاء العملية", "سيتم الغاء العملية ولن يمكنك التراجع.\nهل أنت متأكد؟"):
            self.clear_all()
            
    def clear_all(self):
        for entry in self.entries.values():
            if hasattr(entry, 'delete'):
                entry.delete(0, "end")

        self.scale_display.scale_var.set("0.00")

        # 🔴 إعادة تهيئة اتصال الميزان
        if self.ser:
            try:
                self.ser.reset_input_buffer()
                self.ser.reset_output_buffer()
            except:
                pass

    def save_scale(self, delete_feild=True):
        for entry in self.entries.values():
            if hasattr(entry, 'get') and entry.get() == "":
                showerror("خطأ", f"يجب ملأ جميع الحقول")
                return False
        
        self.db.add_scale(
            self.entries["اسم العميل"].get(),
            self.entries["نوع الحمولة"].get(),
            self.entries["رقم السيارة"].get(),
            self.entries["المحافظة"].get(),
            self.entries["weight1_time"].get(),
            self.entries["weight1_date"].get(),
            self.entries["weight1_weight"].get(),
            self.entries["weight2_time"].get(),
            self.entries["weight2_date"].get(),
            self.entries["weight2_weight"].get(),
            self.entries["السعر"].get()
            )
        showinfo("تم", "تم حفظ الوزنة بنجاح")
        if delete_feild:
            self.clear_all()

        if self.ser:
            try:
                self.ser.close()
            except:
                pass
            self.ser = None
        return True
                
    def save_and_print(self):
        if self.save_scale(False):
            self.chiose_printer_type()
            self.clear_all()

    def chiose_printer_type(self):
        answer = askquestion("اختيار نوع الطابعة", "هل الطابعة عادية؟")

        if answer == 'yes':
            print_scale(self.entries, self.scale_display.net_weight)
        else:
            INV_num = self.db.get_invoice_num()
            print_scale_thermal(self.entries, INV_num)

    
    def _start_serial_thread(self):
        Thread(target=self._serial_worker, daemon=True).start()

    def _serial_worker(self):
        while True:
            self._ensure_serial_connected()

            try:
                if self.ser and self.ser.in_waiting:
                    line = self.ser.readline().decode().strip()
                    if line:
                        self._process_scale_data(line)
            except serial.SerialException:
                self.ser = None

            time.sleep(0.05)

    def _ensure_serial_connected(self):
        if self.ser:
            if self.ser.is_open:
                return
            else:
                try:
                    self.ser.close()
                except:
                    pass
                self.ser = None

        try:
            port = get_setting_by_key("scale_port") or "COM1"
            scale_baudrate = int(get_setting_by_key("scale_baudrate") or 9600)
            self.ser = serial.Serial(
                port=port,
                baudrate=scale_baudrate,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=1
            )
        except Exception as e:
            self.ser = None
            time.sleep(3)

    def _process_scale_data(self, data_line):
        if not data_line:
            return

        # 1) تنظيف السطر من الرموز الشائعة في الموازين
        data_line = (
            data_line.replace("\x02", "")  # STX
                    .replace("\x03", "")  # ETX
                    .replace("\r", "")
                    .replace("\n", "")
                    .replace("kg", "")
                    .replace("g", "")
                    .replace("KG", "")
                    .strip()
        )

        # 2) استخراج الرقم من أي صيغة (ينجح مع معظم الموازين)
        match = search(r"[-+]?\d*\.\d+|[-+]?\d+", data_line)
        if not match:
            return

        try:
            weight_value = float(match.group())
            self.root.after(0, lambda: 
                self.scale_display.scale_var.set(f"{weight_value:.2f}")
            )
        except:
            pass