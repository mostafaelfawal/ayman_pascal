import win32print
import win32ui
from PIL import Image, ImageDraw, ImageFont, ImageWin
import arabic_reshaper
from bidi.algorithm import get_display
from utils.settings_work import get_setting_by_key
from utils.calc_net_weight import calc_net_weight
from tkinter.messagebox import showinfo, showerror

FONT_PATH = "assets/fonts/Amiri-Bold.ttf"


def ar(text, font):
    """كتابة النص العربي مظبوط"""
    reshaped = arabic_reshaper.reshape(str(text))
    bidi = get_display(reshaped)
    return bidi, font


def draw_ar(draw, x, y, text, font, fill="black"):
    reshaped = arabic_reshaper.reshape(str(text))
    bidi = get_display(reshaped)
    draw.text((x, y), bidi, font=font, fill=fill)


def generate_arabic_invoice(entries, invoice_id, img_width=550):

    # بيانات الشركة
    company = get_setting_by_key("company_name") or "ايمن للموازين"
    phone = get_setting_by_key("company_phone") or "01008454579"
    address = get_setting_by_key("company_address") or "فوه كفر الشيخ - مصر"

    # إدخالات المستخدم
    client = entries["اسم العميل"].get()
    car_no = entries["رقم السيارة"].get()
    cargo = entries["نوع الحمولة"].get()
    gov = entries["المحافظة"].get()

    w1_time = entries["weight1_time"].get()
    w1_date = entries["weight1_date"].get()
    w1_val = entries["weight1_weight"].get()

    w2_time = entries["weight2_time"].get()
    w2_date = entries["weight2_date"].get()
    w2_val = entries["weight2_weight"].get()
    net_w = calc_net_weight(w1_val, w2_val)
    price = entries["السعر"].get()

    # إعدادات الخط
    f_title = ImageFont.truetype(FONT_PATH, 42)
    f_section = ImageFont.truetype(FONT_PATH, 36)
    f_regular = ImageFont.truetype(FONT_PATH, 30)
    f_bold = ImageFont.truetype(FONT_PATH, 38)
    img_height = 2000
    img = Image.new("RGB", (img_width, img_height), "white")
    d = ImageDraw.Draw(img)

    y = 20

    # ====== رأس الفاتورة ======
    draw_ar(d, 20, y, company, f_title)
    y += 60

    draw_ar(d, 20, y, address, f_regular)
    y += 35

    draw_ar(d, 20, y, f"هاتف: {phone}", f_regular)
    y += 45

    d.line((10, y, img_width-10, y), fill="black", width=2)
    y += 25

    draw_ar(d, 20, y, f"رقم الفاتورة: {invoice_id}", f_section)
    y += 50

    d.line((10, y, img_width-10, y), fill="black", width=2)
    y += 25

    # ====== بيانات العميل ======
    draw_ar(d, 20, y, "بيانات العميل", f_section)
    y += 50

    box_h = 180
    d.rectangle((10, y, img_width-10, y + box_h), outline="black", width=2)

    y += 15
    draw_ar(d, 20, y, f"اسم العميل: {client}", f_regular)
    y += 40

    draw_ar(d, 20, y, f"رقم السيارة: {car_no}", f_regular)
    y += 40

    draw_ar(d, 20, y, f"نوع الحمولة: {cargo}", f_regular)
    y += 40

    draw_ar(d, 20, y, f"المحافظة: {gov}", f_regular)
    y += 55

    # ====== قسم الوزن ======
    d.line((10, y, img_width-10, y), fill="black", width=2)
    y += 25

    draw_ar(d, 20, y, "تفاصيل الوزن", f_section)
    y += 50

    # رؤوس الجدول
    d.rectangle((10, y, img_width-10, y+45), outline="black", width=2)
    draw_ar(d, 25, y+8, "الوصف", f_regular)
    draw_ar(d, 180, y+8, "الوزن", f_regular)
    draw_ar(d, 310, y+8, "التاريخ", f_regular)
    draw_ar(d, 430, y+8, "الوقت", f_regular)
    y += 60

    # الصف 1
    d.rectangle((10, y, img_width-10, y+45), outline="black", width=1)
    draw_ar(d, 25, y+8, "الوزنة الأولى", f_regular)
    draw_ar(d, 180, y+8, w1_val, f_regular)
    draw_ar(d, 310, y+8, w1_date, f_regular)
    draw_ar(d, 430, y+8, w1_time, f_regular)
    y += 55

    # الصف 2
    d.rectangle((10, y, img_width-10, y+45), outline="black", width=1)
    draw_ar(d, 25, y+8, "الوزنة الثانية", f_regular)
    draw_ar(d, 180, y+8, w2_val, f_regular)
    draw_ar(d, 310, y+8, w2_date, f_regular)
    draw_ar(d, 430, y+8, w2_time, f_regular)
    y += 70

    # ====== الوزن الصافي ======
    d.rectangle((10, y, img_width-10, y+85), outline="black", width=3)
    draw_ar(d, 20, y+10, "الوزن الصافي", f_bold)
    draw_ar(d, img_width-180, y+5, f"{net_w} كجم", f_bold)
    y += 110

    # خط سفلي
    d.line((10, y, img_width-10, y), fill="black", width=2)
    y += 20
    # ===== السعر =====
    d.rectangle((10, y, img_width-10, y+85), outline="black", width=3)
    draw_ar(d, 20, y+10, "السعر", f_bold)
    draw_ar(d, img_width-180, y+5, f"{price} جنيه", f_bold)
    y += 110

    # خط سفلي
    d.line((10, y, img_width-10, y), fill="black", width=2)
    y += 20

    # ====== فوتر بسيط ======
    draw_ar(d, 20, y, "شكراً لثقتكم", f_regular)
    y += 40

    img = img.crop((0, 0, img_width, y + 10))
    return img


def print_image_to_printer(img, printer_name="GP-L80180 Series"):

    hprinter = win32print.OpenPrinter(printer_name)
    hdc = win32ui.CreateDC()
    hdc.CreatePrinterDC(printer_name)

    hdc.StartDoc("Arabic Receipt")
    hdc.StartPage()

    dib = ImageWin.Dib(img)
    dib.draw(hdc.GetHandleOutput(), (0, 0, img.width, img.height))

    hdc.EndPage()
    hdc.EndDoc()
    win32print.ClosePrinter(hprinter)


def print_scale_thermal(entries, invoice_id="INV-001"):
    try:
        img = generate_arabic_invoice(entries, invoice_id)
        print_image_to_printer(img)
        showinfo("تم", f"تمت طباعة الفاتورة رقم {invoice_id}")
    except Exception as e:
        print(e)
        showerror("خطأ", f"حدث خطأ أثناء الطباعة: {e}")
