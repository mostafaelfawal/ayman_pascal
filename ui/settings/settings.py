from customtkinter import BooleanVar, CTkScrollableFrame
from tkinter.messagebox import showerror, showinfo
from utils.settings_work import (
    check_password, save_password,
    update_settings_by_key, get_setting_by_key
)
from ui.settings.settings_security import SecuritySection
from ui.settings.settings_password import PasswordSection
from ui.settings.settings_company import CompanySection
from ui.settings.settings_scale import ScaleSection
from ui.settings.settings_save import SaveSection

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
        # build UI using modular sections
        SecuritySection(self).build()
        PasswordSection(self).build()
        CompanySection(self).build()
        ScaleSection(self).build()
        SaveSection(self).build()
        
        self.toggle_security()  # التحديث الأولي للحالة
    
    def _setup_main_frame(self):
        """إعداد الإطار الرئيسي"""
        self.main_frame = CTkScrollableFrame(self.root, fg_color=self.bg_color)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
    
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
            update_settings_by_key("company_address", self.company_address.get().strip())
            
            # حفظ اعدادات الميزان (منفذ و Baud Rate)
            try:
                port_value = self.scale_port_option.get()
                # OptionMenu may contain an explanatory suffix like " (غير موصول حاليا)"
                if isinstance(port_value, str) and "(" in port_value:
                    port_value = port_value.split("(")[0].strip()
                update_settings_by_key("scale_port", port_value)
            except Exception:
                # ignore if widgets not present
                pass

            try:
                baud = self.scale_baud_entry.get().strip()
                update_settings_by_key("scale_baudrate", baud)
            except Exception:
                pass
        except:
            pass
        showinfo("نجاح", "تم حفظ الإعدادات بنجاح!")