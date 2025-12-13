from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import webbrowser
from bidi.algorithm import get_display
import arabic_reshaper
from reportlab.lib.colors import HexColor, black, white
from reportlab.platypus import Table, TableStyle
import os
from utils.settings_work import get_setting_by_key
from tkinter.messagebox import showinfo

def print_scale(entries, net_weight):
    """طباعة وإنشاء PDF للوزنة مع دعم النص العربي بشكل صحيح"""
    client_name = entries["اسم العميل"].get()
    vehicle_number = entries["رقم السيارة"].get()
    cargo_type = entries["نوع الحمولة"].get()
    governorate = entries["المحافظة"].get()
    weight1_time = entries["weight1_time"].get()
    weight1_date = entries["weight1_date"].get()
    weight1_value = entries["weight1_weight"].get()
    weight2_time = entries["weight2_time"].get()
    weight2_date = entries["weight2_date"].get()
    weight2_value = entries["weight2_weight"].get()
    net_weight_text = net_weight.cget("text")
    time = datetime.now().strftime("%d/%m/%Y , %H:%M:%S")
    # =========================================
    # إعداد PDF
    # =========================================
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    pdf_file = f"exports/scale_invoice_{timestamp}.pdf"
    c = canvas.Canvas(pdf_file, pagesize=A4)
    width, height = A4

    # تسجيل الخطوط العربية
    pdfmetrics.registerFont(TTFont('Amiri', 'assets/fonts/Amiri-Regular.ttf'))
    pdfmetrics.registerFont(TTFont('Amiri-Bold', 'assets/fonts/Amiri-Bold.ttf'))

    # ألوان الهوية البصرية الزرقاء
    primary_blue = HexColor("#1a4f8c")
    secondary_blue = HexColor("#4a90e2")
    light_blue = HexColor("#e8f2ff")
    accent_blue = HexColor("#2c6bb0")

    # المارجن
    margin_x = 40
    current_y = height - 50

    def draw_arabic_text(text, x, y, font_name='Amiri', font_size=14, color=black, alignment='center'):
        """دالة محسنة لرسم النصوص العربية"""
        try:
            reshaped_text = arabic_reshaper.reshape(text)
            bidi_text = get_display(reshaped_text)
            c.setFont(font_name, font_size)
            c.setFillColor(color)
            
            if alignment == 'right':
                c.drawRightString(x, y, bidi_text)
            elif alignment == 'center':
                text_width = c.stringWidth(bidi_text, font_name, font_size)
                c.drawString(x - text_width/2, y, bidi_text)
            else:  # left
                c.drawString(x, y, bidi_text)
        except:
            c.setFont(font_name, font_size)
            c.setFillColor(color)
            if alignment == 'center':
                text_width = c.stringWidth(text, font_name, font_size)
                c.drawString(x - text_width/2, y, text)
            else:
                c.drawString(x, y, text)

    # =========================================
    # رأس الصفحة
    # =========================================
    
    # خلفية الرأس
    c.setFillColor(light_blue)
    c.rect(0, height - 120, width, 120, fill=1, stroke=0)
    
    # شريط أزرق في الأعلى
    c.setFillColor(primary_blue)
    c.rect(0, height - 40, width, 40, fill=1, stroke=0)
    
    # جلب معلومات الشركة من الإعدادات (مع قيم افتراضية احتياطية)
    try:
        company_name = get_setting_by_key("company_name") or "أيمن للموازين"
        company_phone = get_setting_by_key("company_phone") or "01008454579"
        company_email = get_setting_by_key("company_email") or "ayman_scale@gmail.com"
    except Exception:
        company_name = "أيمن للموازين"
        company_phone = "01008454579"
        company_email = "ayman_scale@gmail.com"

    # عنوان الشركة في المركز
    draw_arabic_text(company_name, width/2, height-30, 'Amiri-Bold', 24, white, 'center')
    
    # معلومات الاتصال
    current_y = height - 90
    draw_arabic_text(f"شركة {company_name} - موازين إلكترونية دقيقة", 
            width/2, current_y, 'Amiri', 12, primary_blue, 'center')
    
    current_y -= 20
    contact_line = ""
    if company_phone and company_email:
        contact_line = f"تلفون: {company_phone} - بريد إلكتروني: {company_email}"
    elif company_phone:
        contact_line = f"تلفون: {company_phone}"
    elif company_email:
        contact_line = f"بريد إلكتروني: {company_email}"
    draw_arabic_text(contact_line, width/2, current_y, 'Amiri', 10, primary_blue, 'center')
    
    # خط فاصل
    c.setStrokeColor(secondary_blue)
    c.setLineWidth(1)
    current_y -= 20
    c.line(margin_x, current_y, width-margin_x, current_y)
    
    # =========================================
    # بيانات العميل
    # =========================================
    current_y -= 20
    
    # خلفية قسم بيانات العميل
    c.setFillColor(light_blue)
    c.rect(margin_x, current_y-100, width-2*margin_x, 100, fill=1, stroke=0)
    
    # عنوان قسم بيانات العميل
    c.setFillColor(primary_blue)
    c.rect(margin_x, current_y-30, width-2*margin_x, 30, fill=1, stroke=0)
    draw_arabic_text("بيانات العميل", width/2, current_y-20, 
                    'Amiri-Bold', 16, white, 'center')
    
    # بيانات العميل في صفين
    current_y -= 45
    
    # الصف الأول
    draw_arabic_text(f"اسم العميل: {client_name}", margin_x + 20, current_y, 
                    'Amiri', 14, black, 'left')
    draw_arabic_text(f"رقم السيارة: {vehicle_number}", width/2 + 50, current_y, 
                    'Amiri', 14, black, 'left')
    
    # الصف الثاني
    current_y -= 25
    draw_arabic_text(f"نوع الحمولة: {cargo_type}", margin_x + 20, current_y, 
                    'Amiri', 14, black, 'left')
    draw_arabic_text(f"المحافظة: {governorate}", width/2 + 50, current_y, 
                    'Amiri', 14, black, 'left')
    
    # الصف الثالث 
    current_y -= 25
    draw_arabic_text(f"تاريخ الطباعه: {time}", margin_x + 20, current_y, 
                    'Amiri', 14, black, 'left')
    
    # =========================================
    # البيانات الوزنية - التصميم المحسّن
    # =========================================
    current_y -= 50  # تقليل المسافة لجعل الجدول ملاصق للعنوان
    
    # عنوان قسم البيانات الوزنية
    c.setFillColor(primary_blue)
    c.rect(margin_x, current_y-30, width-2*margin_x, 30, fill=1, stroke=0)
    draw_arabic_text("بيانات الوزن", width/2, current_y-20, 
                    'Amiri-Bold', 16, white, 'center')
    
    # جدول البيانات الوزنية - أبعاد مضبوطة
    data = [
        ["", "التاريخ", "الوقت", "الوزن (كجم)"],
        ["الوزنة الأولى", weight1_date, weight1_time, weight1_value],
        ["الوزنة الثانية", weight2_date, weight2_time, weight2_value]
    ]
    
    # تحضير البيانات للجدول
    table_data = []
    for row in data:
        table_row = []
        for cell in row:
            try:
                reshaped = arabic_reshaper.reshape(str(cell))
                bidi_cell = get_display(reshaped)
                table_row.append(bidi_cell)
            except:
                table_row.append(str(cell))
        table_data.append(table_row)
    
    # حساب أبعاد الجدول بدقة ليتناسب مع الصفحة
    table_width = width-2*margin_x
    col_widths = [
        table_width * 0.30,  # اسم الوزنة
        table_width * 0.25,  # التاريخ
        table_width * 0.20,  # الوقت
        table_width * 0.25   # الوزن
    ]
    
    # إنشاء الجدول
    table = Table(table_data, colWidths=col_widths, rowHeights=[25, 25, 25])
    
    # تنسيق الجدول المحسّن
    table.setStyle(TableStyle([
        ('FONT', (0, 0), (-1, -1), 'Amiri', 11),  # حجم خط أصغر
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BACKGROUND', (0, 0), (-1, 0), accent_blue),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 1, primary_blue),
        ('BACKGROUND', (0, 1), (-1, -1), light_blue),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    
    # رسم الجدول مباشرة تحت العنوان
    table.wrapOn(c, table_width, height)
    table_height = 75  # ارتفاع الجدول (3 صفوف × 25)
    table.drawOn(c, margin_x, current_y - 30 - table_height)  # ملاصق للعنوان
    
    # =========================================
    # الوزن الصافي
    # =========================================
    net_weight_y = current_y - table_height - 50  # مسافة مناسبة بعد الجدول
    
    c.setFillColor(secondary_blue)
    c.rect(margin_x, net_weight_y-50, width-2*margin_x, 50, fill=1, stroke=0)
    
    draw_arabic_text(net_weight_text, width/2, net_weight_y-30, 
                    'Amiri-Bold', 18, white, 'center')
    
    # =========================================
    # تذييل الصفحة (Footer)
    # =========================================
    
    # التأكد من وجود مساحة كافية للفوتر
    footer_height = 60
    if net_weight_y - 50 < footer_height + 20:
        # إذا لم تكن هناك مساحة كافية، نضبط موقع الوزن الصافي
        net_weight_y = footer_height + 70
        c.setFillColor(secondary_blue)
        c.rect(margin_x, net_weight_y-50, width-2*margin_x, 50, fill=1, stroke=0)
        draw_arabic_text(net_weight_text, width/2, net_weight_y-30, 
                        'Amiri-Bold', 18, white, 'center')
    
    # خلفية الفوتر
    c.setFillColor(primary_blue)
    c.rect(0, 0, width, footer_height, fill=1, stroke=0)
    
    # نص الفوتر
    draw_arabic_text("Powered By Mostafa Hamdi", width/2, 40, 
                    'Amiri', 12, white, 'center')
    
    footer_year = datetime.now().year
    footer_line = f"للاستفسار: {company_phone} - جميع الحقوق محفوظة © {footer_year}"
    draw_arabic_text(footer_line, width/2, 20, 'Amiri', 10, white, 'center')
    
    # =========================================
    # حفظ وفتح الملف
    # =========================================
    c.save()
    absolute_path = os.path.abspath(pdf_file)
    webbrowser.open_new(f"file:///{absolute_path}")
    showinfo("تم", "تمت عملية الطباعه بنجاح")
