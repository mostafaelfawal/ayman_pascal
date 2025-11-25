from customtkinter import CTkFrame, CTkLabel, CTkEntry, CTkButton, CTkImage
from tkinter.messagebox import showerror, showinfo
from ui.layout import Layout
from utils.clear_frame import clear_frame
from utils.load_image import load_image
from utils.settings_work import check_password, ensure_file_exists

class Auth:
    def __init__(self, root):
        self.root = root
        self.show_password_state = False
        # استخدام ألوان مناسبة للوضع الداكن
        self.primary_color = "#3b82f6"
        self.hover_color = "#2563eb"
        self.success_color = "#10b981"
        self.error_color = "#ef4444"
        self.bg_color = "#1e1e1e"  # خلفية داكنة
        self.card_bg = "#2d2d2d"   # كارد داكن
        self.text_primary = "#ffffff"  # نص رئيسي أبيض
        self.text_secondary = "#a0a0a0"  # نص ثانوي رمادي فاتح

        self.main_font = ("Arial", 16)
        self.title_font = ("Arial", 28, "bold")
        self.button_font = ("Arial", 18, "bold")
        
        self.init_UI()

    # ---------------------------
    # إعداد واجهة المستخدم
    # ---------------------------
    def init_UI(self):
        # تعيين خلفية للنافذة الرئيسية
        self.root.configure(fg_color=self.bg_color)
        
        self.auth_frame = CTkFrame(self.root, fg_color="transparent")
        self.auth_frame.pack(expand=True, fill="both", padx=20, pady=20)

        # كارد النموذج مع تأثير ظل محسن
        self.card = CTkFrame(
            self.auth_frame, 
            corner_radius=25, 
            fg_color=self.card_bg,
            border_color=self.primary_color, 
            border_width=1
        )
        self.card.pack(expand=True, pady=40)
        self.card.pack_propagate(False)
        self.card.configure(width=400, height=500)

        # العنوان مع تصميم محسن
        title_frame = CTkFrame(self.card, fg_color="transparent")
        title_frame.pack(pady=(30, 20))

        title = CTkLabel(
            title_frame, 
            text="تسجيل الدخول", 
            font=self.title_font, 
            text_color=self.primary_color
        )
        title.pack()

        subtitle = CTkLabel(
            title_frame,
            text="مرحباً بعودتك",
            font=("Arial", 14),
            text_color=self.text_secondary
        )
        subtitle.pack(pady=(5, 0))

        # الصورة مع تأثير محسن
        ctk_image = load_image("assets/verified.png", size=(120, 120))
        image_label = CTkLabel(self.card, image=ctk_image, text="")
        image_label.pack(pady=(0, 30))

        # نموذج تسجيل الدخول
        self.create_form()

    # ---------------------------
    # إنشاء نموذج الدخول
    # ---------------------------
    def create_form(self):
        self.form_frame = CTkFrame(self.card, fg_color="transparent")
        self.form_frame.pack(pady=20, padx=30, fill="both", expand=True)

        # تسمية حقل كلمة المرور
        password_label = CTkLabel(
            self.form_frame,
            text="كلمة المرور",
            font=("Arial", 14, "bold"),
            text_color=self.text_primary,
            anchor="w"
        )
        password_label.pack(pady=(0, 8), fill="x")

        # إطار حقل كلمة المرور وزر الإظهار
        password_frame = CTkFrame(self.form_frame, fg_color="transparent")
        password_frame.pack(pady=8, fill="x")

        self.password_entry = CTkEntry(
            password_frame,
            placeholder_text="أدخل كلمة المرور...",
            show="•",
            font=self.main_font,
            height=50,
            border_color=self.primary_color,
            border_width=2,
            corner_radius=12,
            fg_color="#3d3d3d",  # خلفية داكنة للحقل
            text_color=self.text_primary,  # نص أبيض
            placeholder_text_color=self.text_secondary  # نص رمادي للنص التوضيحي
        )
        self.password_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.password_entry.bind("<Return>", lambda e: self.handle_auth())

        self.password_button = CTkButton(
            password_frame,
            text="إظهار",
            font=("Arial", 14),
            width=80,
            height=50,
            command=self.toggle_show_password,
            fg_color=self.text_secondary,
            hover_color=self.text_primary,
            text_color=self.bg_color,  # نص داكن على خلفية فاتحة
            corner_radius=12
        )
        self.password_button.pack(side="right")

        # زر تسجيل الدخول مع تأثيرات محسنة
        self.submit_btn = CTkButton(
            self.form_frame,
            text="تسجيل الدخول",
            command=self.handle_auth,
            font=self.button_font,
            height=55,
            fg_color=self.primary_color,
            hover_color=self.hover_color,
            text_color="#ffffff",
            corner_radius=15,
            border_width=0
        )
        self.submit_btn.pack(pady=(25, 15), fill="x")

    # ---------------------------
    # تبديل حالة إظهار وإخفاء كلمة المرور
    # ---------------------------
    def toggle_show_password(self):
        self.show_password_state = not self.show_password_state
        if self.show_password_state:
            self.password_entry.configure(show="")
            self.password_button.configure(text="إخفاء", fg_color=self.primary_color)
        else:
            self.password_entry.configure(show="•")
            self.password_button.configure(text="إظهار", fg_color=self.text_secondary)

    # ---------------------------
    # التعامل مع عملية المصادقة
    # ---------------------------
    def handle_auth(self):
        password = self.password_entry.get().strip()
        
        if not password:
            self.show_error("خطأ", "يرجى إدخال كلمة المرور")
            return
        
        # تعطيل الزر أثناء المعالجة
        self.submit_btn.configure(state="disabled", text="جاري التحقق...")
        self.root.update()
        
        ensure_file_exists()
        
        if check_password(password):
            self.show_success("نجاح", "مرحباً بعودتك في نظام أيمن للموازين")
            self.open_main_layout()
        else:
            self.show_error("خطأ", "كلمة المرور غير صحيحة")
            # إعادة تفعيل الزر
            self.submit_btn.configure(state="normal", text="تسجيل الدخول")

    def show_error(self, title, message):
        """عرض رسالة خطأ مع تأثيرات بصرية"""
        self.password_entry.configure(border_color=self.error_color)
        showerror(title, message)
        self.submit_btn.configure(state="normal", text="تسجيل الدخول")

    def show_success(self, title, message):
        """عرض رسالة نجاح مع تأثيرات بصرية"""
        self.password_entry.configure(border_color=self.success_color)
        showinfo(title, message)

    def open_main_layout(self):
        """فتح الواجهة الرئيسية"""
        clear_frame(self.root)
        Layout(self.root)