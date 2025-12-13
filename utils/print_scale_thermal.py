import win32print
import win32ui
from PIL import Image, ImageDraw, ImageFont, ImageWin
import arabic_reshaper
from bidi.algorithm import get_display
from utils.settings_work import get_setting_by_key
from utils.calc_net_weight import calc_net_weight
from tkinter.messagebox import showinfo, showerror
import datetime
from math import ceil

FONT_BOLD = "assets/fonts/NotoNaskhArabic-Bold.ttf"

def ar(text):
    text = to_arabic_digits(text)
    reshaped = arabic_reshaper.reshape(text)
    return get_display(reshaped)

def draw_ar(d, x, y, text, font, fill="black", anchor="ra"):
    d.text((x, y), ar(text), font=font, fill=fill, anchor=anchor)

def draw_center_ar(d, x, y, text, font):
    bbox = d.textbbox((0, 0), ar(text), font=font)
    w = bbox[2] - bbox[0]
    d.text((x - w / 2, y), ar(text), font=font, fill="black")

def to_arabic_digits(text):
    arabic_digits = str.maketrans("0123456789", "٠١٢٣٤٥٦٧٨٩")
    return str(text).translate(arabic_digits)

def generate_arabic_invoice(entries, invoice_id, img_width=550):

    company = get_setting_by_key("company_name") or "مضرب وبسكول عوض للاستيراد والتصدير"
    phone = get_setting_by_key("company_phone") or "01000000000"
    address = get_setting_by_key("company_address") or "فوه - كفر الشيخ"

    client = entries["اسم العميل"].get()
    car_no = entries["رقم السيارة"].get()
    cargo = entries["نوع الحمولة"].get()

    w1_val = entries["weight1_weight"].get()
    w2_val = entries["weight2_weight"].get()
    net_w = calc_net_weight(w1_val, w2_val)


    today = datetime.datetime.now()
    date = today.strftime("%Y/%m/%d")
    time = today.strftime("%H:%M")

    f_title = ImageFont.truetype(FONT_BOLD, 30)
    f_bold = ImageFont.truetype(FONT_BOLD, 28)
    f_reg = ImageFont.truetype(FONT_BOLD, 26)
    f_big = ImageFont.truetype(FONT_BOLD, 42)
    f_small = ImageFont.truetype(FONT_BOLD, 22)

    img = Image.new("1", (img_width, 2000), "white")
    d = ImageDraw.Draw(img)
    y = 20

    # ===== HEADER =====
    header_h = 140
    d.rectangle((20, y, img_width - 20, y + header_h), outline="black", width=3)
    draw_center_ar(d, img_width // 2, y + 15, company, f_title)
    draw_center_ar(d, img_width // 2, y + 55, address, f_small)
    draw_center_ar(d, img_width // 2, y + 85, phone, f_small)
    y += header_h + 20

    # ===== INFO TABLE =====
    row_h = 55
    info_rows = [
        ("الرقم", invoice_id),
        ("التاريخ", date),
        ("الوقت", time),
        ("رقم السيارة", car_no),
        ("اسم العميل", client),
        ("نوع الحمولة", cargo),
    ]

    for label, value in info_rows:
        d.rectangle((20, y, img_width - 20, y + row_h), outline="black", width=1)
        d.line((img_width // 2, y, img_width // 2, y + row_h), fill="black", width=1)

        draw_ar(d, img_width - 30, y + 15, label, f_reg)
        draw_ar(d, img_width // 2 - 20, y + 15, value, f_bold)
        y += row_h

    y += 20

    # ===== WEIGHTS =====
    def weight_box(title, value):
        nonlocal y
        h = 90
        d.rectangle((20, y, img_width - 20, y + h), outline="black", width=2)
        draw_ar(d, img_width - 30, y + 10, title, f_bold)
        draw_center_ar(d, img_width // 2, y + 5, value, f_big)
        y += h + 10

    weight_box("القائم", w1_val)
    weight_box("الفارغ", w2_val)
    weight_box("الصافي", ceil(net_w * 100) / 100)

    # ===== FOOTER =====
    d.line((40, y, img_width - 40, y), fill="black", width=2)
    y += 25
    draw_center_ar(d, img_width // 2, y, "Powered by Mostafa Hamdi", f_small)

    img = img.crop((0, 0, img_width, y + 40))
    return img


def print_image_to_printer(img, printer_name="GP-L80180 Series"):
    hprinter = win32print.OpenPrinter(printer_name)
    hdc = win32ui.CreateDC()
    hdc.CreatePrinterDC(printer_name)

    hdc.StartDoc("Thermal Invoice")
    hdc.StartPage()

    if img.mode != "1":
        img = img.convert("1")

    dib = ImageWin.Dib(img)
    dib.draw(hdc.GetHandleOutput(), (0, 0, img.width, img.height))

    hdc.EndPage()
    hdc.EndDoc()
    win32print.ClosePrinter(hprinter)


def print_scale_thermal(entries, invoice_id="INV-001"):
    try:
        img = generate_arabic_invoice(entries, invoice_id)
        print_image_to_printer(img)
        showinfo("تم", "✅ تمت الطباعة بنجاح")
    except Exception as e:
        showerror("خطأ", str(e))
