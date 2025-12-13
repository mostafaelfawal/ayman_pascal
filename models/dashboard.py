import sqlite3
from datetime import datetime

class DashboardDB:
    """فصل للتعامل مع قاعدة البيانات خاصة بالتقارير"""
    
    def __init__(self):
        self.conn = sqlite3.connect("db/scale.db")
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
    
    def get_total_scales(self):
        """الحصول على إجمالي عدد عمليات الوزن"""
        self.cursor.execute("SELECT COUNT(*) FROM scales")
        return self.cursor.fetchone()[0]
    
    def get_today_scales(self):
        """الحصول على عدد وزنات اليوم"""
        today = datetime.now().strftime("%Y-%m-%d")
        self.cursor.execute("SELECT COUNT(*) FROM scales WHERE last_date = ?", (today,))
        return self.cursor.fetchone()[0]
    
    def get_month_scales(self):
        """الحصول على عدد وزنات الشهر الحالي"""
        current_month = datetime.now().strftime("%Y-%m")
        self.cursor.execute("SELECT COUNT(*) FROM scales WHERE last_date LIKE ?", (f"{current_month}%",))
        return self.cursor.fetchone()[0]
    
    def get_unique_customers(self):
        """الحصول على عدد العملاء المختلفين"""
        self.cursor.execute("SELECT COUNT(DISTINCT customer_name) FROM scales")
        return self.cursor.fetchone()[0]
    
    def get_unique_cars(self):
        """الحصول على عدد السيارات المختلفة"""
        self.cursor.execute("SELECT COUNT(DISTINCT car_number) FROM scales")
        return self.cursor.fetchone()[0]
    
    def get_scales_data(self, start_date=None, end_date=None, customer=None, load_type=None, governorate=None):
        """الحصول على بيانات الوزن مع الفلاتر"""
        query = "SELECT * FROM scales WHERE 1=1"
        params = []
        
        if start_date and end_date:
            query += " AND last_date BETWEEN ? AND ?"
            params.extend([start_date, end_date])
        elif start_date:
            query += " AND last_date >= ?"
            params.append(start_date)
        elif end_date:
            query += " AND last_date <= ?"
            params.append(end_date)
        
        if customer and customer != "الكل":
            query += " AND customer_name = ?"
            params.append(customer)
        
        if load_type and load_type != "الكل":
            query += " AND load_type = ?"
            params.append(load_type)
        
        if governorate and governorate != "الكل":
            query += " AND governorate = ?"
            params.append(governorate)
        
        query += " ORDER BY last_date DESC, last_time DESC"
        self.cursor.execute(query, params)
        return self.cursor.fetchall()
    
    def get_customers_list(self):
        """الحصول على قائمة العملاء"""
        self.cursor.execute("SELECT DISTINCT customer_name FROM scales ORDER BY customer_name")
        return [row[0] for row in self.cursor.fetchall()]
    
    def get_load_types(self):
        """الحصول على قائمة أنواع الحمولة"""
        self.cursor.execute("SELECT DISTINCT load_type FROM scales ORDER BY load_type")
        return [row[0] for row in self.cursor.fetchall()]
    
    def get_governorates(self):
        """الحصول على قائمة المحافظات"""
        self.cursor.execute("SELECT DISTINCT governorate FROM scales ORDER BY governorate")
        return [row[0] for row in self.cursor.fetchall()]
    
    def get_daily_stats(self, start_date=None, end_date=None):
        """الحصول على إحصائيات يومية"""
        if start_date and end_date:
            query = """
                SELECT last_date, COUNT(*) as count 
                FROM scales 
                WHERE last_date BETWEEN ? AND ?
                GROUP BY last_date 
                ORDER BY last_date
            """
            params = [start_date, end_date]
        else:
            query = """
                SELECT last_date, COUNT(*) as count 
                FROM scales 
                GROUP BY last_date 
                ORDER BY last_date 
                LIMIT 30
            """
            params = []
        
        self.cursor.execute(query, params)
        return self.cursor.fetchall()
    
    def get_customer_stats(self, start_date=None, end_date=None):
        """الحصول على إحصائيات العملاء"""
        if start_date and end_date:
            query = """
                SELECT customer_name, COUNT(*) as count 
                FROM scales 
                WHERE last_date BETWEEN ? AND ?
                GROUP BY customer_name 
                ORDER BY count DESC 
                LIMIT 10
            """
            params = [start_date, end_date]
        else:
            query = """
                SELECT customer_name, COUNT(*) as count 
                FROM scales 
                GROUP BY customer_name 
                ORDER BY count DESC 
                LIMIT 10
            """
            params = []
        
        self.cursor.execute(query, params)
        return self.cursor.fetchall()
    
    def close(self):
        """إغلاق الاتصال بقاعدة البيانات"""
        self.conn.close()