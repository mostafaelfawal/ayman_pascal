from customtkinter import CTkLabel, CTkEntry, CTkFrame, CTkButton, StringVar
from tkinter.messagebox import askokcancel, showinfo, showerror
from datetime import datetime
import serial
import time
from threading import Thread
from utils.load_image import load_image
from models.scale import ScaleDB
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import webbrowser
from bidi.algorithm import get_display
import arabic_reshaper
from reportlab.lib.colors import HexColor, black, white
from reportlab.platypus import Table, TableStyle
import os
from utils.settings_work import get_setting_by_key

class NewWeights:
    def __init__(self, root):
        self.root = root
        self._setup_config()
        self._initialize_variables()
        self._start_serial_thread()
        self.build_ui()

    def _setup_config(self):
        """إعداد التكوينات الأساسية"""
        self.main_font = ("Arial", 16, "bold")
        self.title_font = ("Arial", 20, "bold")
        self.digital_font = ("DS-Digital", 60)
        self.db = ScaleDB()
        
        self.frame_style = {
            "corner_radius": 12,
            "border_width": 2,
            "border_color": "#3b82f6",
            "fg_color": "#1e293b"
        }
        
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
        """تهيئة المتغيرات"""
        self.is_last_weight = False
        self.scale_var = StringVar(value="0.00")
        self.entries = {}
        self.weight_frames = []
        self.ser = None

    def build_ui(self):
        """بناء واجهة المستخدم"""
        self.main_container = CTkFrame(self.root, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        self._build_scale_display()
        self._build_weight_frames()
        self._build_form_fields()
        self._build_action_buttons()

    def _build_scale_display(self):
        """بناء شاشة عرض الوزن الرقمية"""
        display_frame = CTkFrame(
            self.main_container, 
            corner_radius=12, 
            fg_color="#0f172a", 
            border_width=2, 
            border_color=self.colors["primary"]
        )
        display_frame.pack(padx=15, pady=10, fill="x")

        # العنوان
        CTkLabel(
            display_frame, 
            text="الوزن الحالي", 
            font=self.title_font, 
            text_color=self.colors["text_primary"]
        ).pack(pady=5)

        # عرض الوزن
        self.weight_label = CTkEntry(
            display_frame,
            textvariable=self.scale_var,
            state="readonly",
            fg_color="transparent",
            border_width=0,
            justify="center",
            font=self.digital_font,
            text_color=self.colors["accent"]
        )
        self.weight_label.pack(fill="x", padx=10, pady=5)

        # صافي الوزن 
        self.net_weight = CTkLabel(
            display_frame,
            text=f"الصافي = 0.00 كجم",
            font=("Arial", 12, "bold"),
            text_color=self.colors["muted"]
        )
        self.net_weight.pack(pady=(0, 2))

    def _build_weight_frames(self):
        """بناء إطارات الوزنتين الأولى والثانية"""
        weights_container = CTkFrame(self.main_container, fg_color="transparent")
        weights_container.pack(fill="x", pady=(0, 10))

        weight_data = [
            ("الوزنة الأولى", "weight1"),
            ("الوزنة الثانية", "weight2")
        ]

        for i, (title, key) in enumerate(weight_data):
            self._create_weight_frame(weights_container, title, key, i)

    def _create_weight_frame(self, parent, title, key, column):
        """إنشاء إطار وزنة فردي"""
        frame = CTkFrame(parent, **self.frame_style)
        frame.grid(row=0, column=column, padx=5, sticky="nsew")
        parent.grid_columnconfigure(column, weight=1)

        # العنوان
        CTkLabel(
            frame,
            text=title,
            font=self.title_font,
            text_color=self.colors["text_primary"]
        ).pack(pady=(10, 5))

        # إطار الحقول
        fields_frame = CTkFrame(frame, fg_color="transparent")
        fields_frame.pack(fill="x", padx=10, pady=5)

        self._create_weight_fields(fields_frame, key)
        self._create_capture_button(frame, key)

        self.weight_frames.append(frame)

    def _create_weight_fields(self, parent, key):
        """إنشاء حقول الوزن والتاريخ والوقت"""
        # حقل الوزن
        self.entries[f"{key}_weight"] = CTkEntry(
            parent,
            placeholder_text="الوزن",
            font=self.main_font,
            justify="center",
            height=35,
            corner_radius=8
        )
        self.entries[f"{key}_weight"].pack(fill="x", pady=2)
        self.entries[f"{key}_weight"].bind("<KeyRelease>", self.update_net_weight)

        # إطار التاريخ والوقت
        time_date_frame = CTkFrame(parent, fg_color="transparent")
        time_date_frame.pack(fill="x", pady=2)

        # حقل التاريخ
        self.entries[f"{key}_date"] = CTkEntry(
            time_date_frame,
            placeholder_text="التاريخ",
            font=self.main_font,
            justify="center",
            height=35,
            corner_radius=8
        )
        self.entries[f"{key}_date"].pack(side="left", fill="x", expand=True, padx=(0, 2))

        # حقل الوقت
        self.entries[f"{key}_time"] = CTkEntry(
            time_date_frame,
            placeholder_text="الوقت",
            font=self.main_font,
            justify="center",
            height=35,
            corner_radius=8
        )
        self.entries[f"{key}_time"].pack(side="right", fill="x", expand=True, padx=(2, 0))

    def _create_capture_button(self, parent, key):
        """إنشاء زر التقاط الوزن"""
        weight_img = load_image("assets/التقاط الوزن.png", (20, 20))
        
        CTkButton(
            parent,
            text="التقاط الوزن",
            font=("Arial", 13, "bold"),
            fg_color=self.colors["primary"],
            hover_color=self.colors["primary_hover"],
            height=35,
            corner_radius=8,
            image=weight_img,
            command=lambda k=key: self.capture_weight(k)
        ).pack(padx=10, pady=10, fill="x")

    def capture_weight(self, key):
        """تعبئة الوزن والتاريخ والوقت للإطار المحدد"""
        now = datetime.now()
        
        self._fill_entry(f"{key}_weight", self.scale_var.get())
        self._fill_entry(f"{key}_date", now.strftime("%Y-%m-%d"))
        self._fill_entry(f"{key}_time", now.strftime("%H:%M:%S"))
        self.update_net_weight()

    def _build_form_fields(self):
        """بناء حقول بيانات العملية"""
        frame = CTkFrame(self.main_container, **self.frame_style)
        frame.pack(fill="x", pady=(0, 10))

        # عنوان القسم
        CTkLabel(
            frame,
            text="بيانات العملية",
            font=self.title_font,
            text_color=self.colors["text_primary"]
        ).pack(pady=(10, 5))

        # إطار الحقول
        form_container = CTkFrame(frame, fg_color="transparent")
        form_container.pack(fill="x", padx=15, pady=10)

        form_fields = [
            ("اسم العميل", 0),
            ("رقم السيارة", 1),
            ("نوع الحمولة", 2),
            ("المحافظة", 3),
        ]

        for label_text, row in form_fields:
            self._create_form_field(form_container, label_text, row)

    def update_net_weight(self, event=None):
        """تحديث الوزن الصافي تلقائياً عند تغيير أي وزن"""
        try:
            w1 = float(self.entries["weight1_weight"].get() or 0)
            w2 = float(self.entries["weight2_weight"].get() or 0)
            if w1 > w2:
                net = w1 - w2
            else:
                net = w2 - w1
            self.net_weight.configure(text=f"الصافي = {net:.2f} كجم")
        except ValueError:
            self.net_weight.configure(text="الصافي = 0.00 كجم")

    def _create_form_field(self, parent, text, row):
        """إنشاء حقل فردي في نموذج البيانات"""
        # حقل الإدخال
        widget = CTkEntry(
            parent,
            height=35,
            placeholder_text=f"...أدخل {text}",
            font=self.main_font,
            justify="right",
            corner_radius=8,
            border_width=1,
            border_color="#475569"
        )
        widget.grid(row=row, column=0, padx=(0, 10), pady=5, sticky="ew")

        self.entries[text] = widget

        # العنوان
        CTkLabel(
            parent,
            text=f":{text}",
            font=self.main_font,
            text_color=self.colors["text_secondary"]
        ).grid(row=row, column=1, padx=(10, 0), pady=5, sticky="w")

        # تكوين الأعمدة
        parent.grid_columnconfigure(0, weight=3)
        parent.grid_columnconfigure(1, weight=1)

    def _build_action_buttons(self):
        """بناء أزرار الإجراءات"""
        frame = CTkFrame(self.main_container, **self.frame_style)
        frame.pack(fill="x")

        buttons_frame = CTkFrame(frame, fg_color="transparent")
        buttons_frame.pack(padx=15, pady=15)

        buttons_config = [
            ("حفظ وطباعة", "assets/حفظ و طباعة.png", self.save_and_print, self.colors["purple"], self.colors["purple_hover"]),
            ("حفظ", "assets/حفظ.png", self.save_scale, self.colors["success"], self.colors["success_hover"]),
            ("طباعة", "assets/طباعة.png", self.print_scale, self.colors["warning"], self.colors["warning_hover"]),
            ("الغاء العملية", "assets/الغاء.png", self.cancel_process, self.colors["danger"], self.colors["danger_hover"])
        ]

        for text, img, command, color, hover_color in buttons_config:
            self._create_action_button(buttons_frame, text, img, command, color, hover_color)

    def _create_action_button(self, parent, text, image_path, command, color, hover_color):
        """إنشاء زر إجراء فردي"""
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

    def _fill_entry(self, field_key, value):
        """تعبئة حقل بقيمة معينة"""
        if field_key in self.entries:
            self.entries[field_key].delete(0, "end")
            self.entries[field_key].insert(0, value)

    def cancel_process(self):
        """إلغاء العملية ومسح جميع الحقول"""
        if askokcancel("الغاء العملية", "سيتم الغاء العملية ولن يمكنك التراجع.\nهل أنت متأكد؟"):
            self.clear_all()
            
    def clear_all(self):
        for entry in self.entries.values():
                entry.delete(0, "end")
        self.scale_var.set("0.00")
    # ====================================================
    # Actions Communication
    # ====================================================
    def save_scale(self, delete_feild=True):
        for entry in self.entries.values():
            if entry.get() == "":
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
            )
        showinfo("تم", "تم حفظ الوزنة بنجاح")
        if delete_feild:
            self.clear_all()
        return True
        
    def print_scale(self):
        """طباعة وإنشاء PDF للوزنة مع دعم النص العربي بشكل صحيح"""
        client_name = self.entries["اسم العميل"].get()
        vehicle_number = self.entries["رقم السيارة"].get()
        cargo_type = self.entries["نوع الحمولة"].get()
        governorate = self.entries["المحافظة"].get()
        weight1_time = self.entries["weight1_time"].get()
        weight1_date = self.entries["weight1_date"].get()
        weight1_value = self.entries["weight1_weight"].get()
        weight2_time = self.entries["weight2_time"].get()
        weight2_date = self.entries["weight2_date"].get()
        weight2_value = self.entries["weight2_weight"].get()
        net_weight_text = self.net_weight.cget("text")
        time = datetime.now().strftime("%d/%m/%Y , %H:%M:%S")
        # =========================================
        # إعداد PDF
        # =========================================
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        pdf_file = f"exports/scale_invoice_{timestamp}.pdf"
        c = canvas.Canvas(pdf_file, pagesize=A4)
        width, height = A4

        # تسجيل الخطوط العربية
        pdfmetrics.registerFont(TTFont('Amiri', 'assets/fonts/Amiri-Regular.ttf'))
        pdfmetrics.registerFont(TTFont('Amiri-Bold', 'assets/fonts/Amiri-Bold.ttf'))

        # ألوان الهوية البصرية الزرقاء
        primary_blue = HexColor("#1a4f8c")
        secondary_blue = HexColor("#4a90e2")
        light_blue = HexColor("#e8f2ff")
        accent_blue = HexColor("#2c6bb0")

        # المارجن
        margin_x = 40
        current_y = height - 50

        def draw_arabic_text(text, x, y, font_name='Amiri', font_size=14, color=black, alignment='center'):
            """دالة محسنة لرسم النصوص العربية"""
            try:
                reshaped_text = arabic_reshaper.reshape(text)
                bidi_text = get_display(reshaped_text)
                c.setFont(font_name, font_size)
                c.setFillColor(color)
                
                if alignment == 'right':
                    c.drawRightString(x, y, bidi_text)
                elif alignment == 'center':
                    text_width = c.stringWidth(bidi_text, font_name, font_size)
                    c.drawString(x - text_width/2, y, bidi_text)
                else:  # left
                    c.drawString(x, y, bidi_text)
            except Exception as e:
                print(f"Error drawing text: {e}")
                c.setFont(font_name, font_size)
                c.setFillColor(color)
                if alignment == 'center':
                    text_width = c.stringWidth(text, font_name, font_size)
                    c.drawString(x - text_width/2, y, text)
                else:
                    c.drawString(x, y, text)

        # =========================================
        # رأس الصفحة
        # =========================================
        
        # خلفية الرأس
        c.setFillColor(light_blue)
        c.rect(0, height - 120, width, 120, fill=1, stroke=0)
        
        # شريط أزرق في الأعلى
        c.setFillColor(primary_blue)
        c.rect(0, height - 40, width, 40, fill=1, stroke=0)
        
        # جلب معلومات الشركة من الإعدادات (مع قيم افتراضية احتياطية)
        try:
            company_name = get_setting_by_key("company_name") or "أيمن للموازين"
            company_phone = get_setting_by_key("company_phone") or "01008454579"
            company_email = get_setting_by_key("company_email") or "ayman_scale@gmail.com"
        except Exception:
            company_name = "أيمن للموازين"
            company_phone = "01008454579"
            company_email = "ayman_scale@gmail.com"

        # عنوان الشركة في المركز
        draw_arabic_text(company_name, width/2, height-30, 'Amiri-Bold', 24, white, 'center')
        
        # معلومات الاتصال
        current_y = height - 90
        draw_arabic_text(f"شركة {company_name} - موازين إلكترونية دقيقة", 
                width/2, current_y, 'Amiri', 12, primary_blue, 'center')
        
        current_y -= 20
        contact_line = ""
        if company_phone and company_email:
            contact_line = f"تلفون: {company_phone} - بريد إلكتروني: {company_email}"
        elif company_phone:
            contact_line = f"تلفون: {company_phone}"
        elif company_email:
            contact_line = f"بريد إلكتروني: {company_email}"
        draw_arabic_text(contact_line, width/2, current_y, 'Amiri', 10, primary_blue, 'center')
        
        # خط فاصل
        c.setStrokeColor(secondary_blue)
        c.setLineWidth(1)
        current_y -= 20
        c.line(margin_x, current_y, width-margin_x, current_y)
        
        # =========================================
        # بيانات العميل
        # =========================================
        current_y -= 20
        
        # خلفية قسم بيانات العميل
        c.setFillColor(light_blue)
        c.rect(margin_x, current_y-100, width-2*margin_x, 100, fill=1, stroke=0)
        
        # عنوان قسم بيانات العميل
        c.setFillColor(primary_blue)
        c.rect(margin_x, current_y-30, width-2*margin_x, 30, fill=1, stroke=0)
        draw_arabic_text("بيانات العميل", width/2, current_y-20, 
                        'Amiri-Bold', 16, white, 'center')
        
        # بيانات العميل في صفين
        current_y -= 45
        
        # الصف الأول
        draw_arabic_text(f"اسم العميل: {client_name}", margin_x + 20, current_y, 
                        'Amiri', 14, black, 'left')
        draw_arabic_text(f"رقم السيارة: {vehicle_number}", width/2 + 50, current_y, 
                        'Amiri', 14, black, 'left')
        
        # الصف الثاني
        current_y -= 25
        draw_arabic_text(f"نوع الحمولة: {cargo_type}", margin_x + 20, current_y, 
                        'Amiri', 14, black, 'left')
        draw_arabic_text(f"المحافظة: {governorate}", width/2 + 50, current_y, 
                        'Amiri', 14, black, 'left')
        
        # الصف الثالث 
        current_y -= 25
        draw_arabic_text(f"تاريخ الطباعه: {time}", margin_x + 20, current_y, 
                        'Amiri', 14, black, 'left')
        
        # =========================================
        # البيانات الوزنية - التصميم المحسّن
        # =========================================
        current_y -= 50  # تقليل المسافة لجعل الجدول ملاصق للعنوان
        
        # عنوان قسم البيانات الوزنية
        c.setFillColor(primary_blue)
        c.rect(margin_x, current_y-30, width-2*margin_x, 30, fill=1, stroke=0)
        draw_arabic_text("بيانات الوزن", width/2, current_y-20, 
                        'Amiri-Bold', 16, white, 'center')
        
        # جدول البيانات الوزنية - أبعاد مضبوطة
        data = [
            ["", "التاريخ", "الوقت", "الوزن (كجم)"],
            ["الوزنة الأولى", weight1_date, weight1_time, weight1_value],
            ["الوزنة الثانية", weight2_date, weight2_time, weight2_value]
        ]
        
        # تحضير البيانات للجدول
        table_data = []
        for row in data:
            table_row = []
            for cell in row:
                try:
                    reshaped = arabic_reshaper.reshape(str(cell))
                    bidi_cell = get_display(reshaped)
                    table_row.append(bidi_cell)
                except:
                    table_row.append(str(cell))
            table_data.append(table_row)
        
        # حساب أبعاد الجدول بدقة ليتناسب مع الصفحة
        table_width = width-2*margin_x
        col_widths = [
            table_width * 0.30,  # اسم الوزنة
            table_width * 0.25,  # التاريخ
            table_width * 0.20,  # الوقت
            table_width * 0.25   # الوزن
        ]
        
        # إنشاء الجدول
        table = Table(table_data, colWidths=col_widths, rowHeights=[25, 25, 25])
        
        # تنسيق الجدول المحسّن
        table.setStyle(TableStyle([
            ('FONT', (0, 0), (-1, -1), 'Amiri', 11),  # حجم خط أصغر
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('BACKGROUND', (0, 0), (-1, 0), accent_blue),
            ('TEXTCOLOR', (0, 0), (-1, 0), white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 1, primary_blue),
            ('BACKGROUND', (0, 1), (-1, -1), light_blue),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        
        # رسم الجدول مباشرة تحت العنوان
        table.wrapOn(c, table_width, height)
        table_height = 75  # ارتفاع الجدول (3 صفوف × 25)
        table.drawOn(c, margin_x, current_y - 30 - table_height)  # ملاصق للعنوان
        
        # =========================================
        # الوزن الصافي
        # =========================================
        net_weight_y = current_y - table_height - 50  # مسافة مناسبة بعد الجدول
        
        c.setFillColor(secondary_blue)
        c.rect(margin_x, net_weight_y-50, width-2*margin_x, 50, fill=1, stroke=0)
        
        draw_arabic_text(net_weight_text, width/2, net_weight_y-30, 
                        'Amiri-Bold', 18, white, 'center')
        
        # =========================================
        # تذييل الصفحة (Footer)
        # =========================================
        
        # التأكد من وجود مساحة كافية للفوتر
        footer_height = 60
        if net_weight_y - 50 < footer_height + 20:
            # إذا لم تكن هناك مساحة كافية، نضبط موقع الوزن الصافي
            net_weight_y = footer_height + 70
            c.setFillColor(secondary_blue)
            c.rect(margin_x, net_weight_y-50, width-2*margin_x, 50, fill=1, stroke=0)
            draw_arabic_text(net_weight_text, width/2, net_weight_y-30, 
                            'Amiri-Bold', 18, white, 'center')
        
        # خلفية الفوتر
        c.setFillColor(primary_blue)
        c.rect(0, 0, width, footer_height, fill=1, stroke=0)
        
        # نص الفوتر
        draw_arabic_text("Powered By Mostafa Hamdi", width/2, 40, 
                        'Amiri', 12, white, 'center')
        
        footer_year = datetime.now().year
        footer_line = f"للاستفسار: {company_phone} - جميع الحقوق محفوظة © {footer_year}"
        draw_arabic_text(footer_line, width/2, 20, 'Amiri', 10, white, 'center')
        
        # =========================================
        # حفظ وفتح الملف
        # =========================================
        c.save()
        absolute_path = os.path.abspath(pdf_file)
        webbrowser.open_new(f"file:///{absolute_path}")
        showinfo("تم", "تمت عملية الطباعه بنجاح")
    
    def save_and_print(self):
        if self.save_scale(False):
            self.print_scale()
            self.clear_all()
    # ====================================================
    # Serial Communication
    # ====================================================
    def _start_serial_thread(self):
        """بدء thread لقراءة البيانات من الميزان"""
        Thread(target=self._serial_worker, daemon=True).start()

    def _serial_worker(self):
        """العمل الأساسي لقراءة البيانات من المنفذ التسلسلي"""
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
        """التأكد من اتصال المنفذ التسلسلي"""
        if self.ser and self.ser.is_open:
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
        except Exception:
            self.ser = None
            time.sleep(3)

    def _process_scale_data(self, data_line):
        """معالجة بيانات الوزن الواردة من الميزان"""
        parts = data_line.split(",")
        if len(parts) < 3:
            return

        raw_weight = parts[2].replace("+", "").replace("kg", "").strip()

        try:
            weight_value = float(raw_weight)
            self.root.after(0, lambda: self.scale_var.set(f"{weight_value:.2f}"))
        except ValueError:
            # تجاهل القيم غير الرقمية
            pass