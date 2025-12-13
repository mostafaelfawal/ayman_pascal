from customtkinter import CTkLabel, CTkFrame, CTkEntry, CTkOptionMenu
from utils.print_utils import get_system_printers
from utils.settings_work import get_setting_by_key


class PrinterSection:
    """Printer settings: select printer, choose type and invoices count."""

    def __init__(self, owner):
        self.owner = owner

    def build(self):
        CTkLabel(self.owner.main_frame, text="إعدادات الطابعة", font=("Arial", 24, "bold"), text_color=self.owner.text_color).pack(anchor="e", pady=(10, 8), padx=10)

        self.frame = CTkFrame(self.owner.main_frame, fg_color=self.owner.frame_bg, corner_radius=12)
        self.frame.pack(fill="x", pady=(10, 15))

        printers = get_system_printers()
        saved_printer = get_setting_by_key("printer_name") or ""

        # OptionMenu for available printers; fallback to allow custom text
        CTkLabel(self.frame, text=":اسم الطابعة", text_color=self.owner.text_color, font=("Arial", 14)).pack(anchor="e", padx=12, pady=(6, 0))

        self.owner.printer_option = CTkOptionMenu(self.frame, values=printers or ["(لا توجد طابعات متاحة)"], width=400, font=("Arial", 20, "bold"), dropdown_font=("Arial", 20, "bold"))
        if saved_printer:
            # if saved printer not present in list, show it with note
            if saved_printer in printers:
                self.owner.printer_option.set(saved_printer)
            else:
                self.owner.printer_option.set(saved_printer + "  (غير متصل حاليا)")
        else:
            self.owner.printer_option.set(printers[0] if printers else "(لا توجد طابعات متاحة)")
        self.owner.printer_option.pack(anchor="e", padx=12, pady=(12, 8))

        # printer type (thermal / normal)
        saved_type = get_setting_by_key("printer_type") or "thermal"
        # display Arabic choices but store english keys in code when saving
        self.owner.printer_type_option = CTkOptionMenu(self.frame, values=["حرارية", "عادية"], width=200, font=("Arial", 20, "bold"), dropdown_font=("Arial", 20, "bold"))
        self.owner.printer_type_option.set("حرارية" if saved_type == "thermal" else "عادية")
        CTkLabel(self.frame, text=":نوع الطابعة", text_color=self.owner.text_color, font=("Arial", 14)).pack(anchor="e", padx=12, pady=(6, 0))
        self.owner.printer_type_option.pack(anchor="e", padx=12, pady=(6, 8))

        # number of invoices per print
        saved_count = get_setting_by_key("invoices_per_print") or 1
        CTkLabel(self.frame, text=":عدد الفواتير لكل عملية طباعة", text_color=self.owner.text_color, font=("Arial", 14)).pack(anchor="e", padx=12, pady=(6, 0))
        self.owner.invoices_per_entry = CTkEntry(self.frame, width=120, height=36, justify="center", font=("Arial", 14))
        self.owner.invoices_per_entry.pack(anchor="e", padx=12, pady=(6, 12))
        self.owner.invoices_per_entry.delete(0, "end")
        self.owner.invoices_per_entry.insert(0, str(saved_count))