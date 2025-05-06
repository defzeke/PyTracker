import customtkinter as ctk
from PIL import Image, ImageTk


class Window:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.geometry("700x700")
        self.canvas = ctk.CTkCanvas(self.root, width=700, height=700)
        self.canvas.pack(fill="both", expand=True)
    
    def run(self):
        self.root.mainloop()

class LogIn(Window):
    def __init__(self):
        super().__init__()

    def container(self):
        container_pic = Image.open("Rectangle 9.png")
        resized_container = container_pic.resize((700, 700), Image.LANCZOS)
        self.login_container = ImageTk.PhotoImage(resized_container)
        self.canvas.create_image(0, 0, image=self.login_container, anchor="nw")

    def input_panel(self):
        input_panel_pic = Image.open("Rectangle 8.png")
        resized_input_panel = input_panel_pic.resize((520, 79), Image.LANCZOS)
        self.panels = ImageTk.PhotoImage(resized_input_panel)
        self.canvas.create_image(100, 100, image=self.panels, anchor="nw")



    def log_in_heading(self):
        pass

if __name__ == "__main__":
    app = LogIn()
    app.container()
    app.input_panel()
    app.run()
