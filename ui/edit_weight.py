from customtkinter import CTkToplevel, CTkLabel, CTkEntry, CTkButton, CTkFrame, CTkScrollableFrame
from models.scale import ScaleDB
from tkinter.messagebox import showinfo, showerror
class EditWeight:
    def __init__(self, id, reload_treeview):
        self.current_id = id
        self.reload_treeview = reload_treeview
        self.db = ScaleDB()
        self.scale_data = self.db.get_scale_by_id(self.current_id)
        
        self.edit_modal = CTkToplevel()
        self.edit_modal.title("تعديل الوزنة")
        self.edit_modal.geometry("600x700")
        self.edit_modal.state("zoomed")
        self.edit_modal.grab_set()
        self.edit_modal.configure(fg_color="#1e1e1e")
        
        self.setup_ui()
        self.populate_fields()

    def setup_ui(self):
        """إعداد واجهة المستخدم"""
        # Header
        header_frame = CTkFrame(self.edit_modal, fg_color="transparent")
        header_frame.pack(pady=20)
        
        CTkLabel(header_frame, 
                text=f"({self.current_id}) تعديل الوزنة رقم", 
                font=("Arial", 24, "bold"), 
                text_color="#3b82f6").pack(pady=10)
        
        # Main container
        container = CTkFrame(self.edit_modal, fg_color="#2b2b2b", corner_radius=12)
        container.pack(padx=20, pady=10, fill="both", expand=True)
        
        # Form fields
        form_frame = CTkScrollableFrame(container, fg_color="transparent")
        form_frame.pack(padx=30, pady=30, fill="both", expand=True)
        
        # تعريف الحقول
        self.fields_config = [
            {
                "section": "معلومات العميل",
                "fields": [
                    {"label": "اسم العميل:", "placeholder": "أدخل اسم العميل", "data_index": 1, "var_name": "customer_name_entry"},
                    {"label": "نوع الحمولة:", "placeholder": "أدخل نوع الحمولة", "data_index": 2, "var_name": "load_type_entry"}
                ]
            },
            {
                "section": "معلومات السيارة", 
                "fields": [
                    {"label": "رقم السيارة:", "placeholder": "أدخل رقم السيارة", "data_index": 3, "var_name": "car_number_entry"},
                    {"label": "المحافظة:", "placeholder": "أدخل اسم المحافظة", "data_index": 4, "var_name": "governorate_entry"}
                ]
            },
            {
                "section": "الوزن",
                "fields": [
                    {"label": "الوزن الأول (كجم):", "placeholder": "الوزن الأول", "data_index": 5, "var_name": "first_weight_entry"},
                    {"label": "الوزن الأخير (كجم):", "placeholder": "الوزن الأخير", "data_index": 8, "var_name": "last_weight_entry"},
                    {"label": "السعر:", "placeholder": "السعر", "data_index": 11, "var_name": "price_entry"}
                ],
                "layout": "grid"  # تخطيط خاص لقسم الأوزان
            }
        ]
        
        self.entries = {}
        self.create_form_sections(form_frame)
        self.create_buttons(container)

    def create_form_sections(self, parent):
        """إنشاء أقسام النموذج باستخدام حلقة"""
        for section_config in self.fields_config:
            section_frame = CTkFrame(parent, fg_color="transparent")
            section_frame.pack(fill="x", pady=10)
            
            # عنوان القسم
            CTkLabel(section_frame, 
                    text=section_config["section"], 
                    font=("Arial", 16, "bold"), 
                    text_color="#e2e8f0").pack(anchor="w", pady=(0, 10))
            
            # إنشاء الحقول
            if section_config.get("layout") == "grid":
                self.create_weight_fields(section_frame, section_config["fields"])
            else:
                self.create_normal_fields(section_frame, section_config["fields"])

    def create_normal_fields(self, parent, fields):
        """إنشاء الحقول العادية"""
        for field in fields:
            self.create_field(parent, field)

    def create_weight_fields(self, parent, fields):
        """إنشاء حقول الأوزان بتخطيط شبكي"""
        grid = CTkFrame(parent, fg_color="transparent")
        grid.pack(fill="x")

        # الصف الأول: الوزن الأول + الوزن الأخير
        for col, field in enumerate(fields[:2]):
            col_frame = CTkFrame(grid, fg_color="transparent")
            col_frame.grid(row=0, column=col, padx=10, pady=5, sticky="nsew")
            self.create_field(col_frame, field)

        # الصف الثاني: السعر
        price_frame = CTkFrame(grid, fg_color="transparent")
        price_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
        self.create_field(price_frame, fields[2])

        # توزيع الأعمدة
        grid.grid_columnconfigure(0, weight=1)
        grid.grid_columnconfigure(1, weight=1)
        
    def create_field(self, parent, field_config):
        """إنشاء حقل إدخال واحد"""
        # التسمية
        CTkLabel(parent, 
                text=field_config["label"], 
                font=("Arial", 14), 
                text_color="#cbd5e1").pack(anchor="w")
        
        # حقل الإدخال
        entry = CTkEntry(parent, 
                        placeholder_text=field_config["placeholder"],
                        width=400,
                        height=40,
                        font=("Arial", 14),
                        fg_color="#374151",
                        border_color="#4b5563",
                        text_color="#f1f5f9",
                        placeholder_text_color="#9ca3af")
        entry.pack(fill="x", pady=(5, 15))
        
        # حفظ المرجع للحقل
        self.entries[field_config["var_name"]] = {
            "widget": entry,
            "data_index": field_config["data_index"],
            "required": True
        }

    def create_buttons(self, parent):
        """إنشاء أزرار الحفظ والإلغاء"""
        buttons_frame = CTkFrame(parent, fg_color="transparent")
        buttons_frame.pack(fill="x", pady=30)
        
        # Save Button
        CTkButton(buttons_frame,
                 text="حفظ التعديلات",
                 width=200,
                 height=45,
                 font=("Arial", 16, "bold"),
                 fg_color="#3b82f6",
                 hover_color="#2563eb",
                 text_color="white",
                 corner_radius=8,
                 command=self.save_changes).pack(side="right", padx=10)
        
        # Cancel Button
        CTkButton(buttons_frame,
                 text="إلغاء",
                 width=120,
                 height=45,
                 font=("Arial", 16),
                 fg_color="#64748b",
                 hover_color="#475569",
                 text_color="white",
                 corner_radius=8,
                 command=self.edit_modal.destroy).pack(side="left", padx=10)

    def populate_fields(self):
        """ملء الحقول بالبيانات الحالية"""
        for _, field_info in self.entries.items():
            data_index = field_info["data_index"]
            if self.scale_data and data_index < len(self.scale_data):
                field_info["widget"].insert(0, str(self.scale_data[data_index] or ""))

    def validate_fields(self):
        """التحقق من أن جميع الحقول مملوءة"""
        empty_fields = []
        
        for field_name, field_info in self.entries.items():
            value = field_info["widget"].get().strip()
            if not value:
                # استخراج اسم الحقل من التسمية
                field_label = next(
                    (field["label"] for section in self.fields_config 
                     for field in section["fields"] 
                     if field["var_name"] == field_name),
                    field_name
                )
                empty_fields.append(field_label)
        
        return empty_fields

    def get_field_values(self):
        return {
            "customer_name": self.entries["customer_name_entry"]["widget"].get().strip(),
            "load_type": self.entries["load_type_entry"]["widget"].get().strip(),
            "car_number": self.entries["car_number_entry"]["widget"].get().strip(),
            "governorate": self.entries["governorate_entry"]["widget"].get().strip(),
            "first_weight": self.entries["first_weight_entry"]["widget"].get().strip(),
            "last_weight": self.entries["last_weight_entry"]["widget"].get().strip(),
            "price": self.entries["price_entry"]["widget"].get().strip(),
        }

    def save_changes(self):
        """حفظ التعديلات في قاعدة البيانات"""
        try:
            # التحقق من الحقول
            empty_fields = self.validate_fields()
            if empty_fields:
                showerror("خطأ", f"يجب ملء الحقول التالية:\n{', '.join(empty_fields)}")
                return

            # الحصول على القيم
            field_values = self.get_field_values()
            
            # الحفاظ على البيانات الزمنية الأصلية
            first_time = self.scale_data[6] if self.scale_data else ""
            first_date = self.scale_data[7] if self.scale_data else ""
            last_time = self.scale_data[9] if self.scale_data else ""
            last_date = self.scale_data[10] if self.scale_data else ""
            
            # حفظ التعديلات
            self.db.edit_scale(
                field_values["customer_name"], 
                field_values["load_type"], 
                field_values["car_number"], 
                field_values["governorate"], 
                first_time, first_date, field_values["first_weight"], 
                last_time, last_date, field_values["last_weight"], 
                self.current_id,
                field_values["price"]
            )

            # إظهار رسالة نجاح وإعادة التحميل
            self.edit_modal.destroy()
            showinfo("تم", "تم تعديل الوزنة بنجاح")
            self.reload_treeview()
            
        except Exception as e:
            showerror("خطأ", f"حدث خطأ أثناء الحفظ: {str(e)}")