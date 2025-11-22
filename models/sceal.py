from sqlite3 import connect

class ScealDB:
    def __init__(self):
        self.con = connect("db/sceal.db")
        self.cur = self.con.cursor()
        
        self.cur.execute("""CREATE TABLE IF NOT EXISTS sceals(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT,
            load_type TEXT,
            car_number TEXT,
            governorate TEXT,
            time TEXT,
            date TEXT,
            first_weight TEXT,
            last_weight TEXT,
            notes TEXT
            )""")
        
        self.con.commit()
    
    def add_sceal(self, customer_name, load_type, car_number, governorate, time, date, first_weight, last_weight, notes):
        self.cur.execute("""INSERT INTO sceals
        (customer_name, load_type, car_number, governorate, time, date, first_weight, last_weight, notes) VALUES
        (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (customer_name, load_type, car_number, governorate, time, date, first_weight, last_weight, notes))
        self.con.commit()
    
    def delete_sceal(self, id):
        self.cur.execute("DELETE FROM sceals WHERE id=?", (id, ))
        self.con.commit()
    
    def edit_sceal(self, customer_name, load_type, car_number, governorate, time, date, first_weight, last_weight, notes, id):
        self.cur.execute("""UPDATE sceals SET customer_name=?, load_type=?, car_number=?, governorate=?, time=?, date=?, first_weight=?, last_weight=?, notes=? WHERE id=?""",
                         (customer_name, load_type, car_number, governorate, time, date, first_weight, last_weight, notes, id))
        self.con.commit()
    
    def get_sceals(self):
        self.cur.execute("SELECT * FROM sceals")
        rows = self.cur.fetchall()
        return rows