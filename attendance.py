# import customtkinter as ctk
# from PIL import ImageTk, Image
# from abc import ABC, abstractmethod

# def center_window(win, width, height):
#         screen_width = win.winfo_screenwidth()
#         screen_height = win.winfo_screenheight()
#         x = (screen_width // 2) - (width // 2)
#         y = (screen_height // 2) - (height // 2)
#         win.geometry(f"{width}x{height}+{x}+{y}") 

# class Window(ABC):
#     def __init__(self):
#         self.root = ctk.CTk()
#         self.root.title("Attendance Tracker")
#         center_window(self.root, 1000, 700)

#     def run(self):
#         self.root.mainloop()

#     @abstractmethod
#     def create_image(self):
#         pass
    
#     @abstractmethod
#     def create_text(self):
#         pass


# class BasicUI(Window):
#     pass

# class LogIn(Window):
#     def __init__(self):
#         super().__init__()

#     def create_image(self):
#         pass

#     def create_text(self):
#         pass

 
# if __name__ == "__main__":
#     app = LogIn()
#     app.run()



