from customtkinter import CTk, set_appearance_mode
from ui.auth import Auth        

def main():
    pro = CTk()

    pro.title("ايمن للموازين")
    pro.geometry("600x500")
    pro.iconbitmap("icon.ico")
    set_appearance_mode("dark")

    Auth(pro)
    pro.mainloop()

if __name__ == "__main__":
    main()
