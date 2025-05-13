import customtkinter as ctk
from PIL import Image, ImageTk


class LogInFrame(ctk.CTkFrame):
    def __init__(self, master=None, switch_to_register=None):
        super().__init__(master)
        self.canvas = ctk.CTkCanvas(self, width=580, height=681, bg="#272757", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.switch_to_register = switch_to_register
        self.container()
        self.input_panel()
        self.log_in_heading()
        self.remember_me()
        self.forgot_password()
        self.account_sign_in()
        
        self.canvas.create_text(265, 560, text="Don't have an account?", font=("Tai Heritage Pro", 15))

        # Create "Register" text
        self.register_text = self.canvas.create_text(365, 560, text="Register", font=("Tai Heritage Pro", 15, "bold"), fill="lightblue")

        # Bind click event to "Register" text
        self.canvas.tag_bind(self.register_text, "<Button-1>", self.to_register)


    def container(self):
        container_pic = Image.open("attendance/public/Rectangle 9.png").resize((580, 681), Image.LANCZOS)
        self.login_container = ImageTk.PhotoImage(container_pic)
        self.canvas.create_image(0, 0, image=self.login_container, anchor="nw")


    def input_panel(self):
        id_logo = Image.open("attendance/public/image 12.png").resize((30, 30), Image.LANCZOS)
        input_panel_pic = Image.open("attendance/public/Rectangle 8.png").resize((520, 75), Image.LANCZOS)
        pass_logo = Image.open("attendance/public/image 13.png").resize((30, 30), Image.LANCZOS)


        '''1st INPUT PANEL'''
        # INPUT PANEL
        self.id_panel = ImageTk.PhotoImage (input_panel_pic) 
        self.canvas.create_image(31, 175, image=self.id_panel, anchor="nw") 
        # THE LITTLE PERSON LOGO 
        self.id_logo = ImageTk.PhotoImage(id_logo)
        self.canvas.create_image(490, 197, image=self.id_logo, anchor="nw") 
        # THE TEXT
        self.id_entry = ctk.CTkEntry(self, font=("Tai Heritage Pro", 18), width=440, height=50, fg_color="#525270", bg_color="#525270", border_width=0, corner_radius=0, placeholder_text="Enter your ID number")
        self.canvas.create_window(50, 190, anchor="nw", window=self.id_entry)
    

        '''2nd INPUT PANEL'''
        # INPUT PANEL
        self.password_panel = ImageTk.PhotoImage(input_panel_pic)
        self.canvas.create_image(31, 285, image=self.password_panel, anchor="nw")
        # THE TEXT
        self.pass_entry = ctk.CTkEntry(self, width=440, height=50, fg_color="#525270", bg_color="#525270", border_width=0, corner_radius=0, placeholder_text="Enter your password", font=("Tai Heritage Pro", 18), show="*")
        self.canvas.create_window(50, 300, anchor="nw", window=self.pass_entry)
        # THE LOGO
        self.pass_logo = ImageTk.PhotoImage(pass_logo)
        self.canvas.create_image(490, 310, image=self.pass_logo, anchor="nw")


    def log_in_heading(self):
        self.canvas.create_text(290, 100, text="LOGIN", font=("Tai Heritage Pro", 70), fill="white")


    def remember_me(self):
        self.check_var = ctk.BooleanVar()
        self.remember = ctk.CTkCheckBox(self, width=0, height=0, variable=self.check_var, command=self.submit_action, border_width=2, corner_radius=0, bg_color="#27274C", font=("Tai Heritage Pro", 15), text=" Remember me", text_color="white", checkmark_color="white")
        self.canvas.create_window(45, 390, anchor="nw", window=self.remember)


    def submit_action(self):
        if self.check_var.get():
            print("remembered, (Need backend and database)")
        else:
            print("forgot, (Need backend and database)")


    def forgot_password(self):
        self.forgot = self.canvas.create_text(415, 391, anchor="nw", text="Forgot password?", font=("Tai Heritage Pro", 15))


    def account_sign_in(self):
        sign_in_img = Image.open("attendance/public/Rectangle 11.png").resize((520, 80), Image.LANCZOS)
        self.sign_ins = ImageTk.PhotoImage(sign_in_img)


        self.canvas.create_image(31, 450, image=self.sign_ins, anchor="nw")
        self.canvas.create_text(31 + 260, 450 + 40, text="Sign In", fill="#E2E2E7", font=("Tai Heritage Pro", 20))


    def to_register(self, event):
            
        if self.switch_to_register:
            self.switch_to_register()
    


if __name__ == "__main__":
    root = ctk.CTk()
    root.geometry("580x681")
    login = LogInFrame(root)
    login.pack()
    root.mainloop()
