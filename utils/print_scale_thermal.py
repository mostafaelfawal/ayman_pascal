import win32print
import win32ui
from PIL import Image, ImageDraw, ImageFont, ImageWin
import arabic_reshaper
from bidi.algorithm import get_display
from datetime import datetime
from utils.settings_work import get_setting_by_key
from tkinter.messagebox import showinfo

# مسار الخط العربي
FONT_PATH = "assets/fonts/Amiri-Regular.ttf" 

# PNG or BMP
LOGO_PATH = "assets/icon.png"

def generate_arabic_invoice(entries, net_weight, img_width=550):
    """توليد فاتورة عربية احترافية بصورة"""

    # جلب بيانات الشركة
    company_name = get_setting_by_key("company_name") or "Ayman pascal"
    company_phone = get_setting_by_key("company_phone") or "01008454579"
    company_email = get_setting_by_key("company_email") or "ayman_scale@gmail.com"

    # بيانات العميل
    client_name = entries["اسم العميل"].get()
    vehicle_number = entries["رقم السيارة"].get()
    cargo_type = entries["نوع الحمولة"].get()
    governorate = entries["المحافظة"].get()
    w1_time = entries["weight1_time"].get()
    w1_date = entries["weight1_date"].get()
    w1_val = entries["weight1_weight"].get()
    w2_time = entries["weight2_time"].get()
    w2_date = entries["weight2_date"].get()
    w2_val = entries["weight2_weight"].get()
    net_w = net_weight.cget("text")

    now = datetime.now()
    time_str = now.strftime("%d/%m/%Y - %H:%M:%S")

    # إعداد الصورة
    img_height = 1500  # ارتفاع مبدئي، سيتم قصه لاحقاً
    img = Image.new("RGB", (img_width, img_height), "white")
    draw = ImageDraw.Draw(img)
    font_title = ImageFont.truetype(FONT_PATH, 36)
    font_regular = ImageFont.truetype(FONT_PATH, 28)
    font_small = ImageFont.truetype(FONT_PATH, 24)

    y = 10

    # ===== Logo الشركة =====
    try:
        logo = Image.open(LOGO_PATH)
        # تصغير اللوجو إذا كان أكبر من المساحة
        logo.thumbnail((img_width - 40, 150))
        img.paste(logo, ((img_width - logo.width)//2, y))
        y += logo.height + 10
    except Exception:
        pass  # لو مفيش Logo يكمل بدون مشكلة

    # ===== اسم الشركة =====
    company_text = f"{company_name}\nالهاتف: {company_phone}\nالايميل: {company_email}"
    reshaped = arabic_reshaper.reshape(company_text)
    bidi_text = get_display(reshaped)
    for line in bidi_text.split("\n"):
        bbox = draw.textbbox((0, 0), line, font=font_regular)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
        draw.text(((img_width - w)//2, y), line, font=font_regular, fill="black")
        y += h + 2

    y += 10
    draw.line((0, y, img_width, y), fill="black", width=2)
    y += 10

    # ===== بيانات العميل مع جدول border =====
    headers = ["بيانات العميل", "القيمة"]
    data = [
        ["اسم العميل", client_name],
        ["رقم السيارة", vehicle_number],
        ["نوع الحمولة", cargo_type],
        ["المحافظة", governorate],
        ["تاريخ الطباعة", time_str]
    ]

    # رسم الجدول
    row_height = 40
    col1_x = 10
    col2_x = img_width//2 + 10

    for row_index, row in enumerate([headers] + data):
        for col_index, cell in enumerate(row):
            reshaped_cell = arabic_reshaper.reshape(cell)
            bidi_cell = get_display(reshaped_cell)
            font = font_title if row_index == 0 else font_regular
            x = col1_x if col_index == 0 else col2_x
            draw.text((x, y), bidi_cell, font=font, fill="black")
        # رسم الخطوط الأفقية
        draw.line((0, y + row_height, img_width, y + row_height), fill="black", width=1)
        y += row_height
    # رسم الخطوط الرأسية
    draw.line((img_width//2,  y - row_height*(len(data)+1), img_width//2, y), fill="black", width=1)

    y += 10
    draw.line((0, y, img_width, y), fill="black", width=2)
    y += 10

    # ===== بيانات الوزن مع جدول =====
    headers = ["الوصف", "الوزن", "التاريخ", "الوقت"]
    weight_data = [
        ["الوزنة الأولى", w1_val, w1_date, w1_time],
        ["الوزنة الثانية", w2_val, w2_date, w2_time],
        ["", net_w, "", ""]
    ]

    col_positions = [10, 140, 300, 450]

    # رؤوس الجدول
    for idx, header in enumerate(headers):
        reshaped_h = arabic_reshaper.reshape(header)
        bidi_h = get_display(reshaped_h)
        draw.text((col_positions[idx], y), bidi_h, font=font_regular, fill="black")
    y += row_height
    draw.line((0, y, img_width, y), fill="black", width=1)

    # البيانات
    for row in weight_data:
        for idx, cell in enumerate(row):
            reshaped_cell = arabic_reshaper.reshape(str(cell))
            bidi_cell = get_display(reshaped_cell)
            draw.text((col_positions[idx], y), bidi_cell, font=font_regular, fill="black")
        y += row_height
        draw.line((0, y, img_width, y), fill="black", width=1)

    y += 10
    # ===== Footer =====
    footer = "<< برمجة مصطفى حمدي >>"
    reshaped_footer = arabic_reshaper.reshape(footer)
    bidi_footer = get_display(reshaped_footer)
    bbox = draw.textbbox((0, 0), bidi_footer, font=font_small)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    draw.text(((img_width - w)//2, y), bidi_footer, font=font_small, fill="black")
    y += h + 10

    # قص الصورة للمحتوى فقط
    img = img.crop((0, 0, img_width, y + 20))

    return img

def print_image_to_printer(img, printer_name="GP-L80180 Series"):
    """طباعة الصورة للطابعة الحرارية"""
    hprinter = win32print.OpenPrinter(printer_name)
    hdc = win32ui.CreateDC()
    hdc.CreatePrinterDC(printer_name)

    hdc.StartDoc("Arabic Receipt")
    hdc.StartPage()

    dib = ImageWin.Dib(img)
    dib.draw(hdc.GetHandleOutput(), (0, 0, img.width, img.height))

    hdc.EndPage()
    hdc.EndDoc()

    # قص الورق

    win32print.ClosePrinter(hprinter)

def print_scale_thermal(entries, net_weight):
    """بناء وطباعة الفاتورة الاحترافية"""
    img = generate_arabic_invoice(entries, net_weight)
    print_image_to_printer(img)
    showinfo("تم", "تمت طباعة الفاتوره")