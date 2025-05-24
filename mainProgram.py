import customtkinter as ctk
from abc import ABC, abstractmethod
from modules.Login import LogInFrame
from modules.Register import RegisterFrame
from modules.Captcha import CaptchaWidget

def center_window(win, width, height):
        # Center the window on the screen
        screen_width = win.winfo_screenwidth()
        screen_height = win.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        win.geometry(f"{width}x{height}+{x}+{y}") 

class Window:
    def __init__(self):
        # Initialize the main application window
        self.root = ctk.CTk()
        self.root.title("PyTracker")
        center_window(self.root, 1280, 800)
        self.root.configure(fg_color="#272757")
        self.root.resizable(True, True)

    def run(self):
        # Start the Tkinter main loop
        self.root.mainloop()

class OpeningAnimation(Window):
    # Placeholder for any opening animation logic
    pass

class Main(Window):
    def __init__(self):
        super().__init__()
        # Configure grid columns for layout
        for col in range(2):            
            self.root.grid_columnconfigure(col, weight=1)
        self.root.grid_columnconfigure(2, weight=0) 
        self.root.grid_rowconfigure(0, weight=1)

        # Create and place the login UI
        self.login_ui = LogInFrame(self.root, switch_to_register=self.show_register)
        self.login_ui.grid(row=0, column=2, padx=60, pady=20)

        # Create and place the register UI (hidden by default)
        self.register_ui = RegisterFrame(self.root, switch_to_login=self.show_login)
        self.register_ui.grid(row=0, column=2, padx=60, pady=20)
        self.register_ui.lower()

###############################################
    def show_register(self):
        # Switch to the register UI
        self.login_ui.lower()  
        self.register_ui.lift()  
        self.register_ui.reset_to_role_pick()

    def show_login(self):
        # Switch to the login UI
        self.register_ui.lower() 
        self.login_ui.lift() 
        self.login_ui.reset_entries() 

    def run(self):
        # Start the main loop
        self.root.mainloop()
###############################################



 
if __name__ == "__main__":
    app = Main()
    app.run()



