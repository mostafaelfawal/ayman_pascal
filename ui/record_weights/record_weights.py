from customtkinter import CTkFrame, CTkLabel, CTkButton
from ui.record_weights.record_search import RecordSearch
from ui.record_weights.record_tree import RecordTree
from ui.record_weights.record_actions import RecordActions
from tkinter.messagebox import askokcancel, showinfo, showerror
from models.scale import ScaleDB
from utils.clear_frame import clear_frame
from utils.load_image import load_image
from ui.new_weights.new_weights_main import NewWeights
from ui.edit_weight import EditWeight

class RecordWeights:
    def __init__(self, root):
        self.root = root
        self.db = ScaleDB()
        self.selected_id = ""
        # pagination state
        self.page_size = 12
        self.current_page = 1
        self.total_pages = 1
        self.current_search = ""
        self.load_images()
        RecordSearch(self).build()
        self.container = CTkFrame(self.root, fg_color="transparent")
        self.container.pack(fill="both", expand=True, padx=10, pady=10)
        # build actions first (contains pagination UI) then load data
        RecordActions(self).build()
        self.load_data()

    def load_images(self):
        self.search_icon = load_image("assets/search_icon.png", (20, 20))
        self.update_data = load_image("assets/update_data.png")
        self.add_icon = load_image("assets/add.png")
        self.delete_icon = load_image("assets/delete.png")
        self.edit_icon = load_image("assets/edit.png")
        
    # =====================================================
    # اضافة البحث محسنة
    # =====================================================
    # search UI moved to ui/record_search.py

    def search_records(self):
        """منطق البحث داخل السجلات"""
        query = self.search_var.get().strip()

        if not hasattr(self, "tree"):
            return

        # reset search and pagination
        self.current_search = query
        self.current_page = 1

        # clear existing rows
        for item in self.tree.get_children():
            self.tree.delete(item)

        # fetch total and first page for search
        total = self.db.get_scales_count(search=query)
        if total == 0:
            self._update_pagination(0)
            self.tree.insert("", "end", values=("", "", "❌ لا يوجد نتائج مطابقة لعبارة البحث", "", ""))
            return

        offset = (self.current_page - 1) * self.page_size
        rows = self.db.get_scales(limit=self.page_size, offset=offset, search=query)
        self._update_pagination(total)

        for row in rows:
            self.tree.insert("", "end", values=(row[0], row[1], row[2], row[5], row[8]))

    def to_new_record(self):
        clear_frame(self.root)
        NewWeights(self.root)

    # =====================================================
    # Treeview
    # =====================================================

    # tree UI moved to ui/record_tree.py

    # tree theming moved to ui/record_tree.py
    
    def reload_treeview(self):
        """إعادة تحميل بيانات التري بدون تدمير كامل الواجهة"""
        if not hasattr(self, "tree"):
            return

        for item in self.tree.get_children():
            self.tree.delete(item)

        offset = (self.current_page - 1) * self.page_size
        rows = self.db.get_scales(limit=self.page_size, offset=offset, search=self.current_search)
        total = self.db.get_scales_count(search=self.current_search)
        self._update_pagination(total)

        for row in rows:
            self.tree.insert("", "end", values=(
                row[0], row[1], row[2], row[5], row[8]
            ))

    # =====================================================
    # تحميل البيانات 
    # =====================================================
    def load_data(self):
        # calculate total and load the current page
        total = self.db.get_scales_count(search=self.current_search)
        rows = self.db.get_scales(limit=self.page_size, offset=(self.current_page - 1) * self.page_size, search=self.current_search)
        
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

        # create and attach tree UI
        RecordTree(self).build()
                
        # تعبئة التري فيو
        for row in rows:
            _id = row[0]
            name = row[1]
            load = row[2]
            first_w = row[5]
            last_w = row[8]

            self.tree.insert("", "end", values=(_id, name, load, first_w, last_w))

        # update page label
        self._update_pagination(total)

    # =====================================================
    # إطار الأزرار 
    # =====================================================
    # actions frame moved to ui/record_actions.py

    def on_tree_click(self, event):
        item = self.tree.focus()
        if not item:
            return

        values = self.tree.item(item, "values")
        if values and values[0] != "":
            self.selected_id = values[0]

    # =====================================================
    # Pagination helpers
    # =====================================================
    def _update_pagination(self, total_rows: int):
        # calculate total pages and sanitize current_page
        self.total_pages = max(1, (total_rows + self.page_size - 1) // self.page_size)
        if self.current_page < 1:
            self.current_page = 1
        if self.current_page > self.total_pages:
            self.current_page = self.total_pages

        # update UI label if present
        if hasattr(self, 'page_label'):
            try:
                self.page_label.configure(text=f"صفحة {self.current_page}/{self.total_pages}")
            except Exception:
                pass

    def next_page(self):
        if self.current_page < self.total_pages:
            self.current_page += 1
            self.reload_treeview()

    def prev_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.reload_treeview()

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
        
        EditWeight(self.selected_id, self.reload_treeview)
        self.selected_id = ""
