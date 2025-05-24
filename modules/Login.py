import customtkinter as ctk
import pandas as pd
import numpy as np
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

        self.register_text = self.canvas.create_text(365, 560, text="Register", font=("Tai Heritage Pro", 15, "bold"), fill="lightblue")

        self.canvas.tag_bind(self.register_text, "<Button-1>", self.to_register)

        self.login_data = {
            "Control No.": [],
            "name": [],
            "ID_number": [],
            "role": [],
            "password": [],
            "email": []
        }

        try:
            # Load registration CSV
            self.registration_df = pd.read_csv("attendance/database/registration_main.csv")

            # Load login CSV
            self.login_df = pd.read_csv("attendance/database/login_main.csv")

        except FileNotFoundError:
            error_window = ctk.CTkToplevel(self, width=300, height=100)
            ctk.CTkLabel(error_window, text="Error: One or both of the CSV files (registration_main.csv or login_main.csv) not found.", font=("Tai Heritage Pro", 15)).pack(pady=20)
            self.registration_df = pd.DataFrame(columns=["Control No.", "name", "ID_number", "role", "password", "email"])
            self.login_df = pd.DataFrame(columns=["Control No.", "name", "ID_number", "role", "password", "email"])

        except pd.errors.EmptyDataError:
            error_window = ctk.CTkToplevel(self, width=300, height=100)
            ctk.CTkLabel(error_window, text="Error: One or both of the CSV files (registration_main.csv or login_main.csv) are empty.", font=("Tai Heritage Pro", 15)).pack(pady=20)
            self.registration_df = pd.DataFrame(columns=["Control No.", "name", "ID_number", "role", "password", "email"])
            self.login_df = pd.DataFrame(columns=["Control No.", "name", "ID_number", "role", "password", "email"])

        except pd.errors.ParserError:
            error_window = ctk.CTkToplevel(self, width=300, height=100)
            ctk.CTkLabel(error_window, text="Error: Unable to parse one or both of the CSV files (registration_main.csv or login_main.csv).", font=("Tai Heritage Pro", 15)).pack(pady=20)
            self.registration_df = pd.DataFrame(columns=["Control No.", "name", "ID_number", "role", "password", "email"])
            self.login_df = pd.DataFrame(columns=["Control No.", "name", "ID_number", "role", "password", "email"])

        except Exception as e:
            error_window = ctk.CTkToplevel(self, width=300, height=100)
            ctk.CTkLabel(error_window, text=f"An error occurred: {e}", font=("Tai Heritage Pro", 15)).pack(pady=20)
            self.registration_df = pd.DataFrame(columns=["Control No.", "name", "ID_number", "role", "password", "email"])
            self.login_df = pd.DataFrame(columns=["Control No.", "name", "ID_number", "role", "password", "email"])
       
        # Uncomment the following lines if you want to load the login CSV file even if the registration CSV file is not found.
        # This is useful if you want to allow users to log in even if the registration data is not available.
        '''
        Code if Database is proceeding with error, and the user is not able to register, proceed to uncomment this if necessary.
        - Database Manager, Yco
        try:
            # Load login CSV
            self.login_df = pd.read_csv("attendance/database/login_main.csv")
            print("Login CSV loaded successfully.")
            print("Login CSV data:")
            print(self.login_df)
        except FileNotFoundError:
            print("Error: Login CSV file not found.")
            self.login_df = pd.DataFrame(columns=["Control No.", "name", "ID_number", "role", "password", "email"])
        except pd.errors.EmptyDataError:
            print("Error: Login CSV file is empty.")
            self.login_df = pd.DataFrame(columns=["Control No.", "name", "ID_number", "role", "password", "email"])
        except pd.errors.ParserError:
            print("Error: Unable to parse Login CSV file.")
            self.login_df = pd.DataFrame(columns=["Control No.", "name", "ID_number", "role", "password", "email"])
       '''

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


    def reset_entries(self):
        if hasattr(self, "id_entry"):
            self.id_entry.delete(0, 'end')
            self.id_entry.lift()
        if hasattr(self, "pass_entry"):
            self.pass_entry.delete(0, 'end')
            self.pass_entry.lift()
        if hasattr(self, "error_label"):
            self.error_label.configure(text="")
            self.error_label.lift()
        if hasattr(self, "sign_in_button"):
            self.sign_in_button.lift()

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

        self.sign_in_image_id = self.canvas.create_image(31, 450, image=self.sign_ins, anchor="nw")
        self.canvas.tag_bind(self.sign_in_image_id, "<Button-1>", lambda event: self.login())

        self.sign_in_button = ctk.CTkButton(self, text="Sign In", font=("Tai Heritage Pro", 20), fg_color="#686882", bg_color="#686882", command=self.login, hover=False)
        self.canvas.create_window(31 + 260, 450 + 40, window=self.sign_in_button)

        self.error_label = ctk.CTkLabel(self, text="", font=("Tai Heritage Pro", 15), text_color="red", bg_color="#26264B")
        self.canvas.create_window(290, 600, window=self.error_label)  

    def to_register(self, event):
            
        if self.switch_to_register:
            self.switch_to_register()

    def login(self):
        try:
            id_number = self.id_entry.get().strip()
            password = self.pass_entry.get().strip()

            # Clear previous error
            self.error_label.configure(text="")

            # Check for empty fields
            if not id_number or not password:
                self.error_label.configure(text="Please fill in all fields.")
                self.after(3000, lambda: self.error_label.configure(text=""))
                return

            # Check if user exists in login CSV (case-insensitive for role)
            user_exists = self.login_df[
                (self.login_df['ID_number'] == id_number) & (self.login_df['password'] == password)
            ]

            if not user_exists.empty:
                user_role = user_exists['role'].iloc[0].strip().lower()
                if user_role == 'admin':
                    self.error_label.configure(text="")  # Clear error
                    self.proceed_to_admin_page()
                elif user_role == 'student' or user_role == 'teacher':
                    self.error_label.configure(text="")  # Clear error
                    self.proceed_to_user_page()
                else:
                    self.error_label.configure(text="Error: Unknown user role.")
                    self.after(3000, lambda: self.error_label.configure(text=""))
            else:
                # Check if ID exists but password is wrong
                id_exists = self.login_df[self.login_df['ID_number'] == id_number]
                if not id_exists.empty:
                    self.error_label.configure(text="Incorrect password.")
                    self.after(3000, lambda: self.error_label.configure(text=""))
                else:
                    self.error_label.configure(text="Account not found.")
                    self.after(3000, lambda: self.error_label.configure(text=""))

        except Exception as e:
            self.error_label.configure(text=f"An error occurred: {e}")
            self.after(3000, lambda: self.error_label.configure(text=""))

    def proceed_to_admin_page(self):
        # Implement admin page logic here
        print("Proceeding to admin page...")

    def proceed_to_user_page(self):
        # Implement user page logic here
        print("Proceeding to user page...")
    


if __name__ == "__main__":
    root = ctk.CTk()
    root.geometry("580x681")
    login = LogInFrame(root)
    login.pack()
    root.mainloop()
