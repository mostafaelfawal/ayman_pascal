from customtkinter import CTkFrame, CTkScrollbar, CTkLabel, CTkButton, CTkEntry
from tkinter.ttk import Treeview, Style
from tkinter.messagebox import askokcancel, showinfo, showerror
from models.scale import ScaleDB
from utils.clear_frame import clear_frame
from utils.load_image import load_image
from ui.new_weights import NewWeights


class RecordWeights:
    def __init__(self, root):
        self.root = root
        self.db = ScaleDB()
        self.selected_id = ""
        self.load_images()
        self.setup_search_frame()
        self.container = CTkFrame(self.root, fg_color="transparent")
        self.container.pack(fill="both", expand=True, padx=10, pady=10)
        self.load_data()
        self.setup_actions_frame()

    def load_images(self):
        self.search_icon = load_image("assets/search_icon.png", (20, 20))
        self.update_data = load_image("assets/update_data.png")
        self.add_icon = load_image("assets/add.png")
        self.delete_icon = load_image("assets/delete.png")
        self.edit_icon = load_image("assets/edit.png")
        
    # =====================================================
    # اضافة البحث محسنة
    # =====================================================
    def setup_search_frame(self):
        # Search frame
        self.search_frame = CTkFrame(self.root, fg_color="#2d3748", corner_radius=15)
        self.search_frame.pack(fill="x", padx=10, pady=5)

        # حاوية داخلية للبحث
        search_container = CTkFrame(self.search_frame, fg_color="transparent")
        search_container.pack(fill="x", padx=15, pady=8)

        # زر البحث مع أيقونة
        CTkButton(
            search_container,
            text="بحث",
            image=self.search_icon,
            corner_radius=20,
            font=("Arial", 14, "bold"),
            fg_color="#3b82f6",
            hover_color="#2563eb",
            command=self.search_records,
            height=35,
            width=80
        ).pack(padx=(5, 10), pady=5, side="right")

        # حقل البحث
        self.search_var = CTkEntry(
            search_container,
            corner_radius=20,
            justify="right",
            font=("Arial", 14),
            height=35,
            border_width=2,
            border_color="#3b82f6",
            placeholder_text="🔍 ابحث بالاسم أو الكود...",
            fg_color="#1e293b",
            text_color="#e2e8f0"
        )
        self.search_var.pack(fill="x", expand=True, padx=(0, 5), pady=5, side="right")
        self.search_var.bind("<Return>", lambda e: self.search_records())

    def search_records(self):
        """منطق البحث داخل السجلات"""
        query = self.search_var.get().strip()

        if not hasattr(self, "tree"):
            return

        # مسح العناصر الحالية في الشجرة
        for item in self.tree.get_children():
            self.tree.delete(item)

        # جلب كل البيانات
        rows = self.db.get_scales()

        if query == "":
            # عرض البيانات كلها
            for row in rows:
                self.tree.insert("", "end", values=(
                    row[0], row[1], row[2], row[5], row[8]
                ))
            return

        # فلترة النتائج
        filtered = []
        for row in rows:
            _id = str(row[0])
            name = row[1]

            if query.lower() in _id.lower() or query.lower() in name.lower():
                filtered.append(row)

        # تعبئة النتائج
        if len(filtered) == 0:
            self.tree.insert("", "end", values=("", "", "❌ لا يوجد نتائج مطابقة لعبارة البحث", "", ""))
            return
        
        for row in filtered:
            self.tree.insert("", "end", values=(
                row[0], row[1], row[2], row[5], row[8]
            ))

    def to_new_record(self):
        clear_frame(self.root)
        NewWeights(self.root)

    # =====================================================
    # Treeview
    # =====================================================

    def setup_tree_frame(self):
        # حاوية رئيسية للتري فيو والتمرير
        tree_container = CTkFrame(self.container, fg_color="#1e293b", corner_radius=15)
        tree_container.pack(fill="both", expand=True, padx=5, pady=5)

        # إنشاء Scrollbar عمودي
        tree_scrollbar = CTkScrollbar(
            tree_container,
            orientation="vertical",
            button_color="#3b82f6",
            button_hover_color="#2563eb",
            fg_color="#1e293b"
        )
        tree_scrollbar.pack(side="right", fill="y")

        # إنشاء Treeview
        self.tree = Treeview(
            tree_container,
            columns=("الكود", "اسم العميل", "نوع الحمولة", "الوزن الأول", "الوزن الثاني"),
            show="headings",
            yscrollcommand=tree_scrollbar.set,
            height=12
        )
        self.tree.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        tree_scrollbar.configure(command=self.tree.yview)

        # أعمدة الـ Treeview
        columns_list = [
            {"title": "الكود", "width": 80},
            {"title": "اسم العميل", "width": 180},
            {"title": "نوع الحمولة", "width": 250},
            {"title": "الوزن الأول", "width": 120},
            {"title": "الوزن الثاني", "width": 120},
        ]
        
        for col in columns_list:
            self.tree.heading(col["title"], text=col["title"])
            self.tree.column(col["title"], width=col["width"], anchor="center")
        
        # حدث النقر على العنصر 
        self.tree.bind("<ButtonRelease-1>", self.on_tree_click)
        self.tree.bind("<Double-1>", lambda e: self.edit_weight())  # تعديل بالنقر المزدوج
        
        # تطبيق الثيم الداكن المحسن
        self.apply_dark_theme()

    def apply_dark_theme(self):
        """تطبيق الثيم المظلم الإلكتروني المحسن"""
        style = Style()
        style.theme_use('clam')
        
        # تكوين النمط للرؤوس
        style.configure(
            "Dark.Treeview.Heading",
            background="#3b82f6",  # أزرق إلكتروني للرأس
            foreground="#ffffff",  # نص أبيض على الرأس
            relief="flat",
            borderwidth=0,
            font=("Arial", 12, "bold"),
            focuscolor="none"
        )
        
        # تكوين النمط للشجرة
        style.configure(
            "Dark.Treeview",
            background="#1e293b",  # خلفية داكنة للجسم
            foreground="#e2e8f0",  # نص فاتح للجسم
            fieldbackground="#1e293b",
            borderwidth=0,
            rowheight=35,
            font=("Arial", 11)
        )
        
        # تأثيرات التحديد
        style.map(
            "Dark.Treeview",
            background=[('selected', '#3b82f6')],
            foreground=[('selected', '#ffffff')]
        )
        
        style.map(
            "Dark.Treeview.Heading",
            background=[('active', '#2563eb')],
            relief=[('active', 'flat')]
        )
        
        # تطبيق النمط
        self.tree.configure(style="Dark.Treeview")
    
    def reload_treeview(self):
        """إعادة تحميل بيانات التري بدون تدمير كامل الواجهة"""
        if not hasattr(self, "tree"):
            return

        for item in self.tree.get_children():
            self.tree.delete(item)

        rows = self.db.get_scales()
        
        for row in rows:
            self.tree.insert("", "end", values=(
                row[0], row[1], row[2], row[5], row[8]
            ))

    # =====================================================
    # تحميل البيانات 
    # =====================================================
    def load_data(self):
        rows = self.db.get_scales()
        
        # تصميم رسالة عدم وجود بيانات
        if len(rows) == 0:
            empty_container = CTkFrame(self.container, fg_color="transparent")
            empty_container.pack(expand=True, fill="both", pady=50)
            
            CTkLabel(
                empty_container,
                text="📊",
                text_color="#94a3b8",
                font=("Arial", 48)
            ).pack(pady=10)
            
            CTkLabel(
                empty_container,
                text="لم تقم بتسجيل أي وزنات بعد",
                text_color="#94a3b8",
                font=("Arial", 20, "bold")
            ).pack(pady=5)
            
            CTkLabel(
                empty_container,
                text="ابدأ بإضافة أول وزنة لك لتنظيم عمليات الوزن",
                text_color="#64748b",
                font=("Arial", 14)
            ).pack(pady=5)
            
            CTkButton(
                empty_container,
                text="اضافة اول وزنة",
                image=self.add_icon,
                font=("Arial", 18, "bold"),
                corner_radius=25,
                height=50,
                border_spacing=15,
                fg_color="#00b4c8",
                hover_color="#00808f",
                command=self.to_new_record
            ).pack(pady=20)
            return

        self.setup_tree_frame()
                
        # تعبئة التري فيو
        for row in rows:
            _id = row[0]
            name = row[1]
            load = row[2]
            first_w = row[5]
            last_w = row[8]

            self.tree.insert("", "end", values=(_id, name, load, first_w, last_w))

    # =====================================================
    # إطار الأزرار 
    # =====================================================
    def setup_actions_frame(self):
        action_frame = CTkFrame(self.root, fg_color="#2d3748", corner_radius=15)
        action_frame.pack(fill="x", padx=10, pady=10)

        # حاوية للأزرار
        buttons_container = CTkFrame(action_frame, fg_color="transparent")
        buttons_container.pack(padx=15, pady=8)

        # زر الحذف
        CTkButton(
            buttons_container,
            text="حذف الوزنة",
            image=self.delete_icon,
            command=self.delete_weight,
            font=("Arial", 16, "bold"),
            fg_color="#ef4444",
            hover_color="#dc2626",
            border_color="#fecaca",
            border_width=1,
            height=40,
            width=120
        ).pack(side="right", padx=8, pady=5)

        # زر التعديل
        CTkButton(
            buttons_container,
            text="تعديل الوزنة",
            image=self.edit_icon,
            command=self.edit_weight,
            font=("Arial", 16, "bold"),
            fg_color="#3b82f6",
            hover_color="#2563eb",
            border_color="#93c5fd",
            border_width=1,
            height=40,
            width=120
        ).pack(side="right", padx=8, pady=5)

        # زر إضافة جديد
        CTkButton(
            buttons_container,
            text="وزنة جديدة",
            image=self.add_icon,
            command=self.to_new_record,
            font=("Arial", 16, "bold"),
            fg_color="#10b981",
            hover_color="#059669",
            border_color="#a7f3d0",
            border_width=1,
            height=40,
            width=120
        ).pack(side="right", padx=8, pady=5)

        # إضافة زر تحديث البيانات
        CTkButton(
            buttons_container,
            text="تحديث البيانات",
            command=self.reload_treeview,
            font=("Arial", 16, "bold"),
            fg_color="#8b5cf6",
            hover_color="#7c3aed",
            border_color="#ddd6fe",
            image=self.update_data,
            border_width=1,
            height=40,
            width=120
        ).pack(side="left", padx=8, pady=5)

    def on_tree_click(self, event):
        item = self.tree.focus()
        if not item:
            return

        values = self.tree.item(item, "values")
        if values and values[0] != "":
            self.selected_id = values[0]

    def delete_weight(self):
        if not self.selected_id:
            showerror("خطأ", "اختر الوزنة التي تريد حذفها أولاً.")
            return

        if not askokcancel("تأكيد الحذف", f"هل أنت متأكد من حذف الوزنة رقم{self.selected_id}؟"):
            return

        try:
            self.db.delete_scale(self.selected_id)
            showinfo("تم", f" تم حذف الوزنة رقم {self.selected_id} بنجاح")
            self.selected_id = ""
            self.reload_treeview()
        except Exception as e:
            showerror("خطأ", f" حدث خطأ أثناء الحذف:\n{e}")

    def edit_weight(self):
        if not self.selected_id:
            showerror("خطأ", "اختر الوزنة التي تريد تعديلها أولاً.")
            return
        showinfo("تم", "تعديل الوزن (قيد التطوير...)")