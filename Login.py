import customtkinter as ctk
from PIL import Image, ImageTk

class LogInFrame(ctk.CTkFrame):
    def __init__(self, master=None):
        super().__init__(master)
        self.canvas = ctk.CTkCanvas(self, width=580, height=681, bg="#272757", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.container()
        self.input_panel()
        self.log_in_heading()

    def container(self):
        container_pic = Image.open("attendance/public/Rectangle 9.png")
        resized_container = container_pic.resize((580, 681), Image.LANCZOS)
        self.login_container = ImageTk.PhotoImage(resized_container)
        self.canvas.create_image(0, 0, image=self.login_container, anchor="nw")

    def input_panel(self):
        id_logo = Image.open("attendance/public/image 12.png")
        resized_id_logo = id_logo.resize((30, 30), Image.LANCZOS)
        input_panel_pic = Image.open("attendance/public/Rectangle 8.png")
        resized_input_panel = input_panel_pic.resize((520, 75), Image.LANCZOS)


        '''# 1st INPUT PANEL'''
        # INPUT PANEL
        self.id_panel = ImageTk.PhotoImage (resized_input_panel) 
        self.canvas.create_image(31, 160, image=self.id_panel, anchor="nw") 
        # THE LITTLE PERSON LOGO 
        self.id_logo = ImageTk.PhotoImage(resized_id_logo)
        self.canvas.create_image(490, 182, image=self.id_logo, anchor="nw") 
        # THE TEXT
    


        self.password_panel = ImageTk.PhotoImage(resized_input_panel)
        self.canvas.create_image(31, 280, image=self.password_panel, anchor="nw")
        
       


    def log_in_heading(self):
        self.canvas.create_text(290, 100, text="LOGIN", font=("Tai Heritage Pro", 64), fill="white")


if __name__ == "__main__":
    root = ctk.CTk()
    root.geometry("580x681")
    login = LogInFrame(root)
    login.pack()
    root.mainloop()
