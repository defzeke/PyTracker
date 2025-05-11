import customtkinter as ctk
from PIL import Image, ImageTk

class RealCaptchaUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("reCAPTCHA Verification")
        self.geometry("420x180")
        self.resizable(False, False)

        self.verified = False

        self.canvas = ctk.CTkCanvas(self, width=420, height=180, bg="#f9f9f9", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.captcha_frame = ctk.CTkFrame(self.canvas, width=400, height=100, corner_radius=8, fg_color="white")
        self.canvas.create_window(210, 90, window=self.captcha_frame)

        self.checkbox_button = ctk.CTkButton(
            self.captcha_frame,
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
        self.checkbox_button.place(x=20, y=35)

        self.robot_label = ctk.CTkLabel(
            self.captcha_frame,
            text="I'm not a robot",
            font=("Arial", 15),
            text_color="black"
        )
        self.robot_label.place(x=60, y=36)

        self.badge_label = ctk.CTkLabel(
            self.captcha_frame,
            text="reCAPTCHA\nPrivacy - Terms",
            font=("Arial", 8),
            justify="right",
            text_color="#555"
        )
        self.badge_label.place(x=290, y=60)

        self.status_label = ctk.CTkLabel(self, text="", text_color="green", font=("Arial", 14))
        self.canvas.create_window(210, 150, window=self.status_label)  
        self.put_captcha_image()

    def put_captcha_image(self):
        captcha_img = Image.open("attendance/public/captcha.png").resize((37, 37), Image.LANCZOS)
        self.captcha = ImageTk.PhotoImage(captcha_img)

        self.captcha_label = ctk.CTkLabel(self.captcha_frame, image=self.captcha, text="", fg_color="transparent")
        self.captcha_label.place(x=300, y=20)  


    def verify_human(self):
        if not self.verified:
            self.checkbox_button.configure(fg_color="gray", text="...")  
            self.robot_label.configure(text="Verifying...")
            self.robot_label.configure(text_color="orange")

            self.after(1000, self.complete_verification) 
        else:
            self.robot_label.configure(text="You're already verified!")
            self.robot_label.configure(text_color="blue")

    def complete_verification(self):
        self.checkbox_button.configure(text="✓", fg_color="green")
        self.robot_label.configure(text="You're not a robot")
        self.robot_label.configure(text_color="green")
        self.verified = True

if __name__ == "__main__":
    ctk.set_appearance_mode("light")  
    ctk.set_default_color_theme("blue")
    app = RealCaptchaUI()
    app.mainloop()
