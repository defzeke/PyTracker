import customtkinter as ctk
import pandas as pd
import numpy as np
import threading
from PIL import Image, ImageTk
from .Captcha import CaptchaWidget
from .OTP import generate_otp, send_otp_email

class RegisterFrame(ctk.CTkFrame):
    def __init__(self, master=None, switch_to_login=None):
        super().__init__(master)

        # Create canvas for the main registration UI
        self.canvas = ctk.CTkCanvas(self, width=580, height=681, bg="#272757", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        # Callback to switch to login frame
        self.switch_to_login = switch_to_login

        # Build the registration UI
        self.container()
        self.register_heading()
        self.role_pick()
        
        # Text asking if user already has account
        self.canvas.create_text(263, 560, text="Already have an account?", font=("Tai Heritage Pro", 15))
        
        # Clickable 'Log In' text
        self.login_text = self.canvas.create_text(365, 560, text="Log In", font=("Tai Heritage Pro", 15, "bold"), fill="lightblue")
        self.canvas.tag_bind(self.login_text, "<Button-1>", self.to_login)

        # Continue button for advancing stages
        self.continue_text_button = self.canvas.create_text(460, 480, text="Continue -->", font=("Tai Heritage Pro", 15, "bold"), fill="white")
        self.canvas.tag_bind(self.continue_text_button, "<Button-1>", self.continue_register)
        self.continue_enabled = False 

        # Initialize registration data
        self.registration_data = {
            "Control No.": "",
            "temp_ID": "",
            "name": "",
            "email": "",
            "role": "",
            "password": "",
            "status": "Pending"
        }
        try:
            # Load registration CSV
            self.registration_df = pd.read_csv("attendance/database/registration_main.csv")

            # Load login CSV
            self.login_df = pd.read_csv("attendance/database/login_main.csv")

        # Error Handsling
        # If CSV files are not found, create empty DataFrames with the same columns
        # and show error message
        except FileNotFoundError:
            ctk.CTkToplevel(self, text="Error", width=300, height=100)
            ctk.CTkLabel(self, text="Error: One or both of the CSV files (registration_main.csv or login_main.csv) not found.", font=("Tai Heritage Pro", 15)).pack(pady=20)
            self.registration_df = pd.DataFrame(columns=["Control No.", "name", "ID_number", "role", "password", "email"])
            self.login_df = pd.DataFrame(columns=["Control No.", "name", "ID_number", "role", "password", "email"])

        except pd.errors.EmptyDataError:
            ctk.CTkToplevel(self, text="Error", width=300, height=100)
            ctk.CTkLabel(self, text="Error: One or both of the CSV files (registration_main.csv or login_main.csv) are empty.", font=("Tai Heritage Pro", 15)).pack(pady=20)
            self.registration_df = pd.DataFrame(columns=["Control No.", "name", "ID_number", "role", "password", "email"])
            self.login_df = pd.DataFrame(columns=["Control No.", "name", "ID_number", "role", "password", "email"])

        except pd.errors.ParserError:
            ctk.CTkToplevel(self, text="Error", width=300, height=100)
            ctk.CTkLabel(self, text="Error: Unable to parse one or both of the CSV files (registration_main.csv or login_main.csv).", font=("Tai Heritage Pro", 15)).pack(pady=20)
            self.registration_df = pd.DataFrame(columns=["Control No.", "name", "ID_number", "role", "password", "email"])
            self.login_df = pd.DataFrame(columns=["Control No.", "name", "ID_number", "role", "password", "email"])

        except Exception as e:
            ctk.CTkToplevel(self, text="Error", width=300, height=100)
            ctk.CTkLabel(self, text=f"An error occurred: {e}", font=("Tai Heritage Pro", 15)).pack(pady=20)
            self.registration_df = pd.DataFrame(columns=["Control No.", "name", "ID_number", "role", "password", "email"])
            self.login_df = pd.DataFrame(columns=["Control No.", "name", "ID_number", "role", "password", "email"])

            # Uncomment the following lines if you want to proceed with registration even if the CSV files are not found    
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
        # Load and display background container image
        container_pic = Image.open("attendance/public/Rectangle 9.png").resize((580, 681), Image.LANCZOS)
        self.login_container = ImageTk.PhotoImage(container_pic)
        self.canvas.create_image(0, 0, image=self.login_container, anchor="nw")


    def register_heading(self):
        # Display large REGISTER heading text
        self.register_heading_id = self.canvas.create_text(290, 100, text="REGISTER", font=("Tai Heritage Pro", 70), fill="white")


    def role_pick(self):
        self.stage = "role"     # Current stage of form

        # Load all panel styles (normal, hover, selected)
        choice_panel_pic = Image.open("attendance/public/Rectangle 8.png").resize((520, 90), Image.LANCZOS)
        hover_panel_pic = Image.open("attendance/public/Rectangle 12.png").resize((520, 90), Image.LANCZOS)
        pick_panel_pic = Image.open("attendance/public/Rectangle 405.png").resize((520, 90), Image.LANCZOS)

        self.student_img_normal = ImageTk.PhotoImage(choice_panel_pic)
        self.student_img_hover = ImageTk.PhotoImage(hover_panel_pic)
        self.student_img_pick = ImageTk.PhotoImage(pick_panel_pic)

        self.prof_img_normal = ImageTk.PhotoImage(choice_panel_pic)
        self.prof_img_hover = ImageTk.PhotoImage(hover_panel_pic)
        self.prof_img_pick = ImageTk.PhotoImage(pick_panel_pic)

        self.selected_role = None   # Track which role was picked

        # Student panel with hover/click actions
        self.student_panel_id = self.canvas.create_image(31, 220, image=self.student_img_normal, anchor="nw")
        self.student_text_id = self.canvas.create_text(290, 265, text="Student", font=("Tai Heritage Pro", 20), fill="white")
        self.student_rect = self.canvas.create_rectangle(31, 220, 551, 300, outline="", fill="", tags="student")

        # Professor panel with hover/click actions
        self.prof_panel_id = self.canvas.create_image(31, 340, image=self.prof_img_normal, anchor="nw")
        self.prof_text_id = self.canvas.create_text(290, 385, text="Professor", font=("Tai Heritage Pro", 20), fill="white")
        self.prof_rect = self.canvas.create_rectangle(31, 340, 551, 420, outline="", fill="", tags="prof")

        # Bind mouse hover and click events
        self.canvas.tag_bind("student", "<Enter>", lambda e: self.hover_role("student"))
        self.canvas.tag_bind("student", "<Leave>", lambda e: self.leave_role("student"))
        self.canvas.tag_bind("prof", "<Enter>", lambda e: self.hover_role("prof"))
        self.canvas.tag_bind("prof", "<Leave>", lambda e: self.leave_role("prof"))
        self.canvas.tag_bind("student", "<Button-1>", lambda e: self.select_role("student"))
        self.canvas.tag_bind("prof", "<Button-1>", lambda e: self.select_role("prof"))



##############################################################################################
    def reset_to_role_pick(self):
        # Reset the registration form to the role selection stage

        # Hide name input widgets if present
        if hasattr(self, "name_input_items"):
            for item in self.name_input_items:
                self.canvas.itemconfigure(item, state='hidden')
            self.canvas.itemconfigure(self.win1, state='hidden')
            self.canvas.itemconfigure(self.win2, state='hidden')
            self.canvas.itemconfigure(self.win3, state='hidden')

        # Hide credentials input widgets if present
        if hasattr(self, "cred_input_items"):
            for item in self.cred_input_items:
                self.canvas.itemconfigure(item, state='hidden')
            self.canvas.itemconfigure(self.email_win, state='hidden')
            self.canvas.itemconfigure(self.password_win, state='hidden')
            self.canvas.itemconfigure(self.confirm_password_win, state='hidden')

        # Hide captcha widget if present
        if hasattr(self, "captcha_widget"):
            self.captcha_widget.place_forget()

        # Reset continue button appearance and state
        if hasattr(self, "continue_text_button"):
            self.canvas.itemconfigure(self.continue_text_button, fill="white", state='normal')

        # Hide and reset back button
        if hasattr(self, "back_text_button"):
            self.canvas.coords(self.back_text_button, 120, 480)
            self.canvas.itemconfigure(self.back_text_button, state='hidden')
            self.canvas.tag_unbind(self.back_text_button, "<Button-1>")

        # Hide OTP/verification widgets 
        if hasattr(self, "otp_entry"):
            self.otp_entry.place_forget()
        if hasattr(self, "sign_up_image_id"):
            self.canvas.itemconfigure(self.sign_up_image_id, state='hidden')
        if hasattr(self, "signup"):
            self.canvas.itemconfigure(self.signup, state='hidden')
        if hasattr(self, "email_verify_panel"):
            self.canvas.itemconfigure(self.email_verify_panel, state='hidden')

        # Clear registration entries
        if hasattr(self, "first_name_entry"):
            self.first_name_entry.delete(0, 'end')
        if hasattr(self, "middle_name_entry"):
            self.middle_name_entry.delete(0, 'end')
        if hasattr(self, "last_name_entry"):
            self.last_name_entry.delete(0, 'end')
        if hasattr(self, "email_entry"):
            self.email_entry.delete(0, 'end')
        if hasattr(self, "password_entry"):
            self.password_entry.delete(0, 'end')
        if hasattr(self, "confirm_password_entry"):
            self.confirm_password_entry.delete(0, 'end')

        # Restore role pick panels/texts to normal (non-hover, non-selected) state
        if hasattr(self, "student_panel_id"):
            self.canvas.itemconfig(self.student_panel_id, image=self.student_img_normal)
        if hasattr(self, "student_text_id"):
            self.canvas.itemconfig(self.student_text_id, fill="white")
        if hasattr(self, "prof_panel_id"):
            self.canvas.itemconfig(self.prof_panel_id, image=self.prof_img_normal)
        if hasattr(self, "prof_text_id"):
            self.canvas.itemconfig(self.prof_text_id, fill="white")

        # Show role pick panels/texts
        self.canvas.itemconfigure(self.student_panel_id, state='normal')
        self.canvas.itemconfigure(self.student_text_id, state='normal')
        self.canvas.itemconfigure(self.prof_panel_id, state='normal')
        self.canvas.itemconfigure(self.prof_text_id, state='normal')

        # Deselect role and reset stage
        self.selected_role = None
        self.stage = "role"
        self.continue_enabled = False

    def capitalize_name_entry(self, entry):
        value = entry.get()
        # Capitalize first letter and every letter after a space
        capitalized = ' '.join(word.capitalize() for word in value.split(' '))
        if value != capitalized:
            entry.delete(0, 'end')
            entry.insert(0, capitalized)
    
    def to_login(self, event):
        # Switch to login frame when 'Log In' text is clicked
        if self.switch_to_login:
            self.switch_to_login()
    
    def hover_role(self, role):
        # Show hover image if role isn't selected
        if self.selected_role == role:
            return

        if role == "student":
            self.canvas.itemconfig(self.student_panel_id, image=self.student_img_hover)
        elif role == "prof":
            self.canvas.itemconfig(self.prof_panel_id, image=self.prof_img_hover)

    def leave_role(self, role):
        # Revert to normal image on hover leave
        if self.selected_role == role:
            return

        if role == "student":
            self.canvas.itemconfig(self.student_panel_id, image=self.student_img_normal)
        elif role == "prof":
            self.canvas.itemconfig(self.prof_panel_id, image=self.prof_img_normal)

    def select_role(self, role):
        # Set role selection visuals and mark role as selected
        self.selected_role = role

        # Highlight the selected role and reset the other
        if role == "student":
            self.canvas.itemconfig(self.student_panel_id, image=self.student_img_pick)
            self.canvas.itemconfig(self.student_text_id, fill="black")
            self.canvas.itemconfig(self.prof_panel_id, image=self.prof_img_normal)
            self.canvas.itemconfig(self.prof_text_id, fill="white")
        elif role == "prof":
            self.canvas.itemconfig(self.prof_panel_id, image=self.prof_img_pick)
            self.canvas.itemconfig(self.prof_text_id, fill="black")
            self.canvas.itemconfig(self.student_panel_id, image=self.student_img_normal)
            self.canvas.itemconfig(self.student_text_id, fill="white")

        # Enable the continue button when a role is selected
        self.canvas.itemconfig(self.continue_text_button, fill="lightblue")
        self.continue_enabled = True

    def show_error(self, message, persist=False):
        # Display an error message on the registration form
        if hasattr(self, "error_text"):
            self.canvas.itemconfig(self.error_text, text=message, state="normal")
        else:
            self.error_text = self.canvas.create_text(
                290, 590,
                text=message,
                font=("Tai Heritage Pro", 15),
                fill="red"
            )
        # Always auto-hide the error after 10 seconds
        self.after(10000, lambda: self.canvas.itemconfig(self.error_text, state="hidden"))

    def is_strong_password(self, password):
        # Check password strength and return a list of missing requirements
        import re
        errors = []
        if len(password) < 8:
            errors.append("at least 8 characters")
        if not re.search(r"[A-Z]", password):
            errors.append("an uppercase letter")
        if not re.search(r"[a-z]", password):
            errors.append("a lowercase letter")
        if not re.search(r"\d", password):
            errors.append("a number")
        if not re.search(r"[!\"#$%&'()*+,\-./:;<=>?@[\\\]^_`{|}~]", password):
            errors.append("a special character")
        return errors

    def continue_register(self, event=None):
        # Advance to the next stage of registration form based on current stage

        # If on role selection stage and a role is selected, hide role widgets and show name input
        if self.stage == "role" and self.selected_role:
            self.canvas.itemconfigure(self.student_panel_id, state='hidden')
            self.canvas.itemconfigure(self.student_text_id, state='hidden')
            self.canvas.itemconfigure(self.prof_panel_id, state='hidden')
            self.canvas.itemconfigure(self.prof_text_id, state='hidden')

            self.name_input_panels()

        # If on name input stage, validate names and proceed to credentials input
        elif self.stage == "name":
            first = self.first_name_entry.get().strip()
            middle = self.middle_name_entry.get().strip()
            last = self.last_name_entry.get().strip()
            if not first or not last:
                self.show_error("You must fill up every sections.")
            else:
                if middle:
                    self.registration_data["name"] = f"{first} {middle} {last}"
                else:
                    self.registration_data["name"] = f"{first} {last}"
                self.show_credentials_input()

        # If on credentials stage, validate CAPTCHA, email, and password, then proceed to OTP
        elif self.stage == "credentials":
            if hasattr(self, "captcha_widget") and not self.captcha_widget.verified:
                self.show_error("Please verify the CAPTCHA before continuing.")
                return

            email = self.email_entry.get().strip()
            password = self.password_entry.get().strip()
            confirm = self.confirm_password_entry.get().strip()

            # Check for empty fields
            if not email or not password or not confirm:
                self.show_error("You must fill up every sections.")
            # Check if passwords match
            elif password != confirm:
                self.show_error("Passwords do not match.")
            else:
                # Check password strength
                pw_errors = self.is_strong_password(password)
                if pw_errors:
                    self.show_error("Password must contain " + ", ".join(pw_errors) + ".")
                    return
                # Email domain validation based on role
                if self.selected_role == "student":
                    if not email.endswith("@iskolarngbayan.pup.edu.ph"):
                        self.show_error("Student email must end with @iskolarngbayan.pup.edu.ph")
                        return
                elif self.selected_role == "prof":
                    if not email.endswith("@pup.edu.ph"):
                        self.show_error("Professor email must end with @pup.edu.ph")
                        return
                # Proceed to OTP verification stage
                self.show_email_verify()

                # Save registration data for later use
                self.registration_data["email"] = email
                self.registration_data["password"] = password
                self.registration_data["role"] = self.selected_role

                # Generate control number
                if self.registration_df.empty:
                    control_no = 1
                else:
                    control_no = self.registration_df['Control No.'].max() + 1
                self.registration_data["Control No."] = control_no

                # Generate temp_ID
                if self.registration_df.empty:
                    temp_id = 1
                else:
                    temp_id = self.registration_df['temp_ID'].max() + 1
                self.registration_data["temp_ID"] = temp_id

                # Save registration data to CSV
                new_row = pd.DataFrame([self.registration_data])
                self.registration_df = pd.concat([self.registration_df, new_row], ignore_index=True)
                self.registration_df.to_csv("attendance/database/registration_main.csv", index=False)

                # Check if user already exists in login_main.csv
                existing_user = self.login_df[(self.login_df['email'] == email) & (self.login_df['password'] == password)]
                if not existing_user.empty:
                    self.show_error("User      already exists. Please try again.")
                else:
                    # Generate control number for login
                    if self.login_df.empty:
                        login_control_no = 1
                    else:
                        login_control_no = self.login_df['Control No.'].max() + 1

                    # Generate temp_ID for login
                    if self.login_df.empty:
                        login_temp_id = 1
                    else:
                        login_temp_id = self.login_df['ID_number'].max() + 1

                    # Add registration data to login CSV
                    login_data = {
                        "Control No.": login_control_no,
                        "name": self.registration_data["name"],
                        "ID_number": login_temp_id,
                        "role": self.registration_data["role"],
                        "password": self.registration_data["password"],
                        "email": self.registration_data["email"]
                    }
                    new_login_row = pd.DataFrame([login_data])
                    self.login_df = pd.concat([self.login_df, new_login_row], ignore_index=True)
                    self.login_df.to_csv("attendance/database/login_main.csv", index=False)

                    # Switch to login frame
                    if self.switch_to_login:
                        self.switch_to_login()

    def back_to_role(self, event=None):
        # Go back from name input or credentials input to role selection

        # Hide name input items if present
        if hasattr(self, "name_input_items"):
            for item in self.name_input_items:
                self.canvas.itemconfigure(item, state='hidden')

        # Remove name entry widgets if present
        if hasattr(self, "win1"):
            self.canvas.delete(self.win1)
        if hasattr(self, "win2"):
            self.canvas.delete(self.win2)
        if hasattr(self, "win3"):
            self.canvas.delete(self.win3)
        if hasattr(self, "first_name_entry"):
            self.first_name_entry.destroy()
        if hasattr(self, "middle_name_entry"):
            self.middle_name_entry.destroy()
        if hasattr(self, "last_name_entry"):
            self.last_name_entry.destroy()

        # Remove credentials entry widgets if present
        if hasattr(self, "email_entry"):
            self.email_entry.delete(0, 'end')
        if hasattr(self, "password_entry"):
            self.password_entry.delete(0, 'end')
        if hasattr(self, "confirm_password_entry"):
            self.confirm_password_entry.delete(0, 'end')

        # Hide back button if present
        if hasattr(self, "back_text_button"):
            self.canvas.itemconfigure(self.back_text_button, state='hidden')

        # Show role selection panels/texts
        self.canvas.itemconfigure(self.student_panel_id, state='normal')
        self.canvas.itemconfigure(self.student_text_id, state='normal')
        self.canvas.itemconfigure(self.prof_panel_id, state='normal')
        self.canvas.itemconfigure(self.prof_text_id, state='normal')

        # Set stage back to role selection
        self.stage = "role"

    def back_to_name(self, event=None):
        # Go back from credentials input to name input
        self.stage = "name"

        # Hide credentials input widgets if present
        if hasattr(self, "cred_input_items"):
            for item in self.cred_input_items:
                self.canvas.itemconfigure(item, state='hidden')
            self.canvas.itemconfigure(self.email_win, state='hidden')
            self.canvas.itemconfigure(self.password_win, state='hidden')
            self.canvas.itemconfigure(self.confirm_password_win, state='hidden')

            # Destroy captcha widget if present
            if hasattr(self, "captcha_widget"):
                self.captcha_widget.destroy()
                del self.captcha_widget

        # Show name input widgets if present
        if hasattr(self, "name_input_items"):
            for item in self.name_input_items:
                self.canvas.itemconfigure(item, state='normal')
            self.canvas.itemconfigure(self.win1, state='normal')
            self.canvas.itemconfigure(self.win2, state='normal')
            self.canvas.itemconfigure(self.win3, state='normal')

            # Bring widgets to the front
            self.canvas.lift(self.win1)
            self.canvas.lift(self.win2)
            self.canvas.lift(self.win3)

            self.first_name_entry.lift()
            self.middle_name_entry.lift()
            self.last_name_entry.lift()

            self.first_name_entry.update_idletasks()
            self.middle_name_entry.update_idletasks()
            self.last_name_entry.update_idletasks()

        # Re-bind back button to go back to role selection
        self.canvas.tag_unbind(self.back_text_button, "<Button-1>")
        self.canvas.tag_bind(self.back_text_button, "<Button-1>", self.back_to_role)

    def back_to_credentials(self, event=None):
        # Go back from OTP/email verification to credentials input
        self.stage = "credentials"

        # Hide email verification widgets if you have any (add them to a list if needed)
        if hasattr(self, "otp_entry"):
            self.otp_entry.place_forget()
        if hasattr(self, "sign_up_image_id"):
            self.canvas.itemconfigure(self.sign_up_image_id, state='hidden')
        if hasattr(self, "signup"):
            self.canvas.itemconfigure(self.signup, state='hidden')
        if hasattr(self, "email_verify_panel"):
            self.canvas.itemconfigure(self.email_verify_panel, state='hidden')
        if hasattr(self, "register_heading_id"):
            self.canvas.itemconfigure(self.register_heading_id, state='normal')

        # Show credentials input widgets
        if hasattr(self, "cred_input_items"):
            for item in self.cred_input_items:
                self.canvas.itemconfigure(item, state='normal')
            self.canvas.itemconfigure(self.email_win, state='normal')
            self.canvas.itemconfigure(self.password_win, state='normal')
            self.canvas.itemconfigure(self.confirm_password_win, state='normal')

        # Always recreate captcha when returning from OTP 
        if hasattr(self, "captcha_widget"):
            self.captcha_widget.destroy()
            del self.captcha_widget
        self.captcha_widget = CaptchaWidget(self)
        self.captcha_widget.place(x=140, y=370)

        # Hide name input widgets
        if hasattr(self, "name_input_items"):
            for item in self.name_input_items:
                self.canvas.itemconfigure(item, state='hidden')
            self.canvas.itemconfigure(self.win1, state='hidden')
            self.canvas.itemconfigure(self.win2, state='hidden')
            self.canvas.itemconfigure(self.win3, state='hidden')

        # Bring credentials widgets to the front
        self.canvas.lift(self.email_win)
        self.canvas.lift(self.password_win)
        self.canvas.lift(self.confirm_password_win)
        self.email_entry.lift()
        self.password_entry.lift()
        self.confirm_password_entry.lift()
        self.email_entry.update_idletasks()
        self.password_entry.update_idletasks()
        self.confirm_password_entry.update_idletasks()

        # Show continue button
        self.canvas.itemconfigure(self.continue_text_button, state='normal')

        # Move the back button back to its original position (e.g., y=480)
        self.canvas.coords(self.back_text_button, 120, 480)
        self.canvas.itemconfigure(self.back_text_button, state='normal')
        self.canvas.tag_unbind(self.back_text_button, "<Button-1>")
        self.canvas.tag_bind(self.back_text_button, "<Button-1>", self.back_to_name)

        # Bind back button to go back to name input
        self.canvas.tag_unbind(self.back_text_button, "<Button-1>")
        self.canvas.tag_bind(self.back_text_button, "<Button-1>", self.back_to_name)

    def captcha_verified(self):
        # Enable the continue button when captcha is verified
        self.canvas.itemconfigure(self.continue_text_button, fill="lightblue", state='normal')
        self.continue_enabled = True

##############################################################################################


    def name_input_panels(self):
        # Show name entry fields
        self.stage = "name"
        self.name_input_items = []

        # Load input panel images for each name field
        input_panel_pic = Image.open("attendance/public/Rectangle 8.png").resize((520, 75), Image.LANCZOS)
        self.first_name_panel = ImageTk.PhotoImage(input_panel_pic)
        self.middle_name_panel = ImageTk.PhotoImage(input_panel_pic)
        self.last_name_panel = ImageTk.PhotoImage(input_panel_pic)

        # First Name Entry
        panel1 = self.canvas.create_image(31, 175, image=self.first_name_panel, anchor="nw")
        self.first_name_entry = ctk.CTkEntry(self, font=("Tai Heritage Pro", 18), width=440, height=50,
                                            fg_color="#525270", bg_color="#525270", border_width=0, corner_radius=0,
                                            placeholder_text="First Name")
        self.win1 = self.canvas.create_window(50, 190, anchor="nw", window=self.first_name_entry)
        self.first_name_entry.bind("<KeyRelease>", lambda e: self.capitalize_name_entry(self.first_name_entry))


        # Middle Name Entry
        panel2 = self.canvas.create_image(31, 275, image=self.middle_name_panel, anchor="nw")
        self.middle_name_entry = ctk.CTkEntry(self, font=("Tai Heritage Pro", 18), width=440, height=50,
                                            fg_color="#525270", bg_color="#525270", border_width=0, corner_radius=0,
                                            placeholder_text="Middle Name")
        self.win2 = self.canvas.create_window(50, 290, anchor="nw", window=self.middle_name_entry)
        self.middle_name_entry.bind("<KeyRelease>", lambda e: self.capitalize_name_entry(self.middle_name_entry))


        # Last Name Entry
        panel3 = self.canvas.create_image(31, 375, image=self.last_name_panel, anchor="nw")
        self.last_name_entry = ctk.CTkEntry(self, font=("Tai Heritage Pro", 18), width=440, height=50,
                                            fg_color="#525270", bg_color="#525270", border_width=0, corner_radius=0,
                                            placeholder_text="Last Name")
        self.win3 = self.canvas.create_window(50, 390, anchor="nw", window=self.last_name_entry)
        self.last_name_entry.bind("<KeyRelease>", lambda e: self.capitalize_name_entry(self.last_name_entry))

        # Store all name input widgets for easy hiding/showing
        self.name_input_items.extend([panel1, self.win1, panel2, self.win2, panel3, self.win3])

        self.canvas.itemconfigure(self.continue_text_button, state='normal')

        # Add or show back button
        if hasattr(self, "back_text_button"):
            self.canvas.coords(self.back_text_button, 120, 480)  # Original position
            self.canvas.itemconfigure(self.back_text_button, state='normal')
            self.canvas.tag_unbind(self.back_text_button, "<Button-1>")
            self.canvas.tag_bind(self.back_text_button, "<Button-1>", self.back_to_role)
        else:
            self.back_text_button = self.canvas.create_text(120, 480, text="<-- Back", font=("Tai Heritage Pro", 15, "bold"), fill="lightblue")
            self.canvas.tag_bind(self.back_text_button, "<Button-1>", self.back_to_role)

    

    def show_credentials_input(self):
        # Show email, password, and confirm password entry fields, and CAPTCHA
        self.stage = "credentials"

        # Remove old CAPTCHA if present, then add new one
        if hasattr(self, "captcha_widget"):
            self.captcha_widget.destroy()
            del self.captcha_widget
        self.captcha_widget = CaptchaWidget(self)
        self.captcha_widget.place(x=140, y=370)

        # Hide name inputs
        if hasattr(self, "name_input_items"):
            for item in self.name_input_items:
                self.canvas.itemconfigure(item, state='hidden')
            self.canvas.itemconfigure(self.win1, state='hidden')
            self.canvas.itemconfigure(self.win2, state='hidden')
            self.canvas.itemconfigure(self.win3, state='hidden')

        # Create or show credentials UI
        if not hasattr(self, "cred_input_items"):
            self.cred_input_items = []

            panel_pic = Image.open("attendance/public/Rectangle 8.png").resize((520, 75), Image.LANCZOS)
            panel_pic2 = Image.open("attendance/public/Rectangle 406.png").resize((245, 75), Image.LANCZOS)
            self.email_panel = ImageTk.PhotoImage(panel_pic)
            self.password_panel = ImageTk.PhotoImage(panel_pic2)
            self.confirm_panel = ImageTk.PhotoImage(panel_pic2)

            # Email Entry
            panel1 = self.canvas.create_image(31, 175, image=self.email_panel, anchor="nw")
            self.email_entry = ctk.CTkEntry(
                self, font=("Tai Heritage Pro", 18), width=440, height=50,
                fg_color="#525270", bg_color="#525270", border_width=0, corner_radius=0,
                placeholder_text=(
                    "youremail@iskolarngbayan.pup.edu.ph" 
                    if self.selected_role == "student" 
                    else "youremail@pup.edu.ph"
                )
            )
            self.email_win = self.canvas.create_window(50, 190, anchor="nw", window=self.email_entry)


            # Password Entry
            panel2 = self.canvas.create_image(31, 275, image=self.password_panel, anchor="nw")
            self.password_entry = ctk.CTkEntry(self, font=("Tai Heritage Pro", 18), width=210, height=50,
                                            fg_color="#525270", bg_color="#525270", border_width=0, corner_radius=0,
                                            placeholder_text="Password", show="*")
            self.password_win = self.canvas.create_window(50, 290, anchor="nw", window=self.password_entry)


            # Confirm Password Entry
            panel3 = self.canvas.create_image(310, 275, image=self.confirm_panel, anchor="nw")
            self.confirm_password_entry = ctk.CTkEntry(self, font=("Tai Heritage Pro", 18), width=210, height=50,
                                            fg_color="#525270", bg_color="#525270", border_width=0, corner_radius=0,
                                            placeholder_text="Confirm Password", show="*")
            self.confirm_password_win = self.canvas.create_window(325, 290, anchor="nw", window=self.confirm_password_entry)

            self.cred_input_items.extend([panel1, panel2, panel3])



        else:
            # Show existing widgets again
            for item in self.cred_input_items:
                self.canvas.itemconfigure(item, state='normal')
            self.canvas.itemconfigure(self.email_win, state='normal')
            self.canvas.itemconfigure(self.password_win, state='normal')
            self.canvas.itemconfigure(self.confirm_password_win, state='normal')  

            # Adjust email placeholder based on role
            self.email_entry.configure(
                placeholder_text=(
                    "youremail@iskolarngbayan.pup.edu.ph"
                    if self.selected_role == "student"
                    else "youremail@pup.edu.ph"
                )
            )

        # Bring entries to front
        self.canvas.lift(self.email_win)
        self.canvas.lift(self.password_win)
        self.canvas.lift(self.confirm_password_win)  
        self.email_entry.lift()
        self.password_entry.lift()
        self.confirm_password_entry.lift() 
        self.email_entry.update_idletasks()
        self.password_entry.update_idletasks()
        self.confirm_password_entry.update_idletasks()  

        # Bind back button to return to name input
        self.canvas.itemconfigure(self.back_text_button, state='normal')
        self.canvas.tag_unbind(self.back_text_button, "<Button-1>")
        self.canvas.tag_bind(self.back_text_button, "<Button-1>", self.back_to_name)

    
    def show_email_verify(self):
        # Show OTP verification UI and send OTP to the entered email
        self.stage = "email_verify"

        email = self.email_entry.get().strip()
        otp = generate_otp()
        self.generated_otp = otp

        # Send OTP in a separate thread to avoid freezing the UI
        def send_otp_thread():
            if send_otp_email(email, otp):
                print("OTP sent successfully.")
            else:
                self.after(0, lambda: self.show_error("Failed to send OTP. Please try again later."))

        threading.Thread(target=send_otp_thread, daemon=True).start()


        # Hide name input widgets
        if hasattr(self, "name_input_items"):
            for item in self.name_input_items:
                self.canvas.itemconfigure(item, state='hidden')
            self.canvas.itemconfigure(self.win1, state='hidden')
            self.canvas.itemconfigure(self.win2, state='hidden')
            self.canvas.itemconfigure(self.win3, state='hidden')
        # Hide credentials input widgets
        if hasattr(self, "cred_input_items"):
            for item in self.cred_input_items:
                self.canvas.itemconfigure(item, state='hidden')
            self.canvas.itemconfigure(self.email_win, state='hidden')
            self.canvas.itemconfigure(self.password_win, state='hidden')
            self.canvas.itemconfigure(self.confirm_password_win, state='hidden')
        # Hide CAPTCHA if present
        if hasattr(self, "captcha_widget"):
            self.captcha_widget.destroy()
            del self.captcha_widget

        # Hide continue button and move/show back button for OTP stage
        self.canvas.itemconfigure(self.continue_text_button, state='hidden')
        self.canvas.coords(self.back_text_button, 80, 435)
        self.canvas.itemconfigure(self.back_text_button, state='normal')
        self.canvas.tag_unbind(self.back_text_button, "<Button-1>")
        self.canvas.tag_bind(self.back_text_button, "<Button-1>", self.back_to_credentials)

        # Create OTP entry fields (6 digits)
        self.otp_entries = []
        otp_length = 6
        start_x = 170  
        y = 370        
        gap = 50      
        def only_digit(char):
            return char.isdigit()

        vcmd = (self.register(only_digit), '%S')

        for i in range(otp_length):
            entry = ctk.CTkEntry(
                self,
                width=30,
                font=("Tai Heritage Pro", 22),
                justify="center",
                validate="key",
                validatecommand=vcmd,
                state="normal" if i == 0 else "disabled"  # Only first is enabled
            )
            win = self.canvas.create_window(start_x + i*gap, y, window=entry)
            self.otp_entries.append(entry)
            # Draw underline
            self.canvas.create_line(start_x + i*gap - 15, y+20, start_x + i*gap + 15, y+20, fill="white", width=2)

            # Bind to move focus and enable/disable logic
            def on_key(event, idx=i):
                value = self.otp_entries[idx].get()
                # If a digit is entered, enable the next entry
                if value and idx < otp_length - 1:
                    self.otp_entries[idx+1].configure(state="normal")
                    self.otp_entries[idx+1].focus_set()
                # If entry is cleared, disable all next entries
                elif not value:
                    for j in range(idx+1, otp_length):
                        self.otp_entries[j].delete(0, 'end')
                        self.otp_entries[j].configure(state="disabled")
            entry.bind("<KeyRelease>", on_key)

        # Show OTP note image and info text
        otp_note_img = Image.open("attendance/public/otp rectangle.png").resize((520, 170), Image.LANCZOS)   
        self.note = ImageTk.PhotoImage(otp_note_img)
        self.otp_note_image_id = self.canvas.create_image(31, 150, image=self.note, anchor="nw")

        # Show sign up button for OTP verification
        signup_img = Image.open("attendance/public/Rectangle 11.png").resize((520, 80), Image.LANCZOS)   
        self.sign_up = ImageTk.PhotoImage(signup_img)

        # Show info text about OTP being sent
        self.otp_sent_text_id = self.canvas.create_text(
            291, 235, 
            text=f"We've sent an OTP verification code to:\n{email}",
            font=("Tai Heritage Pro", 20),
            fill="white",
            anchor="center",
            justify="center"
        )


        self.sign_up_image_id = self.canvas.create_image(31, 450, image=self.sign_up, anchor="nw")
        self.sign_up_button = ctk.CTkButton(self, text="Sign Up", font=("Tai Heritage Pro", 20), fg_color="#686882", bg_color="#686882", hover=False)
        self.signup = self.canvas.create_window(31 + 260, 450 + 40, window=self.sign_up_button)

        # Show back button for returning to credentials input
        self.canvas.itemconfigure(self.back_text_button, state='normal')
        self.canvas.tag_unbind(self.back_text_button, "<Button-1>")
        self.canvas.tag_bind(self.back_text_button, "<Button-1>", self.back_to_credentials)


if __name__ == "__main__":
    # Entry point for standalone testing of the RegisterFrame
    root = ctk.CTk()
    root.geometry("580x681")
    login = RegisterFrame(root)
    login.pack()
    root.mainloop()