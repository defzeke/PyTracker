import customtkinter as ctk
from abc import ABC, abstractmethod
from modules.Login import LogInFrame
from modules.Register import RegisterFrame
from modules.Captcha import CaptchaWidget

def center_window(win, width, height):
        screen_width = win.winfo_screenwidth()
        screen_height = win.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        win.geometry(f"{width}x{height}+{x}+{y}") 

class Window:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("PyTracker")
        center_window(self.root, 1280, 800)
        self.root.configure(fg_color="#272757")
        self.root.resizable(True, True)

    def run(self):
        self.root.mainloop()

class OpeningAnimation(Window):
    pass

class Main(Window):
    def __init__(self):
        super().__init__()
        for col in range(2):            
            self.root.grid_columnconfigure(col, weight=1)

        self.root.grid_columnconfigure(2, weight=0) 
        self.root.grid_rowconfigure(0, weight=1)

        self.login_ui = LogInFrame(self.root, switch_to_register=self.show_register)
        self.login_ui.grid(row=0, column=2, padx=60, pady=20)

        self.register_ui = RegisterFrame(self.root, switch_to_login=self.show_login)
        self.register_ui.grid(row=0, column=2, padx=60, pady=20)
        self.register_ui.lower()

###############################################
    def show_register(self):
        self.login_ui.lower()  
        self.register_ui.lift()  
        self.register_ui.reset_to_role_pick()

    def show_login(self):
        self.register_ui.lower() 
        self.login_ui.lift() 
        self.login_ui.reset_entries() 

    def run(self):
        self.root.mainloop()
###############################################



 
if __name__ == "__main__":
    app = Main()
    app.run()



