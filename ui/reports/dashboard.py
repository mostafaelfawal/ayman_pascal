import customtkinter as ctk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from datetime import datetime
import tkinter as tk

# الألوان المخصصة بناءً على طلبك
COLORS = {
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
    "muted": "#94a3b8",
    "bg_primary": "#0f172a",
    "bg_secondary": "#1e293b",
    "bg_card": "#334155",
    "border": "#475569"
}

class ScaleDashboard():
    """الواجهة الرئيسية للتقارير الإدارية مع دعم الشاشات الضيقة"""
    
    def __init__(self, root):
        self.root = root
        
        # إنشاء قاعدة البيانات
        from models.dashboard import DashboardDB
        self.db = DashboardDB()
        
        # متغيرات الفلاتر
        self.start_date_var = ctk.StringVar()
        self.end_date_var = ctk.StringVar()
        self.customer_var = ctk.StringVar(value="الكل")
        self.load_type_var = ctk.StringVar(value="الكل")
        self.governorate_var = ctk.StringVar(value="الكل")
        
        # إنشاء الواجهة مع CTkScrollableFrame
        self.create_scrollable_interface()
        
        # تحميل البيانات الأولية
        self.update_dashboard()

    def create_scrollable_interface(self):
        """إنشاء واجهة قابلة للتمرير تناسب الشاشات الضيقة"""
        
        # إطار رئيسي
        self.main_container = ctk.CTkFrame(self.root, fg_color=COLORS["bg_primary"])
        self.main_container.pack(fill="both", expand=True, padx=5, pady=5)
        
        # إنشاء CTkScrollableFrame
        self.scrollable_frame = ctk.CTkScrollableFrame(
            self.main_container,
            fg_color=COLORS["bg_primary"],
            scrollbar_button_color=COLORS["primary"],
            scrollbar_button_hover_color=COLORS["primary_hover"]
        )
        self.scrollable_frame.pack(fill="both", expand=True)
        
        # إنشاء محتوى الواجهة داخل الإطار القابل للتمرير
        self.create_widgets()
    
    def create_widgets(self):
        """إنشاء عناصر الواجهة داخل CTkScrollableFrame"""
        
        # عنوان التطبيق
        title_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="transparent", height=60)
        title_frame.pack(fill="x", padx=15, pady=(5, 10))
        title_frame.pack_propagate(False)
        
        title_label = ctk.CTkLabel(
            title_frame,
            text="📊 ميزان بسكول – التقارير الإدارية",
            font=("Arial", 24, "bold"),
            text_color=COLORS["text_primary"]
        )
        title_label.pack(side="left")
        
        # شريط الفلاتر - تصميم عمودي للشاشات الضيقة
        self.create_filters_bar()
        
        # كروت الإحصائيات السريعة - تصميم عمودي للشاشات الضيقة
        self.create_stats_cards()
        
        # إطار التحليلات والرسوم البيانية
        analytics_frame = ctk.CTkFrame(self.scrollable_frame, fg_color=COLORS["bg_secondary"], corner_radius=10)
        analytics_frame.pack(fill="x", padx=15, pady=10)
        
        # عنوان قسم التحليلات
        analytics_title = ctk.CTkLabel(
            analytics_frame,
            text="📈 التحليلات والرسوم البيانية",
            font=("Arial", 18, "bold"),
            text_color=COLORS["text_primary"]
        )
        analytics_title.pack(anchor="w", padx=20, pady=(15, 10))
        
        # قسم التحليلات (أعلى للشاشات الضيقة)
        analytics_grid = ctk.CTkFrame(analytics_frame, fg_color="transparent")
        analytics_grid.pack(fill="x", padx=15, pady=(0, 15))
        
        # تحليلات الوزن
        self.create_weight_analytics(analytics_grid)
        
        # التحليلات الزمنية
        self.create_time_analytics(analytics_grid)
        
        # الرسوم البيانية
        self.create_charts_frame(analytics_grid)
        
        # أزرار سريعة
        self.create_quick_actions()
    
    def create_filters_bar(self):
        """إنشاء شريط الفلاتر عمودي للشاشات الضيقة"""
        filters_frame = ctk.CTkFrame(self.scrollable_frame, fg_color=COLORS["bg_secondary"], corner_radius=10)
        filters_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        # عنوان الفلاتر
        filters_label = ctk.CTkLabel(
            filters_frame,
            text="🔍 فلترة البيانات",
            font=("Arial", 16, "bold"),
            text_color=COLORS["text_primary"]
        )
        filters_label.pack(anchor="w", padx=20, pady=(15, 10))
        
        # شبكة الفلاتر (عمودية للشاشات الضيقة)
        filters_grid = ctk.CTkFrame(filters_frame, fg_color="transparent")
        filters_grid.pack(fill="x", padx=20, pady=(0, 15))
        
        # صف 1: التواريخ
        date_row = ctk.CTkFrame(filters_grid, fg_color="transparent")
        date_row.pack(fill="x", pady=5)
        
        # من تاريخ
        from_label = ctk.CTkLabel(
            date_row,
            text="من تاريخ:",
            font=("Arial", 14),
            text_color=COLORS["text_secondary"]
        )
        from_label.pack(side="left", padx=(0, 10))
        
        self.start_date_entry = ctk.CTkEntry(
            date_row,
            textvariable=self.start_date_var,
            placeholder_text="YYYY-MM-DD",
            height=35
        )
        self.start_date_entry.pack(side="left", fill="x", expand=True, padx=(0, 20))
        
        # إلى تاريخ
        to_label = ctk.CTkLabel(
            date_row,
            text="إلى تاريخ:",
            font=("Arial", 14),
            text_color=COLORS["text_secondary"]
        )
        to_label.pack(side="left", padx=(0, 10))
        
        self.end_date_entry = ctk.CTkEntry(
            date_row,
            textvariable=self.end_date_var,
            placeholder_text="YYYY-MM-DD",
            height=35
        )
        self.end_date_entry.pack(side="left", fill="x", expand=True)
        
        # صف 2: العملاء ونوع الحمولة
        row2 = ctk.CTkFrame(filters_grid, fg_color="transparent")
        row2.pack(fill="x", pady=5)
        
        # العميل
        customer_label = ctk.CTkLabel(
            row2,
            text="العميل:",
            font=("Arial", 14),
            text_color=COLORS["text_secondary"]
        )
        customer_label.pack(side="left", padx=(0, 10))
        
        customers = ["الكل"] + self.db.get_customers_list()
        self.customer_combo = ctk.CTkComboBox(
            row2,
            values=customers,
            variable=self.customer_var,
            height=35,
            dropdown_font=("Arial", 12)
        )
        self.customer_combo.pack(side="left", fill="x", expand=True, padx=(0, 20))
        
        # نوع الحمولة
        load_label = ctk.CTkLabel(
            row2,
            text="نوع الحمولة:",
            font=("Arial", 14),
            text_color=COLORS["text_secondary"]
        )
        load_label.pack(side="left", padx=(0, 10))
        
        load_types = ["الكل"] + self.db.get_load_types()
        self.load_type_combo = ctk.CTkComboBox(
            row2,
            values=load_types,
            variable=self.load_type_var,
            height=35,
            dropdown_font=("Arial", 12)
        )
        self.load_type_combo.pack(side="left", fill="x", expand=True)
        
        # صف 3: المحافظة وأزرار
        row3 = ctk.CTkFrame(filters_grid, fg_color="transparent")
        row3.pack(fill="x", pady=5)
        
        # المحافظة
        gov_label = ctk.CTkLabel(
            row3,
            text="المحافظة:",
            font=("Arial", 14),
            text_color=COLORS["text_secondary"]
        )
        gov_label.pack(side="left", padx=(0, 10))
        
        governorates = ["الكل"] + self.db.get_governorates()
        self.governorate_combo = ctk.CTkComboBox(
            row3,
            values=governorates,
            variable=self.governorate_var,
            height=35,
            dropdown_font=("Arial", 12)
        )
        self.governorate_combo.pack(side="left", fill="x", expand=True, padx=(0, 20))
        
        # زر تحديث التقارير
        update_btn = ctk.CTkButton(
            row3,
            text="🔄 تحديث التقارير",
            command=self.update_dashboard,
            fg_color=COLORS["primary"],
            hover_color=COLORS["primary_hover"],
            height=40,
            font=("Arial", 14, "bold")
        )
        update_btn.pack(side="left", fill="x", expand=True)
    
    def create_stats_cards(self):
        """إنشاء كروت الإحصائيات السريعة عمودية للشاشات الضيقة"""
        cards_container = ctk.CTkFrame(self.scrollable_frame, fg_color="transparent")
        cards_container.pack(fill="x", padx=15, pady=(0, 15))
        
        # عنوان الكروت
        cards_title = ctk.CTkLabel(
            cards_container,
            text="📊 الإحصائيات السريعة",
            font=("Arial", 18, "bold"),
            text_color=COLORS["text_primary"]
        )
        cards_title.pack(anchor="w", pady=(0, 10))
        
        # شبكة الكروت (5 كروت في صفين)
        cards_grid = ctk.CTkFrame(cards_container, fg_color="transparent")
        cards_grid.pack(fill="x")
        
        # بيانات الكروت
        cards_data = [
            {
                "title": "إجمالي عمليات الوزن",
                "value": "0",
                "icon": "📊",
                "color": COLORS["primary"]
            },
            {
                "title": "وزنات اليوم",
                "value": "0",
                "icon": "📅",
                "color": COLORS["success"]
            },
            {
                "title": "وزنات الشهر الحالي",
                "value": "0",
                "icon": "📈",
                "color": COLORS["warning"]
            },
            {
                "title": "عملاء مختلفون",
                "value": "0",
                "icon": "👥",
                "color": COLORS["purple"]
            },
            {
                "title": "سيارات مختلفة",
                "value": "0",
                "icon": "🚛",
                "color": COLORS["accent"]
            }
        ]
        
        self.stats_cards = []
        
        for i, card_data in enumerate(cards_data):
            # تحديد الصف والعمود
            row = i // 3  # 3 كروت في كل صف
            col = i % 3
            
            # إنشاء الكارت
            card = ctk.CTkFrame(
                cards_grid,
                fg_color=COLORS["bg_card"],
                border_width=1,
                border_color=COLORS["border"],
                corner_radius=10
            )
            card.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
            
            # جعل الخلايا تتمدد بشكل متساوٍ
            cards_grid.grid_columnconfigure(col, weight=1)
            
            # المحتوى الداخلي للكارت
            inner_frame = ctk.CTkFrame(card, fg_color="transparent")
            inner_frame.pack(fill="both", expand=True, padx=10, pady=10)
            
            # صف الأيقونة والعنوان
            top_row = ctk.CTkFrame(inner_frame, fg_color="transparent")
            top_row.pack(fill="x")
            
            # الأيقونة
            icon_label = ctk.CTkLabel(
                top_row,
                text=card_data["icon"],
                font=("Arial", 24),
                text_color=card_data["color"]
            )
            icon_label.pack(side="left", padx=(0, 10))
            
            # العنوان
            title_label = ctk.CTkLabel(
                top_row,
                text=card_data["title"],
                font=("Arial", 12),
                text_color=COLORS["text_secondary"]
            )
            title_label.pack(side="left")
            
            # القيمة
            value_label = ctk.CTkLabel(
                inner_frame,
                text="0",
                font=("Arial", 22, "bold"),
                text_color=COLORS["text_primary"]
            )
            value_label.pack(anchor="w", pady=(5, 0))
            
            self.stats_cards.append({
                "frame": card,
                "value_label": value_label,
                "title": card_data["title"],
                "icon": card_data["icon"],
                "color": card_data["color"]
            })
    
    def create_weight_analytics(self, parent):
        """إنشاء قسم تحليلات الوزن"""
        weight_frame = ctk.CTkFrame(
            parent,
            fg_color=COLORS["bg_card"],
            border_width=1,
            border_color=COLORS["border"],
            corner_radius=10
        )
        weight_frame.pack(fill="x", pady=(0, 10))
        
        # عنوان القسم
        weight_title = ctk.CTkLabel(
            weight_frame,
            text="⚖️ تحليلات الوزن الصافي",
            font=("Arial", 16, "bold"),
            text_color=COLORS["text_primary"]
        )
        weight_title.pack(anchor="w", padx=15, pady=12)
        
        # شبكة لعرض البيانات (صفين)
        grid_frame = ctk.CTkFrame(weight_frame, fg_color="transparent")
        grid_frame.pack(fill="x", padx=15, pady=(0, 12))
        
        self.weight_stats_labels = {}
        stats_data = [
            ("إجمالي الوزن الصافي", "kg 0", COLORS["primary"]),
            ("متوسط الوزن الصافي", "kg 0", COLORS["success"]),
            ("أعلى وزن صافي", "kg 0", COLORS["warning"]),
            ("أقل وزن صافي", "kg 0", COLORS["accent"])
        ]
        
        for i, (title, default_value, color) in enumerate(stats_data):
            row = i // 2
            col = i % 2
            
            stat_frame = ctk.CTkFrame(grid_frame, fg_color="transparent")
            stat_frame.grid(row=row, column=col, padx=10, pady=5, sticky="ew")
            grid_frame.grid_columnconfigure(col, weight=1)
            
            title_label = ctk.CTkLabel(
                stat_frame,
                text=title,
                font=("Arial", 13),
                text_color=COLORS["text_secondary"]
            )
            title_label.pack(anchor="w")
            
            value_label = ctk.CTkLabel(
                stat_frame,
                text=default_value,
                font=("Arial", 20, "bold"),
                text_color=color
            )
            value_label.pack(anchor="w", pady=(2, 0))
            
            self.weight_stats_labels[title] = value_label
    
    def create_time_analytics(self, parent):
        """إنشاء قسم التحليلات الزمنية"""
        time_frame = ctk.CTkFrame(
            parent,
            fg_color=COLORS["bg_card"],
            border_width=1,
            border_color=COLORS["border"],
            corner_radius=10
        )
        time_frame.pack(fill="x", pady=(0, 10))
        
        # عنوان القسم
        time_title = ctk.CTkLabel(
            time_frame,
            text="⏱️ التحليلات الزمنية",
            font=("Arial", 16, "bold"),
            text_color=COLORS["text_primary"]
        )
        time_title.pack(anchor="w", padx=15, pady=12)
        
        # شبكة لعرض البيانات (صفين)
        grid_frame = ctk.CTkFrame(time_frame, fg_color="transparent")
        grid_frame.pack(fill="x", padx=15, pady=(0, 12))
        
        self.time_stats_labels = {}
        stats_data = [
            ("متوسط زمن العملية", "0 دقيقة", COLORS["primary"]),
            ("أطول عملية وزن", "0 دقيقة", COLORS["warning"]),
            ("أسرع عملية وزن", "0 دقيقة", COLORS["success"]),
            ("إجمالي الزمن", "0 ساعة", COLORS["accent"])
        ]
        
        for i, (title, default_value, color) in enumerate(stats_data):
            row = i // 2
            col = i % 2
            
            stat_frame = ctk.CTkFrame(grid_frame, fg_color="transparent")
            stat_frame.grid(row=row, column=col, padx=10, pady=5, sticky="ew")
            grid_frame.grid_columnconfigure(col, weight=1)
            
            title_label = ctk.CTkLabel(
                stat_frame,
                text=title,
                font=("Arial", 13),
                text_color=COLORS["text_secondary"]
            )
            title_label.pack(anchor="w")
            
            value_label = ctk.CTkLabel(
                stat_frame,
                text=default_value,
                font=("Arial", 20, "bold"),
                text_color=color
            )
            value_label.pack(anchor="w", pady=(2, 0))
            
            self.time_stats_labels[title] = value_label
    
    def create_charts_frame(self, parent):
        """إنشاء إطار الرسوم البيانية عمودي للشاشات الضيقة"""
        charts_frame = ctk.CTkFrame(
            parent,
            fg_color=COLORS["bg_card"],
            border_width=1,
            border_color=COLORS["border"],
            corner_radius=10
        )
        charts_frame.pack(fill="x", pady=(0, 10))
        
        # عنوان الرسوم البيانية
        charts_title = ctk.CTkLabel(
            charts_frame,
            text="📊 الرسوم البيانية",
            font=("Arial", 16, "bold"),
            text_color=COLORS["text_primary"]
        )
        charts_title.pack(anchor="w", padx=15, pady=12)
        
        # إطار للرسوم البيانية (عمودي للشاشات الضيقة)
        self.charts_container = ctk.CTkFrame(charts_frame, fg_color="transparent")
        self.charts_container.pack(fill="x", padx=15, pady=(0, 12))
    
    def create_table(self, parent):
        """إنشاء جدول البيانات مع تصميم للشاشات الضيقة"""
        # إطار للجدول
        table_container = ctk.CTkFrame(parent, fg_color="transparent")
        table_container.pack(fill="x", padx=20, pady=(0, 15))
        
        # إنشاء Treeview مع تحديد ارتفاع مناسب
        columns = ("ID", "العميل", "نوع الحمولة", "رقم العربية", "الوزن الصافي", "التاريخ")
        self.tree = ttk.Treeview(
            table_container,
            columns=columns,
            show="headings",
            height=6  # ارتفاع أقل للشاشات الضيقة
        )
        
        # تحديد الأنماط
        style = ttk.Style()
        style.theme_use("clam")
        
        # تكوين الأنماط للوضع الداكن
        style.configure(
            "Treeview",
            background=COLORS["bg_card"],
            foreground=COLORS["text_primary"],
            fieldbackground=COLORS["bg_card"],
            borderwidth=0,
            font=("Arial", 10)  # خط أصغر للشاشات الضيقة
        )
        
        style.configure(
            "Treeview.Heading",
            background=COLORS["bg_secondary"],
            foreground=COLORS["accent"],
            font=("Arial", 11, "bold"),
            borderwidth=0,
            relief="flat"
        )
        
        style.map(
            "Treeview",
            background=[("selected", COLORS["primary"])],
            foreground=[("selected", "white")]
        )
        
        # تعريف العناوين بعناوين مختصرة
        self.tree.heading("ID", text="رقم")
        self.tree.heading("العميل", text="العميل")
        self.tree.heading("نوع الحمولة", text="النوع")
        self.tree.heading("رقم العربية", text="السيارة")
        self.tree.heading("الوزن الصافي", text="الوزن")
        self.tree.heading("التاريخ", text="التاريخ")
        
        # تحديد عرض أعمدة أصغر للشاشات الضيقة
        self.tree.column("ID", width=60, anchor="center", minwidth=60)
        self.tree.column("العميل", width=150, anchor="center", minwidth=120)
        self.tree.column("نوع الحمولة", width=100, anchor="center", minwidth=80)
        self.tree.column("رقم العربية", width=100, anchor="center", minwidth=80)
        self.tree.column("الوزن الصافي", width=80, anchor="center", minwidth=70)
        self.tree.column("التاريخ", width=80, anchor="center", minwidth=70)
        
        # إضافة Scrollbar أفقية وعمودية
        v_scrollbar = ttk.Scrollbar(table_container, orient="vertical", command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(table_container, orient="horizontal", command=self.tree.xview)
        
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # وضع العناصر في grid
        self.tree.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        # تكوين grid للتمدد
        table_container.grid_rowconfigure(0, weight=1)
        table_container.grid_columnconfigure(0, weight=1)
    
    def create_quick_actions(self):
        """إنشاء أزرار الإجراءات السريعة"""
        actions_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="transparent")
        actions_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        # شبكة للأزرار
        buttons_grid = ctk.CTkFrame(actions_frame, fg_color="transparent")
        buttons_grid.pack(fill="x")
        
        # زر تصفية الفلاتر
        clear_btn = ctk.CTkButton(
            buttons_grid,
            text="🗑️ مسح الفلاتر",
            command=self.clear_filters,
            fg_color=COLORS["danger"],
            hover_color=COLORS["danger_hover"],
            height=40,
            font=("Arial", 14, "bold")
        )
        clear_btn.pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        # زر التحديث
        refresh_btn = ctk.CTkButton(
            buttons_grid,
            text="🔄 تحديث البيانات",
            command=self.update_dashboard,
            fg_color=COLORS["success"],
            hover_color=COLORS["success_hover"],
            height=40,
            font=("Arial", 14, "bold")
        )
        refresh_btn.pack(side="left", fill="x", expand=True, padx=5)
        
        # زر طباعة تقرير اليوم
        print_btn = ctk.CTkButton(
            buttons_grid,
            text="🖨️ طباعة تقرير اليوم",
            command=self.print_today_report,
            fg_color=COLORS["primary"],
            hover_color=COLORS["primary_hover"],
            height=40,
            font=("Arial", 14, "bold")
        )
        print_btn.pack(side="left", fill="x", expand=True, padx=(5, 0))
    
    def update_charts(self):
        """تحديث الرسوم البيانية مع تصميم للشاشات الضيقة"""
        # تنظيف الإطار الحالي
        for widget in self.charts_container.winfo_children():
            widget.destroy()
        
        # الحصول على البيانات
        daily_stats = self.db.get_daily_stats(
            self.start_date_var.get() if self.start_date_var.get() else None,
            self.end_date_var.get() if self.end_date_var.get() else None
        )
        
        customer_stats = self.db.get_customer_stats(
            self.start_date_var.get() if self.start_date_var.get() else None,
            self.end_date_var.get() if self.end_date_var.get() else None
        )
        
        # إنشاء الرسم البياني 1: عدد الوزنات اليومية
        fig1 = Figure(figsize=(6, 2.5), dpi=80, facecolor=COLORS["bg_card"])  # حجم أصغر
        ax1 = fig1.add_subplot(111)
        
        if daily_stats:
            dates = [row["last_date"] for row in daily_stats]
            counts = [row["count"] for row in daily_stats]
            
            # تقصير تواريخ العرض أكثر للشاشات الضيقة
            short_dates = []
            for date in dates:
                parts = date.split("-")
                if len(parts) >= 3:
                    short_dates.append(f"{parts[2]}/{parts[1]}")
                else:
                    short_dates.append(date[-5:])
            
            # تحديد عدد الأعمدة للعرض
            max_bars = 8  # عدد أقل للأعمدة للشاشات الضيقة
            if len(short_dates) > max_bars:
                short_dates = short_dates[-max_bars:]
                counts = counts[-max_bars:]
            
            bars1 = ax1.bar(short_dates, counts, color=COLORS["primary"], edgecolor=COLORS["border"], width=0.6)
            ax1.set_facecolor(COLORS["bg_card"])
            ax1.tick_params(colors=COLORS["text_secondary"], labelsize=9)
            ax1.set_title("عدد عمليات الوزن يومياً", color=COLORS["text_primary"], fontsize=11, pad=8)
            ax1.set_xlabel("التاريخ", color=COLORS["text_secondary"], fontsize=9)
            ax1.set_ylabel("العدد", color=COLORS["text_secondary"], fontsize=9)
            
            # إضافة القيم فوق الأعمدة
            for bar in bars1:
                height = bar.get_height()
                ax1.text(bar.get_x() + bar.get_width()/2., height + 0.05,
                        f'{int(height)}', ha='center', va='bottom',
                        color=COLORS["text_primary"], fontsize=8)
        
        else:
            ax1.text(0.5, 0.5, "لا توجد بيانات", 
                    ha='center', va='center',
                    color=COLORS["text_secondary"], fontsize=12)
            ax1.set_facecolor(COLORS["bg_card"])
        
        fig1.tight_layout(pad=2)
        
        # إنشاء الرسم البياني 2: أكثر العملاء تعاملاً
        fig2 = Figure(figsize=(6, 2.5), dpi=80, facecolor=COLORS["bg_card"])
        ax2 = fig2.add_subplot(111)
        
        if customer_stats:
            customers = [row["customer_name"] for row in customer_stats]
            counts = [row["count"] for row in customer_stats]
            
            # تقصير أسماء العملاء أكثر للشاشات الضيقة
            short_customers = []
            for name in customers:
                if len(name) > 8:
                    short_customers.append(name[:6] + "..")
                else:
                    short_customers.append(name)
            
            # تحديد عدد الأعمدة للعرض
            max_bars = 6
            if len(short_customers) > max_bars:
                short_customers = short_customers[:max_bars]
                counts = counts[:max_bars]
            
            bars2 = ax2.barh(short_customers, counts, color=COLORS["purple"], edgecolor=COLORS["border"], height=0.5)
            ax2.set_facecolor(COLORS["bg_card"])
            ax2.tick_params(colors=COLORS["text_secondary"], labelsize=9)
            ax2.set_title("أكثر العملاء تعاملاً", color=COLORS["text_primary"], fontsize=11, pad=8)
            ax2.set_xlabel("عدد العمليات", color=COLORS["text_secondary"], fontsize=9)
            
            # إضافة القيم على الأعمدة
            for bar in bars2:
                width = bar.get_width()
                ax2.text(width + 0.05, bar.get_y() + bar.get_height()/2.,
                        f'{int(width)}', ha='left', va='center',
                        color=COLORS["text_primary"], fontsize=8)
        
        else:
            ax2.text(0.5, 0.5, "لا توجد بيانات", 
                    ha='center', va='center',
                    color=COLORS["text_secondary"], fontsize=12)
            ax2.set_facecolor(COLORS["bg_card"])
        
        fig2.tight_layout(pad=2)
        
        # إضافة الرسوم البيانية إلى الواجهة (عمودي للشاشات الضيقة)
        canvas1 = FigureCanvasTkAgg(fig1, self.charts_container)
        canvas1.draw()
        canvas1.get_tk_widget().pack(fill="x", pady=(0, 10))
        
        canvas2 = FigureCanvasTkAgg(fig2, self.charts_container)
        canvas2.draw()
        canvas2.get_tk_widget().pack(fill="x")
    
    # باقي الدوال تبقى كما هي مع بعض التعديلات الطفيفة
    
    def update_stats_cards(self):
        """تحديث كروت الإحصائيات"""
        total_scales = self.db.get_total_scales()
        today_scales = self.db.get_today_scales()
        month_scales = self.db.get_month_scales()
        unique_customers = self.db.get_unique_customers()
        unique_cars = self.db.get_unique_cars()
        
        stats_values = [
            f"{total_scales:,}",
            f"{today_scales:,}",
            f"{month_scales:,}",
            f"{unique_customers:,}",
            f"{unique_cars:,}"
        ]
        
        for i, card in enumerate(self.stats_cards):
            card["value_label"].configure(text=stats_values[i])
    
    def calculate_weight_stats(self, data):
        """حساب إحصائيات الوزن"""
        if not data:
            return {
                "total_net": 0,
                "avg_net": 0,
                "max_net": 0,
                "min_net": 0
            }
        
        net_weights = []
        for row in data:
            try:
                first_weight = float(row["first_weight"])
                last_weight = float(row["last_weight"])
                net_weight = last_weight - first_weight
                if net_weight > 0:
                    net_weights.append(net_weight)
            except:
                continue
        
        if not net_weights:
            return {
                "total_net": 0,
                "avg_net": 0,
                "max_net": 0,
                "min_net": 0
            }
        
        return {
            "total_net": sum(net_weights),
            "avg_net": sum(net_weights) / len(net_weights),
            "max_net": max(net_weights),
            "min_net": min(net_weights)
        }
    
    def calculate_time_stats(self, data):
        """حساب إحصائيات الزمن"""
        if not data:
            return {
                "avg_time": 0,
                "max_time": 0,
                "min_time": 0,
                "total_time": 0
            }
        
        times_in_minutes = []
        for row in data:
            try:
                first_time = datetime.strptime(f"{row['first_date']} {row['first_time']}", "%Y-%m-%d %H:%M:%S")
                last_time = datetime.strptime(f"{row['last_date']} {row['last_time']}", "%Y-%m-%d %H:%M:%S")
                
                time_diff = (last_time - first_time).total_seconds() / 60
                if time_diff > 0:
                    times_in_minutes.append(time_diff)
            except:
                continue
        
        if not times_in_minutes:
            return {
                "avg_time": 0,
                "max_time": 0,
                "min_time": 0,
                "total_time": 0
            }
        
        return {
            "avg_time": sum(times_in_minutes) / len(times_in_minutes),
            "max_time": max(times_in_minutes),
            "min_time": min(times_in_minutes),
            "total_time": sum(times_in_minutes) / 60
        }
    
    def update_weight_analytics(self, data):
        """تحديث تحليلات الوزن"""
        stats = self.calculate_weight_stats(data)
        
        self.weight_stats_labels["إجمالي الوزن الصافي"].configure(
            text=f"{stats['total_net']:,.0f} kg"
        )
        self.weight_stats_labels["متوسط الوزن الصافي"].configure(
            text=f"{stats['avg_net']:,.0f} kg"
        )
        self.weight_stats_labels["أعلى وزن صافي"].configure(
            text=f"{stats['max_net']:,.0f} kg"
        )
        self.weight_stats_labels["أقل وزن صافي"].configure(
            text=f"{stats['min_net']:,.0f} kg"
        )
    
    def update_time_analytics(self, data):
        """تحديث التحليلات الزمنية"""
        stats = self.calculate_time_stats(data)
        
        self.time_stats_labels["متوسط زمن العملية"].configure(
            text=f"{stats['avg_time']:.0f} دقيقة"
        )
        self.time_stats_labels["أطول عملية وزن"].configure(
            text=f"{stats['max_time']:.0f} دقيقة"
        )
        self.time_stats_labels["أسرع عملية وزن"].configure(
            text=f"{stats['min_time']:.0f} دقيقة"
        )
        self.time_stats_labels["إجمالي الزمن"].configure(
            text=f"{stats['total_time']:.0f} ساعة"
        )
    
    def update_table(self, data):
        """تحديث جدول البيانات"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for row in data:
            try:
                first_weight = float(row["first_weight"])
                last_weight = float(row["last_weight"])
                net_weight = last_weight - first_weight
                
                self.tree.insert("", "end", values=(
                    row["id"],
                    row["customer_name"],
                    row["load_type"],
                    row["car_number"],
                    f"{net_weight:.0f} kg",
                    row["last_date"]
                ))
            except:
                continue
    
    def filter_table(self):
        """تصفية الجدول بناءً على البحث"""
        search_term = self.search_entry.get().lower()
        
        data = self.db.get_scales_data(
            self.start_date_var.get() if self.start_date_var.get() else None,
            self.end_date_var.get() if self.end_date_var.get() else None,
            self.customer_var.get() if self.customer_var.get() != "الكل" else None,
            self.load_type_var.get() if self.load_type_var.get() != "الكل" else None,
            self.governorate_var.get() if self.governorate_var.get() != "الكل" else None
        )
        
        if search_term:
            filtered_data = []
            for row in data:
                if (search_term in str(row["id"]).lower() or 
                    search_term in row["customer_name"].lower()):
                    filtered_data.append(row)
            data = filtered_data
        
        self.update_table(data)
        self.update_weight_analytics(data)
        self.update_time_analytics(data)
    
    def update_dashboard(self):
        """تحديث جميع أجزاء الداشبورد"""
        data = self.db.get_scales_data(
            self.start_date_var.get() if self.start_date_var.get() else None,
            self.end_date_var.get() if self.end_date_var.get() else None,
            self.customer_var.get() if self.customer_var.get() != "الكل" else None,
            self.load_type_var.get() if self.load_type_var.get() != "الكل" else None,
            self.governorate_var.get() if self.governorate_var.get() != "الكل" else None
        )
        
        self.update_stats_cards()
        self.update_weight_analytics(data)
        self.update_time_analytics(data)
        self.update_charts()
        self.update_table(data)
        
        print("✅ تم تحديث الداشبورد بنجاح")
    
    def clear_filters(self):
        """مسح جميع الفلاتر"""
        self.start_date_var.set("")
        self.end_date_var.set("")
        self.customer_var.set("الكل")
        self.load_type_var.set("الكل")
        self.governorate_var.set("الكل")
        self.search_entry.delete(0, "end")
        
        self.update_dashboard()
    
    def print_today_report(self):
        """طباعة تقرير اليوم"""
        today = datetime.now().strftime("%Y-%m-%d")
        data = self.db.get_scales_data(start_date=today, end_date=today)
        
        if not data:
            print("⚠️ لا توجد عمليات وزن اليوم")
            return
        
        report = f"""
        ====================================
        تقرير يومي - ميزان بسكول
        التاريخ: {today}
        ====================================
        
        إجمالي عمليات الوزن اليوم: {len(data)}
        
        تفاصيل العمليات:
        """
        
        total_net_weight = 0
        for row in data:
            try:
                first_weight = float(row["first_weight"])
                last_weight = float(row["last_weight"])
                net_weight = last_weight - first_weight
                total_net_weight += net_weight
                
                report += f"""
                العملية #{row['id']}:
                العميل: {row['customer_name']}
                نوع الحمولة: {row['load_type']}
                رقم العربية: {row['car_number']}
                الوزن الصافي: {net_weight:.0f} kg
                ---
                """
            except:
                continue
        
        report += f"""
        ====================================
        إجمالي الوزن الصافي اليوم: {total_net_weight:.0f} kg
        ====================================
        """
        
        print(report)
        print("✅ تم إنشاء تقرير اليوم")
