from customtkinter import CTk, set_appearance_mode
from utils.settings_work import get_setting_by_key

def main():
    pro = CTk()

    pro.title("ايمن للموازين")
    pro.geometry("600x500")
    pro.iconbitmap("icon.ico")
    set_appearance_mode("dark")
    if get_setting_by_key("is_security"):
        from ui.auth import Auth
        Auth(pro)
    else:
        from ui.layout import Layout
        Layout(pro)
    pro.mainloop()

if __name__ == "__main__":
    main()
