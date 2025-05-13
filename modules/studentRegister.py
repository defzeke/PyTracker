import customtkinter as ctk
from PIL import Image, ImageTk


class RegisterFrame(ctk.CTkFrame):
    def __init__(self, master=None, switch_to_login=None):
        super().__init__(master)
        self.canvas = ctk.CTkCanvas(self, width=580, height=681, bg="#272757", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.switch_to_login = switch_to_login
        self.container()
        self.register_heading()
        
        self.canvas.create_text(265, 560, text="Already have an account?", font=("Tai Heritage Pro", 15))
        self.canvas.create_text(265, 585, text="Not a student?", font=("Tai Heritage Pro", 15))

        self.to_professor = self.canvas.create_text(341, 585, text="Professor", font=("Tai Heritage Pro", 15, "bold"), fill="lightblue")

        self.login_text = self.canvas.create_text(365, 560, text="Log In", font=("Tai Heritage Pro", 15, "bold"), fill="lightblue")
        self.canvas.tag_bind(self.login_text, "<Button-1>", self.to_login)


    def container(self):
        container_pic = Image.open("attendance/public/Rectangle 9.png").resize((580, 681), Image.LANCZOS)
        self.login_container = ImageTk.PhotoImage(container_pic)
        self.canvas.create_image(0, 0, image=self.login_container, anchor="nw")


    def register_heading(self):
        self.canvas.create_text(290, 100, text="REGISTER", font=("Tai Heritage Pro", 70), fill="white")


    def to_login(self, event):
        if self.switch_to_login:
            self.switch_to_login()

    def name_input_panels(self):
        pass
    

if __name__ == "__main__":
    root = ctk.CTk()
    root.geometry("580x681")
    login = RegisterFrame(root)
    login.pack()
    root.mainloop()
