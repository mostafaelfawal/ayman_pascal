from customtkinter import CTkFrame, CTkLabel, CTkEntry, CTkButton
from tkinter.messagebox import showerror, showinfo
from ui.layout import Layout
from utils.clear_frame import clear_frame
from utils.load_image import load_image

class Auth:
    def __init__(self, root):
        self.root = root
        self.show_password_state = False
        self.main_font = ("Arial", 20, "bold")
        self.init_UI()

    # ---------------------------
    # إعداد واجهة المستخدم
    # ---------------------------
    def init_UI(self):
        self.auth_frame = CTkFrame(self.root, fg_color="transparent")
        self.auth_frame.pack(expand=True)

        # كارد النموذج
        self.card = CTkFrame(self.auth_frame, corner_radius=20, border_color="blue", border_width=2)
        self.card.pack()

        # العنوان
        title = CTkLabel(self.card, text="تسجيل الدخول", font=("Arial", 30, "bold"))
        title.pack(pady=(20, 10))

        # الصورة
        ctk_image = load_image("assets/verified.png", size=(100, 100))
        image_label = CTkLabel(self.card, image=ctk_image, text="")
        image_label.pack(pady=(0, 20))

        # نموذج تسجيل / دخول
        self.create_form()

    # ---------------------------
    # إنشاء نموذج الدخول أو التسجيل
    # ---------------------------
    def create_form(self):
        self.form_frame = CTkFrame(self.card, fg_color="transparent")
        self.form_frame.pack(pady=10, padx=10)

        # اسم المستخدم
        self.name_entry = CTkEntry(
            self.form_frame,
            placeholder_text="اسم المستخدم...",
            font=self.main_font,
            width=300,
        )
        self.name_entry.pack(pady=8, padx=5)

        # كلمة المرور + زر الإظهار
        password_frame = CTkFrame(self.form_frame, fg_color="transparent")
        password_frame.pack(pady=8)

        self.password_entry = CTkEntry(
            password_frame,
            placeholder_text="كلمة المرور...",
            show="•",
            font=self.main_font,
            width=230,
        )
        self.password_entry.pack(side="left", padx=5)

        self.password_button = CTkButton(
            password_frame,
            text="اظهار",
            font=("Arial", 16),
            width=60,
            command=self.toggle_show_password
        )
        self.password_button.pack(side="left", padx=5)

        # زر تسجيل الدخول
        self.submit_btn = CTkButton(
            self.form_frame,
            text="تسجيل الدخول",
            command=self.handle_auth,
            font=self.main_font,
            width=300,
            height=45
        )
        self.submit_btn.pack(pady=15)
    
    # ---------------------------
    # تبديل حالة اظهار و اخفاء حقل كلمة المرور 
    # ---------------------------
    def toggle_show_password(self):
        self.show_password_state = not self.show_password_state
        if self.show_password_state:
            self.password_entry.configure(show="")
            self.password_button.configure(text="اخفاء")
        else:
            self.password_entry.configure(show="•")
            self.password_button.configure(text="اظهار")

    # ---------------------------
    # التعامل مع الضغط على الزر
    # ---------------------------
    def handle_auth(self):
        password = self.password_entry.get()
        name = self.name_entry.get()

        if not password or not name:
            showerror("خطأ", "من فضلك املأ الحقول")
            return
        
        if name == 'admin' and password == "admin":
            showinfo("نجاح", "مرحبا بعودتك في ايمن للموازين.")
            clear_frame(self.root)
            Layout(self.root)
        else:
            showerror("خطأ", "المعلومات التي ادخلتها غير صحيحه.")
