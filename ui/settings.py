from customtkinter import BooleanVar, CTkFrame, CTkScrollableFrame, CTkSwitch, CTkEntry, CTkLabel, CTkButton
from tkinter.messagebox import showerror, showinfo
from utils.settings_work import (
    check_password, save_password,
    update_settings_by_key, get_setting_by_key
)
from utils.load_image import load_image

class Settings:
    def __init__(self, root):
        self.root = root
        self.is_security = BooleanVar(value=get_setting_by_key("is_security"))

        # الألوان الأساسية
        self.primary_color = "#3b82f6"
        self.hover_color = "#2563eb"
        self.text_color = "#f8fafc"
        self.bg_color = "#1e293b"
        self.frame_bg = "#334155"
        
        self._setup_main_frame()
        self._setup_security_section()
        self._setup_password_section()
        self._setup_company_section()
        self._setup_save_button()
        
        self.toggle_security()  # التحديث الأولي للحالة
    
    def _setup_main_frame(self):
        """إعداد الإطار الرئيسي"""
        self.main_frame = CTkScrollableFrame(self.root, fg_color=self.bg_color)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
    
    def _setup_security_section(self):
        """إعداد قسم الحماية"""
        # عنوان القسم
        self.section_title = CTkLabel(
            self.main_frame, 
            text="إعدادات الأمان",
            font=("Arial", 24, "bold"),
            text_color=self.text_color
        )
        self.section_title.pack(anchor="e", pady=(0, 20), padx=10)
        
        # إطار الحماية
        self.security_frame = CTkFrame(
            self.main_frame, 
            fg_color=self.frame_bg,
            corner_radius=12
        )
        self.security_frame.pack(fill="x", pady=(0, 15))
        
        # السويتش مع تصميم محسن
        self.sec_switch = CTkSwitch(
            self.security_frame, 
            text="تفعيل الحماية",
            variable=self.is_security, 
            command=self.toggle_security,
            font=("Arial", 18, "bold"),
            fg_color=self.primary_color,
            progress_color=self.primary_color,
            button_color="#f8fafc",
            button_hover_color="#e2e8f0",
        )
        self.sec_switch.pack(anchor="e", padx=15, pady=15)
    
    def _setup_password_section(self):
        """إعداد قسم كلمة المرور"""
        self.pass_frame = CTkFrame(
            self.security_frame, 
            fg_color="transparent",
        )
        
        self._build_password_ui()

    def _setup_company_section(self):
        """إعداد قسم بيانات الشركة (اسم - هاتف - ايميل)"""
        # عنوان القسم
        self.company_title = CTkLabel(
            self.main_frame,
            text="شركتك",
            font=("Arial", 24, "bold"),
            text_color=self.text_color
        )
        self.company_title.pack(anchor="e", pady=(10, 10), padx=10)

        # إطار خاص بالشركة
        self.company_frame = CTkFrame(
            self.main_frame,
            fg_color=self.frame_bg,
            corner_radius=12
        )
        self.company_frame.pack(fill="x", pady=(0, 15))

        # اسم الشركة
        company_name = get_setting_by_key("company_name") or ""
        self._create_text_field(
            ": اسم الشركة",
            "company_name_entry",
            initial_text=company_name
        )

        # هاتف الشركة
        company_phone = get_setting_by_key("company_phone") or ""
        self._create_text_field(
            ": رقم الهاتف",
            "company_phone_entry",
            initial_text=company_phone
        )

        # ايميل الشركة
        company_email = get_setting_by_key("company_email") or ""
        self._create_text_field(
            ": البريد الإلكتروني",
            "company_email_entry",
            initial_text=company_email
        )
    
    def _build_password_ui(self):
        """بناء واجهة كلمة المرور"""
        # إطار العنوان
        title_frame = CTkFrame(self.pass_frame, fg_color="transparent")
        title_frame.pack(fill="x", pady=(0, 15), padx=10)
        
        CTkLabel(
            title_frame, 
            text="تغيير كلمة المرور",
            font=("Arial", 18, "bold"),
            text_color=self.text_color
        ).pack(anchor="e")
        
        # كلمة المرور القديمة
        self._create_password_field(
            ": كلمة المرور القديمة", 
            "old_pass_entry",
            self.check_old_password
        )
        
        # كلمة المرور الجديدة
        self._create_password_field(
            ": كلمة المرور الجديدة", 
            "new_pass_entry"
        )
        
        # أزرار التحكم
        self._create_action_buttons()
    
    def _create_password_field(self, label_text, entry_name, command=None):
        """إنشاء حقل إدخال لكلمة المرور"""
        # الإطار الخاص بالحقل
        field_frame = CTkFrame(self.pass_frame, fg_color="transparent")
        field_frame.pack(fill="x", pady=8, padx=10)
        
        # التسمية
        CTkLabel(
            field_frame, 
            text=label_text,
            font=("Arial", 16),
            text_color=self.text_color
        ).pack(anchor="e", pady=(0, 5))
        
        # إطار الإدخال والزر
        input_frame = CTkFrame(field_frame, fg_color="transparent")
        input_frame.pack(fill="x")
        
        # حقل الإدخال
        entry = CTkEntry(
            input_frame, 
            width=300,
            height=40,
            justify="right",
            show="•",
            font=("Arial", 16),
            fg_color="#475569",
            border_color=self.primary_color,
            text_color=self.text_color,
            placeholder_text_color="#94a3b8"
        )
        entry.pack(side="right", fill="x", expand=True)
        
        setattr(self, entry_name, entry)
        
        # زر التحقق (للكلمة القديمة فقط)
        if command:
            CTkButton(
                input_frame,
                text="تحقق",
                command=command,
                font=("Arial", 14, "bold"),
                fg_color=self.primary_color,
                hover_color=self.hover_color,
                height=40,
                width=80
            ).pack(side="right", padx=10)

    def _create_text_field(self, label_text, entry_name, initial_text=""):
        """إنشاء حقل نصي (غير مشفر) بنفس تصميم حقول كلمة المرور"""
        field_frame = CTkFrame(self.company_frame if hasattr(self, 'company_frame') else self.pass_frame, fg_color="transparent")
        field_frame.pack(fill="x", pady=8, padx=10)

        CTkLabel(
            field_frame,
            text=label_text,
            font=("Arial", 16),
            text_color=self.text_color
        ).pack(anchor="e", pady=(0, 5))

        input_frame = CTkFrame(field_frame, fg_color="transparent")
        input_frame.pack(fill="x")

        entry = CTkEntry(
            input_frame,
            width=300,
            height=40,
            justify="right",
            font=("Arial", 16),
            fg_color="#475569",
            border_color=self.primary_color,
            text_color=self.text_color,
            placeholder_text_color="#94a3b8"
        )
        entry.pack(side="right", fill="x", expand=True)
        if initial_text:
            entry.insert(0, initial_text)

        setattr(self, entry_name, entry)
    
    def _create_action_buttons(self):
        """إنشاء أزرار الإجراءات"""
        buttons_frame = CTkFrame(self.pass_frame, fg_color="transparent")
        buttons_frame.pack(anchor="e", pady=15)
        
        # زر التغيير
        self.change_btn = CTkButton(
            buttons_frame,
            text="تغيير كلمة المرور",
            command=self.change_password,
            font=("Arial", 16, "bold"),
            fg_color=self.primary_color,
            hover_color=self.hover_color,
            height=45,
            width=150
        )
        self.change_btn.pack(side="right", padx=10)
        
        # زر الإلغاء
        self.cancel_btn = CTkButton(
            buttons_frame,
            text="إلغاء",
            command=self.cancel_process,
            font=("Arial", 16),
            fg_color="#64748b",
            hover_color="#475569",
            height=45,
            width=100
        )
        self.cancel_btn.pack(side="right")
    
    def _setup_save_button(self):
        """إعداد زر الحفظ"""
        save_settings_img = load_image("assets/حفظ الأعدادات.png")
        
        self.save_btn = CTkButton(
            self.main_frame,
            text="حفظ الإعدادات",
            image=save_settings_img,
            command=self.save_settings,
            font=("Arial", 18, "bold"),
            fg_color=self.primary_color,
            hover_color=self.hover_color,
            height=50,
            corner_radius=10
        )
        self.save_btn.pack(side="bottom", pady=(20, 0))
    
    def toggle_security(self):
        """تشغيل/إيقاف الحماية"""
        if self.is_security.get():
            self.pass_frame.pack(fill="x", pady=(10, 0))
            self.disable_new_password_ui()
        else:
            self.pass_frame.pack_forget()
    
    def disable_new_password_ui(self):
        """تعطيل واجهة كلمة المرور الجديدة"""
        self.new_pass_entry.configure(state="disabled")
        self.change_btn.configure(state="disabled")
        self.cancel_btn.configure(state="disabled")
        
        # تغيير الألوان للإشارة إلى التعطيل
        self.new_pass_entry.configure(fg_color="#374151", border_color="#4b5563")
        self.cancel_btn.configure(fg_color="#6b7280", hover_color="#6b7280")
    
    def enable_new_password_ui(self):
        """تمكين واجهة كلمة المرور الجديدة"""
        self.new_pass_entry.configure(state="normal")
        self.change_btn.configure(state="normal")
        self.cancel_btn.configure(state="normal")
        
        # استعادة الألوان الأصلية
        self.new_pass_entry.configure(fg_color="#475569", border_color=self.primary_color)
        self.change_btn.configure(fg_color=self.primary_color, hover_color=self.hover_color)
        self.cancel_btn.configure(fg_color="#64748b", hover_color="#475569")
    
    def check_old_password(self):
        """التحقق من كلمة المرور القديمة"""
        old_password = self.old_pass_entry.get().strip()
        
        if not old_password:
            showerror("خطأ", "يرجى إدخال كلمة المرور القديمة")
            return
        
        if not check_password(old_password):
            showerror("خطأ", "كلمة المرور القديمة غير صحيحة!")
            return
        
        showinfo("نجاح", "تم التحقق بنجاح! يمكنك الآن إدخال كلمة المرور الجديدة.")
        self.enable_new_password_ui()
    
    def change_password(self):
        """تغيير كلمة المرور"""
        new_password = self.new_pass_entry.get().strip()
        
        if len(new_password) < 4:
            showerror("خطأ", "كلمة المرور يجب أن تحتوي على 4 أحرف على الأقل")
            return
        
        save_password(new_password)
        showinfo("نجاح", "تم تغيير كلمة المرور بنجاح!")
        self.cancel_process()
    
    def cancel_process(self):
        """إلغاء عملية التغيير"""
        self.old_pass_entry.delete(0, "end")
        self.new_pass_entry.delete(0, "end")
        self.disable_new_password_ui()
    
    def save_settings(self):
        """حفظ الإعدادات"""
        update_settings_by_key("is_security", self.is_security.get())
        # حفظ بيانات الشركة
        try:
            update_settings_by_key("company_name", self.company_name_entry.get().strip())
            update_settings_by_key("company_phone", self.company_phone_entry.get().strip())
            update_settings_by_key("company_email", self.company_email_entry.get().strip())
        except Exception:
            # إذا الحقول غير موجودة (حفظ قد يكون قادم من نسخة قديمة)، تجاوب بهدوء
            pass
        showinfo("نجاح", "تم حفظ الإعدادات بنجاح!")