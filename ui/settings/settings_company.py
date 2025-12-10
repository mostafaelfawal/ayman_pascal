from customtkinter import CTkLabel, CTkFrame, CTkEntry, CTkButton
from tkinter import filedialog
from PIL import Image, ImageTk
import customtkinter as ctk


class CompanySection:
    """Builds company info section (name, phone, email, logo uploader) and attaches entries to owner."""

    def __init__(self, owner):
        self.owner = owner

    def build(self):
        self.owner.company_title = CTkLabel(
            self.owner.main_frame,
            text="شركتك",
            font=("Arial", 24, "bold"),
            text_color=self.owner.text_color,
        )
        self.owner.company_title.pack(anchor="e", padx=10)
        CTkLabel(
            self.owner.main_frame,
            text="!سيتم عرض هذه البيانات في الفاتوره",
            text_color="#00b3ad",
            font=("Arial", 14)
        ).pack(anchor="e", pady=(4, 10), padx=10)

        self.owner.company_frame = CTkFrame(
            self.owner.main_frame,
            fg_color=self.owner.frame_bg,
            corner_radius=12,
        )
        self.owner.company_frame.pack(fill="x", pady=(0, 15))

        from utils.settings_work import get_setting_by_key

        company_name = get_setting_by_key("company_name") or ""
        company_phone = get_setting_by_key("company_phone") or ""
        company_email = get_setting_by_key("company_email") or ""
        company_logo = get_setting_by_key("company_logo") or ""

        self._create_text_field(": اسم الشركة", "company_name_entry", company_name)
        self._create_text_field(": رقم الهاتف", "company_phone_entry", company_phone)
        self._create_text_field(": البريد الإلكتروني", "company_email_entry", company_email)

        # ----------- Logo Picker with Preview -----------
        logo_frame = CTkFrame(self.owner.company_frame, fg_color="transparent")
        logo_frame.pack(fill="x", pady=8, padx=10)

        CTkLabel(
            logo_frame,
            text=": شعار الشركة",
            font=("Arial", 16),
            text_color=self.owner.text_color,
        ).pack(anchor="e", pady=(0, 5))

        # Create main container for logo
        logo_container = CTkFrame(logo_frame, fg_color="transparent")
        logo_container.pack(fill="x", pady=5)

        # Left side: Preview frame
        self.owner.preview_frame = CTkFrame(logo_container, fg_color="#475569", width=150, height=150, corner_radius=8)
        self.owner.preview_frame.pack(side="right", padx=(0, 10))
        self.owner.preview_frame.pack_propagate(False)

        # Preview label inside frame
        self.owner.logo_preview_label = CTkLabel(
            self.owner.preview_frame,
            text="معاينة الشعار",
            text_color="#cbd5e1",
            font=("Arial", 12)
        )
        self.owner.logo_preview_label.pack(expand=True, padx=10, pady=10)

        # Right side: Button and file name
        controls_frame = CTkFrame(logo_container, fg_color="transparent")
        controls_frame.pack(side="right", fill="both", expand=True)

        # Button frame
        btn_frame = CTkFrame(controls_frame, fg_color="transparent")
        btn_frame.pack(anchor="e", pady=(10, 5))

        def pick_logo():
            path = filedialog.askopenfilename(
                title="اختر صورة الشعار",
                filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")]
            )
            if path:
                self.owner.company_logo_path = path
                self.logo_name_label.configure(text=path.split("/")[-1])
                self._update_logo_preview(path)

        # اختيار صورة button
        CTkButton(
            btn_frame,
            text="اختر صورة",
            command=pick_logo,
            fg_color=self.owner.primary_color,
            font=("Arial", 14),
            text_color="white",
            corner_radius=8,
            height=40,
            width=120
        ).pack(side="right", padx=5)

        # عرض اسم الشعار الحالي
        self.logo_name_label = CTkLabel(
            btn_frame,
            text=company_logo.split("/")[-1] if company_logo else "لا يوجد شعار محدد",
            font=("Arial", 14),
            text_color="#cbd5e1"
        )
        self.logo_name_label.pack(side="right", padx=(10, 5))

        # Clear logo button
        CTkButton(
            btn_frame,
            text="إزالة الشعار",
            command=self._clear_logo,
            fg_color="#64748b",
            font=("Arial", 14),
            text_color="white",
            corner_radius=8,
            height=40,
            width=100
        ).pack(side="right")

        # Instructions
        CTkLabel(
            controls_frame,
            text="الحجم الموصى به: (150x150) بكسل",
            text_color="#94a3b8",
            font=("Arial", 12)
        ).pack(anchor="e", pady=(5, 0))

        # حفظ القيمة في الـ owner
        self.owner.company_logo_path = company_logo
        
        # عرض الصورة المحفوظة إن وجدت
        if company_logo:
            self._update_logo_preview(company_logo)

    def _update_logo_preview(self, image_path):
        """تحديث معاينة الشعار"""
        try:
            # Load image
            img = Image.open(image_path)
            
            # Calculate size to fit in preview frame while maintaining aspect ratio
            max_size = (140, 140)
            img.thumbnail(max_size, Image.Resampling.LANCZOS)
            
            # Convert to CTkImage
            ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=img.size)
            
            # Update label with image
            self.owner.logo_preview_label.configure(image=ctk_img, text="")
            self.owner.logo_preview_label.image = ctk_img  # Keep reference
            
        except Exception as e:
            print(f"Error loading image: {e}")
            self.owner.logo_preview_label.configure(
                text="خطأ في تحميل الصورة",
                image=None
            )

    def _clear_logo(self):
        """إزالة الشعار"""
        self.owner.company_logo_path = ""
        self.logo_name_label.configure(text="لا يوجد شعار محدد")
        self.owner.logo_preview_label.configure(
            text="معاينة الشعار",
            image=None
        )
        self.owner.logo_preview_label.image = None

    # ----------------------
    def _create_text_field(self, label_text, entry_name, initial_text=""):
        field_frame = CTkFrame(self.owner.company_frame, fg_color="transparent")
        field_frame.pack(fill="x", pady=8, padx=10)

        CTkLabel(field_frame, text=label_text, font=("Arial", 16),
                 text_color=self.owner.text_color).pack(anchor="e", pady=(0, 5))

        input_frame = CTkFrame(field_frame, fg_color="transparent")
        input_frame.pack(fill="x")

        entry = CTkEntry(
            input_frame,
            width=300,
            height=40,
            justify="right",
            font=("Arial", 16),
            fg_color="#475569",
            border_color=self.owner.primary_color,
            text_color=self.owner.text_color,
            placeholder_text_color="#94a3b8",
        )
        entry.pack(side="right", fill="x", expand=True)
        if initial_text:
            entry.insert(0, initial_text)

        setattr(self.owner, entry_name, entry)