import customtkinter as ctk
from PIL import ImageTk, Image
from abc import ABC, abstractmethod
from Login import LogInFrame

def center_window(win, width, height):
        screen_width = win.winfo_screenwidth()
        screen_height = win.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        win.geometry(f"{width}x{height}+{x}+{y}") 

class Window(ABC):
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Attendance Tracker")
        center_window(self.root, 1280, 800)
        self.root.configure(fg_color="#272757")
        self.root.resizable(False, False)

    def run(self):
        self.root.mainloop()

class OpeningAnimation(Window):
    pass

class LogIn(Window):
    def __init__(self):
        super().__init__()
        self.login_ui = LogInFrame(self.root)
        self.login_ui.place(rely=0.5, x=930 , anchor="center")

 
if __name__ == "__main__":
    app = LogIn()
    app.run()



