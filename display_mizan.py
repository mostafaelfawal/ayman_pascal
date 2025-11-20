from customtkinter import CTk, CTkLabel
import serial

# فتح الاتصال بالسيريال
ser = serial.Serial(
    port='COM1',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

app = CTk()
app.geometry("500x500")

weight_label = CTkLabel(app, text="0.00", font=("Arial", 50, "bold"))
weight_label.pack(expand=True)


def read_weight():
    """قراءة الوزن من الميزان وتحديث الواجهه"""
    try:
        line = ser.readline().decode('utf-8').strip()
        
        # الشكل المتوقع: US, GS, + 42.80kg
        if line:
            parts = line.split(",")  # ['US', ' GS', ' + 42.80kg']
            if len(parts) >= 3:
                weight_str = parts[2].strip()   # '+ 42.80kg'
                weight_str = weight_str.replace("+", "").replace("kg", "").strip()
                try:
                    weight = float(weight_str)
                    weight_label.configure(text=f"{weight:.2f}")
                except ValueError as e:
                    print(e)  # لو فيه أي خطأ في التحويل يتجاهل
    except Exception as e:
        print("Error:", e)

    app.after(200, read_weight)  # تحديث كل 200ms


read_weight()
app.mainloop()
