from json import load, dump
from bcrypt import checkpw, hashpw, gensalt
from os.path import exists

FILE = "settings.json"

def ensure_file_exists():
    """تأكد من وجود الملف، إذا مش موجود انشئه مع password = 'admin'"""
    if not exists(FILE):
        hashed = hashpw("admin".encode(), gensalt())
        dump({
            "password": hashed.decode(),
            "is_security": True,
            "company_name": "أيمن للموازين",
            "company_phone": "01008454579",
            "company_email": "ayman_scale@gmail.com",
            "company_address": "مصر - فوه كفر الشيخ",
            "scale_port": "COM1",
            "scale_baudrate": "9600",
            "printer_name": "",
            "printer_type": "thermal",
            "invoices_per_print": 1
        }, open(FILE, "w"), indent=4)

def update_settings_by_key(key, value):
    """تعديل مفتاح محدد في JSON بدون مسح باقي البيانات"""
    ensure_file_exists()
    with open(FILE, "r") as f:
        data = load(f)
    data[key] = value
    with open(FILE, "w") as f:
        dump(data, f, indent=4)

def get_setting_by_key(key):
    """جلب بيانات بواسطة مفتاح محدد في JSON"""
    ensure_file_exists()
    with open(FILE, "r") as f:
        data = load(f)
    # return None if key doesn't exist (backwards compatible with older settings files)
    return data.get(key)

def check_password(password: str) -> bool:
    """تحقق من الباسورد المدخل مقابل المخزن في JSON"""
    ensure_file_exists()
    with open(FILE, "r") as f:
        data = load(f)
    hashed = data["password"].encode()
    return checkpw(password.encode(), hashed)

def save_password(password: str):
    """احفظ كلمة مرور جديدة في JSON بدون مسح باقي البيانات"""
    ensure_file_exists()
    with open(FILE, "r") as f:
        data = load(f)
    data["password"] = hashpw(password.encode(), gensalt()).decode()
    with open(FILE, "w") as f:
        dump(data, f, indent=4)
