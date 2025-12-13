import serial
import time
from threading import Thread
from re import search
from utils.settings_work import get_setting_by_key

class ScaleManager:
    _instance = None

    def __new__(cls, update_callback=None):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.ser = None
            cls._instance.update_callback = update_callback
            cls._instance._start_thread()
        else:
            # تحديث callback عند فتح واجهة جديدة
            cls._instance.update_callback = update_callback
        return cls._instance

    def _start_thread(self):
        Thread(target=self._worker, daemon=True).start()

    def _worker(self):
        while True:
            self._ensure_serial_connected()
            try:
                if self.ser and self.ser.in_waiting:
                    line = self.ser.readline().decode(errors="ignore").strip()
                    if line and self.update_callback:
                        weight_value = self._parse_weight(line)
                        if weight_value is not None:
                            # نحدث الوزن في الـ UI عبر after
                            self.update_callback(weight_value)
            except serial.SerialException:
                self.ser = None
            time.sleep(0.05)

    def _ensure_serial_connected(self):
        if self.ser and self.ser.is_open:
            return
        try:
            port = get_setting_by_key("scale_port") or "COM1"
            baudrate = int(get_setting_by_key("scale_baudrate") or 9600)
            self.ser = serial.Serial(
                port=port,
                baudrate=baudrate,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=1
            )
        except:
            self.ser = None
            time.sleep(3)

    def _parse_weight(self, data_line):
        # تنظيف السطر من الرموز الشائعة
        data_line = (
            data_line.replace("\x02", "")
                     .replace("\x03", "")
                     .replace("\r", "")
                     .replace("\n", "")
                     .replace("kg", "")
                     .replace("g", "")
                     .replace("KG", "")
                     .strip()
        )
        match = search(r"[-+]?\d*\.\d+|[-+]?\d+", data_line)
        if match:
            try:
                return float(match.group())
            except:
                return None
        return None
