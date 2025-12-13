from sqlite3 import connect

class ScaleDB:
    def __init__(self):
        self.con = connect("db/scale.db")
        self.cur = self.con.cursor()
        
        self.cur.execute("""CREATE TABLE IF NOT EXISTS scales(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT,
            load_type TEXT,
            car_number TEXT,
            governorate TEXT,
            first_weight TEXT,
            first_time TEXT,
            first_date TEXT,
            last_weight TEXT,
            last_time TEXT,
            last_date TEXT
            )""")
        
        self.con.commit()
    
    def add_scale(self, customer_name, load_type, car_number, governorate, first_time, first_date, first_weight, last_time, last_date, last_weight):
        """إضافة وزن جديد"""
        self.cur.execute("""INSERT INTO scales
        (customer_name, load_type, car_number, governorate, first_time, first_date, first_weight, last_time, last_date, last_weight) VALUES
        (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (customer_name, load_type, car_number, governorate, first_time, first_date, first_weight, last_time, last_date, last_weight))
        self.con.commit()
    
    def delete_scale(self, id):
        self.cur.execute("DELETE FROM scales WHERE id=?", (id, ))
        self.con.commit()
    
    def edit_scale(self, customer_name, load_type, car_number, governorate, first_time, first_date, first_weight, last_time, last_date, last_weight, id):
        """تعديل بيانات الوزن """
        self.cur.execute("""UPDATE scales SET customer_name=?, load_type=?, car_number=?, governorate=?, first_time=?, first_date=?, first_weight=?, last_time=?, last_date=?, last_weight=? WHERE id=?""",
                         (customer_name, load_type, car_number, governorate, first_time, first_date, first_weight, last_time, last_date, last_weight, id))
        self.con.commit()
        
    def get_scales(self, limit=None, offset=0, search=None):
        """Return scales with optional pagination and simple search.

        Args:
            limit: maximum number of rows to return (None => no LIMIT)
            offset: rows to skip
            search: optional string to filter by id or customer_name (SQL LIKE)
        """
        sql = "SELECT * FROM scales"
        params = []

        if search:
            sql += " WHERE customer_name LIKE ? OR CAST(id AS TEXT) LIKE ?"
            q = f"%{search}%"
            params.extend([q, q])

        if limit is not None:
            sql += " LIMIT ? OFFSET ?"
            params.extend([limit, offset])

        self.cur.execute(sql, tuple(params))
        rows = self.cur.fetchall()
        return rows

    def get_scales_count(self, search=None):
        """Return total number of scales (optionally filtered by search)."""
        sql = "SELECT COUNT(*) FROM scales"
        params = []
        if search:
            sql += " WHERE customer_name LIKE ? OR CAST(id AS TEXT) LIKE ?"
            q = f"%{search}%"
            params.extend([q, q])

        self.cur.execute(sql, tuple(params))
        result = self.cur.fetchone()
        return result[0] if result else 0
    
    def get_scale_by_id(self, id):
        self.cur.execute("SELECT * FROM scales WHERE id=?", (id,))
        data = self.cur.fetchone()
        return data
    
    def get_invoice_num(self):
        """إرجاع آخر id مُضاف في جدول scales"""
        self.cur.execute("SELECT MAX(id) FROM scales")
        result = self.cur.fetchone()
        return result[0] + 1 if result and result[0] is not None else 0