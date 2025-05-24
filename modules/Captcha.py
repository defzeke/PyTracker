import customtkinter as ctk
from PIL import Image, ImageTk

class CaptchaWidget(ctk.CTkFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        # Set up the frame appearance
        self.configure(width=300, height=80, fg_color="#f9f9f9", corner_radius=8)
        
        self.verified = False

        # Checkbox button for user to click to verify
        self.checkbox_button = ctk.CTkButton(
            self,
            width=26,
            height=26,
            text="",
            command=self.verify_human,
            fg_color="white",
            text_color="green",
            hover=False,
            border_color="#999",
            border_width=2,
            corner_radius=2
        )
        self.checkbox_button.place(x=30, rely=0.5, anchor="center")

        # Label next to the checkbox
        self.robot_label = ctk.CTkLabel(
            self,
            text="I'm not a robot",
            font=("Arial", 15),
            text_color="black"
        )
        self.robot_label.place(x=100, rely=0.5, anchor="center")

        # Small badge label to mimic reCAPTCHA branding
        self.badge_label = ctk.CTkLabel(
            self,
            text="reCAPTCHA\nPrivacy - Terms",
            font=("Arial", 6),
            justify="right",
            text_color="#555"
        )
        self.badge_label.place(x=230, y=50)

        # Add the captcha image (icon)
        self.put_captcha_image()

    def put_captcha_image(self):
        # Load and display the captcha icon image
        captcha_img = Image.open("attendance/public/captcha.png").resize((37, 37), Image.LANCZOS)
        self.captcha = ImageTk.PhotoImage(captcha_img)
        self.captcha_label = ctk.CTkLabel(self, image=self.captcha, text="", fg_color="transparent")
        self.captcha_label.place(x=235, y=14)

    def verify_human(self):
        # Simulate verification process when checkbox is clicked
        if not self.verified:
            self.checkbox_button.configure(fg_color="gray", text="...")  
            self.robot_label.configure(text="Verifying...", text_color="orange")
            self.after(1000, self.complete_verification)
        else:
            self.robot_label.configure(text="You're already verified!", text_color="blue")

    def complete_verification(self):
        # Mark as verified and update UI
        self.checkbox_button.configure(text="✓", fg_color="green")
        self.robot_label.configure(text="You're not a robot", text_color="green")
        self.verified = True
