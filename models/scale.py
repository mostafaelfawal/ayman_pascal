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
        self.cur.execute("""INSERT INTO scales
        (customer_name, load_type, car_number, governorate, first_time, first_date, first_weight, last_time, last_date, last_weight) VALUES
        (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (customer_name, load_type, car_number, governorate, first_time, first_date, first_weight, last_time, last_date, last_weight))
        self.con.commit()
    
    def delete_scale(self, id):
        self.cur.execute("DELETE FROM scales WHERE id=?", (id, ))
        self.con.commit()
    
    def edit_scale(self, customer_name, load_type, car_number, governorate, first_time, first_date, first_weight, last_time, last_date, last_weight, id):
        self.cur.execute("""UPDATE scales SET customer_name=?, load_type=?, car_number=?, governorate=?, first_time=?, first_date=?, first_weight=?, last_time=?, last_date=?, last_weight=? WHERE id=?""",
                         (customer_name, load_type, car_number, governorate, first_time, first_date, first_weight, last_time, last_date, last_weight, id))
        self.con.commit()
    
    def get_scales(self):
        self.cur.execute("SELECT * FROM scales")
        rows = self.cur.fetchall()
        return rows