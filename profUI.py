import tkinter as tk
import customtkinter as ctk
from PIL import ImageTk, Image
from mainProgram import Window

class NavigationPanel(Window):
    def __init__(self):
        super().__init__()

        self.root.resizable(True, True)
        self.root.state("zoomed")
        self.root.resizable(False, False)
        
        # Used tk.Canvas for animation only kasi may move() function sya unlike sa ctk
        self.canvas = tk.Canvas(self.root, width=2000, height=2000, bg="#E3E9ED", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        # Navigation rectangle properties
        self.nav_width = 100
        self.nav_rect = self.canvas.create_rectangle(-self.nav_width, 0, 0, 1000, fill="#272757", outline="")
        self.nav_visible = False
        self.animating = False

        self.canvas.tag_raise(self.nav_rect)

        self.root.bind("<Motion>", self.on_mouse_move)
        self.root.after(100, self.draw_top_bar)

        self.nav_text = None
        self.notif = None



###########################################################################################
    def on_mouse_move(self, event):
        if event.x <= 10 and not self.nav_visible and not self.animating:
            self.slide_in()
        elif event.x > self.nav_width and self.nav_visible and not self.animating:
            self.slide_out()

    def slide_in(self):
        self.animating = True
        def animate():
            x1, y1, x2, y2 = self.canvas.coords(self.nav_rect)
            if x1 < 0:
                self.canvas.move(self.nav_rect, 10, 0)
                self.root.after(10, animate)
            else:
                self.canvas.coords(self.nav_rect, 0, 0, self.nav_width, 1000)
                self.nav_visible = True
                self.animating = False
                if not self.nav_text:
                    self.nav_text = self.canvas.create_text(45, 40, text="logo", fill="white", font=("Actor", 16))
        animate()

    def slide_out(self):
        self.animating = True
        def animate():
            x1, y1, x2, y2 = self.canvas.coords(self.nav_rect)
            if x1 > -self.nav_width:
                self.canvas.move(self.nav_rect, -10, 0)
                self.root.after(10, animate)
            else:
                self.canvas.coords(self.nav_rect, -self.nav_width, 0, 0, 1000)
                self.nav_visible = False
                self.animating = False
                if self.nav_text:
                    self.canvas.delete(self.nav_text)
                    self.nav_text = None
        animate()

    def draw_top_bar(self):
        width = self.canvas.winfo_width()
        if width > 0:
            top_bar = self.canvas.create_rectangle(0, 0, width, 80, fill="white", outline="")
            self.canvas.tag_lower(top_bar)
            
            self.add_top_bar_lines(width)
            self.top_bar_features()
            self.account_settings()
        else:
            self.root.after(100, self.draw_top_bar)

    def add_top_bar_lines(self, width):
        self.canvas.create_line(1370, 0, 1370, 81, fill="gray", width=1)
        self.canvas.create_line(1260, 0, 1260, 81, fill="gray", width=1)
###########################################################################################




    def top_bar_features(self):
        # notif
        notif = Image.open("attendance/public/image 11.png")
        resized_notif_logo = notif.resize((30, 30), Image.LANCZOS)
        self.notif = ImageTk.PhotoImage(resized_notif_logo)
        # recitation
        recit = Image.open("attendance/public/image 18.png")
        resized_recit_logo = recit.resize((42, 42), Image.LANCZOS)
        self.recit = ImageTk.PhotoImage(resized_recit_logo)
        # message
        msg = Image.open("attendance/public/image 17.png")
        resized_msg_logo = msg.resize((37, 37), Image.LANCZOS)
        self.msg = ImageTk.PhotoImage(resized_msg_logo)
        # status
        stat = Image.open("attendance/public/image 16.png")
        resized_status_logo = stat.resize((37, 37), Image.LANCZOS)
        self.status = ImageTk.PhotoImage(resized_status_logo)
        # sticky nav bar
        stick = Image.open("attendance/public/image 15.png")
        resized_sticky_logo = stick.resize((37, 37), Image.LANCZOS)
        self.sticky = ImageTk.PhotoImage(resized_sticky_logo)


        notification = self.canvas.create_image(1300, 25, image=self.notif, anchor="nw")
        recitation = self.canvas.create_image(650, 20, image=self.recit, anchor="nw")
        message = self.canvas.create_image(550, 24, image=self.msg, anchor="nw")
        status = self.canvas.create_image(445, 23, image=self.status, anchor="nw")
        sticky = self.canvas.create_image(10, 23, image=self.sticky, anchor="nw")

    def account_settings(self):
        # settings dropdown
        settings_dropdown = Image.open("attendance/public/image 9.png")
        resized_dropdown_logo = settings_dropdown.resize((15, 15), Image.LANCZOS)
        self.dropdown = ImageTk.PhotoImage(resized_dropdown_logo)
        # display picture
        dp = Image.open("attendance/public/display pic.png")
        resized_dp_logo = dp.resize((40, 40), Image.LANCZOS)
        self.dp = ImageTk.PhotoImage(resized_dp_logo)

        dropdown = self.canvas.create_image(1650, 32, image=self.dropdown, anchor="nw")
        display_pic = self.canvas.create_image(1600, 20, image=self.dp, anchor="nw")





if __name__ == "__main__":
    app = NavigationPanel()
    app.run()
