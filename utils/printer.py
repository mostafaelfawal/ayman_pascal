from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import mm
import arabic_reshaper
from bidi.algorithm import get_display

# ====== Register Arabic Font ======
pdfmetrics.registerFont(TTFont('Amiri', 'assets/fonts/Amiri-Regular.ttf'))

def ar(text):
    reshaped = arabic_reshaper.reshape(text)
    return get_display(reshaped)

# ========== DATA INPUT ==========
customer_name   = "شركة النور للنقل"
load_type       = "أسمنت"
car_number      = "س ج ه 2345"
governorate     = "القاهرة"
first_time      = "10:35 صباحاً"
first_date      = "23-11-2025"
first_weight    = "35000"

last_time       = "11:10 صباحاً"
last_date       = "23-11-2025"
last_weight     = "12000"

net_weight      = str(int(first_weight) - int(last_weight))  # الوزن الصافي

# ========== START PDF ==========
c = canvas.Canvas("bascule_invoice.pdf", pagesize=A4)
c.setFont("Amiri", 14)

# ======== Header ========
c.drawImage("assets/icon.png", 20, 760, width=80, height=60)  # Logo (اختياري)
c.setFont("Amiri", 18)
c.drawCentredString(105*mm, 285*mm, ar("أيمــن للمــوازين"))
c.setFont("Amiri", 13)
c.drawCentredString(105*mm, 275*mm, ar("فاتــورة وزنة - ميزان بسكول"))

# ======== Customer & Car Info ========
c.setFont("Amiri", 12)
y = 250

c.drawRightString(195*mm, y*mm, ar(f"العميل: {customer_name}"))
y -= 8
c.drawRightString(195*mm, y*mm, ar(f"نوع الحمولة: {load_type}"))
y -= 8
c.drawRightString(195*mm, y*mm, ar(f"رقم السيارة: {car_number}"))
y -= 8
c.drawRightString(195*mm, y*mm, ar(f"المحافظة: {governorate}"))

# ======== Separator Line ========
c.line(15*mm, (y-4)*mm, 195*mm, (y-4)*mm)
y -= 20

# ======== First Weight ========
c.setFont("Amiri", 13)
c.drawRightString(195*mm, y*mm, ar("الــوزن الأول"))
y -= 10
c.setFont("Amiri", 12)
c.drawRightString(195*mm, y*mm, ar(f"الوقت: {first_time}"))
y -= 8
c.drawRightString(195*mm, y*mm, ar(f"التاريخ: {first_date}"))
y -= 8
c.drawRightString(195*mm, y*mm, ar(f"الوزن: {first_weight} كجم"))

# ======== Separator Line ========
y -= 5
c.line(15*mm, y*mm, 195*mm, y*mm)
y -= 20

# ======== Last Weight ========
c.setFont("Amiri", 13)
c.drawRightString(195*mm, y*mm, ar("الــوزن الثاني"))
y -= 10
c.setFont("Amiri", 12)
c.drawRightString(195*mm, y*mm, ar(f"الوقت: {last_time}"))
y -= 8
c.drawRightString(195*mm, y*mm, ar(f"التاريخ: {last_date}"))
y -= 8
c.drawRightString(195*mm, y*mm, ar(f"الوزن: {last_weight} كجم"))

# ======== Separator Line ========
y -= 5
c.line(15*mm, y*mm, 195*mm, y*mm)
y -= 20

# ======== Net Weight ========
c.setFont("Amiri", 15)
c.drawRightString(195*mm, y*mm, ar(f"الوزن الصافي: {net_weight} كجم"))
y -= 15

c.setFont("Amiri", 11)
c.drawRightString(195*mm, y*mm, ar("ملاحظة: الوزن الصافي = الوزن الأول - الوزن الثاني"))

# ======== Footer ========
c.setFont("Amiri", 12)
c.drawCentredString(105*mm, 20*mm, ar("شكراً لاستخدامكم برنامج أيمن للموازين"))

c.showPage()
c.save()

print("bascule_invoice.pdf Saved!")
