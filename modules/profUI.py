import tkinter as tk
import customtkinter as ctk
from PIL import ImageTk, Image
from tkcalendar import Calendar
import pandas as pd
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from mainProgram import Window

class NavigationPanel(Window):
    def __init__(self):
        super().__init__()
        self.root.state("zoomed")
        self.root.resizable(False, False)
        
        self.canvas = tk.Canvas(self.root, width=2000, height=2000, bg="#E3E9ED", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.positions = {
            'dashboard': (20/2000, 100/1000),  
            'attendance': (19/2000, 175/1000),    
            'schedule': (19/2000, 250/1000),     
            'add_class': (20/2000, 325/1000), 

            'dropdown': (1650/2000, 32/1000),
            'display_pic': (1600/2000, 20/1000),
            'first_line': (1370/2000, 0/1000),
            'second_line': (1260/2000, 0/1000),
            'notification': (1300/2000, 25/1000),
            'recitation': (650/2000, 20/1000),
            'message': (550/2000, 24/1000),
            'status': (445/2000, 23/1000),
            'dashboard_label': (240/2000, 140/1000),
            'rect1': (200/2000, 180/1000),
            'rect2': (200/2000, 510/1000),
            'rect3': (1060/2000, 510/1000),
            'attendance_label': (240/2000, 140/1000),
            'schedule_label': (240/2000, 140/1000),
            'adclass_label': (240/2000, 140/1000),
}
        
        navbar_img = Image.open("attendance/public/rectangle 1.png").resize((90, 1000), Image.LANCZOS)
        self.navbar = ImageTk.PhotoImage(navbar_img)
        self.navbar_img_id = self.canvas.create_image(0, 0, image=self.navbar, anchor="nw")  

        self.canvas.bind("<Configure>", self.on_canvas_resize)

        self.root.after(100, self.draw_top_bar)
        self.load_navbar_features()

        self.root.after(100, self.show_dashboard_ui)
        self.active_section = "dashboard"

###########################################################################################
#                        ANIMATIONS /// TRANSITIONS /// DRAW                              #
###########################################################################################
    def on_canvas_resize(self, event):
        w, h = event.width, event.height

        self.load_navbar_image(h)
        self.canvas.itemconfig(self.navbar_img_id, image=self.navbar)
        x, _ = self.canvas.coords(self.navbar_img_id)
        self.canvas.coords(self.navbar_img_id, x, 0)

        if hasattr(self, 'top_bar'):
            self.canvas.coords(self.top_bar, 0, 0, w, 80)

        for name, (x_ratio, y_ratio) in self.positions.items():
            item_id = getattr(self, name, None)
            if item_id:  
                self.canvas.coords(item_id, int(w * x_ratio), int(h * y_ratio))

    def draw_top_bar(self):
        width = self.canvas.winfo_width()
        if width > 0:
            self.top_bar = self.canvas.create_rectangle(0, 0, width, 80, fill="white", outline="")
            self.canvas.tag_lower(self.top_bar)
            
            self.add_top_bar_lines(width)
            self.top_bar_features()
            self.account_settings()
        else:
            self.root.after(100, self.draw_top_bar)

    def add_top_bar_lines(self, width):
        self.first_line = self.canvas.create_line(1370, 0, 1370, 81, fill="gray", width=1)
        self.second_line = self.canvas.create_line(1260, 0, 1260, 81, fill="gray", width=1)

    def set_active(self, selected):
        self.canvas.itemconfig(self.dashboard, image=self.db_inactive)
        self.canvas.itemconfig(self.attendance, image=self.attend_inactive)
        self.canvas.itemconfig(self.schedule, image=self.sched_inactive)
        self.canvas.itemconfig(self.add_class, image=self.add_inactive)

        if selected == "dashboard":
            self.canvas.itemconfig(self.dashboard, image=self.db_active)
            self.active_nav = "dashboard"
        elif selected == "attendance":
            self.canvas.itemconfig(self.attendance, image=self.attend_active)
            self.active_nav = "attendance"
        elif selected == "schedule":
            self.canvas.itemconfig(self.schedule, image=self.sched_active)
            self.active_nav = "schedule"
        elif selected == "add_class":
            self.canvas.itemconfig(self.add_class, image=self.add_active)
            self.active_nav = "add_class"

    def set_topbar_active(self, name):
        if not hasattr(self, 'topbar_windows'):
            self.topbar_windows = {}

        popup_width = 500
        popup_height = 500

        if name == "recitation":
            popup_width, popup_height = 400, 500
        elif name == "message":
            popup_width, popup_height = 900, 700
        elif name == "status":
            popup_width, popup_height = 400, 500
        elif name == "notification":
            popup_width, popup_height = 350, 700
        else:
            popup_width, popup_height = 300, 500  

        if self.active_topbar == name:
            self.canvas.itemconfig(self.topbar_items[name], image=self.topbar_icons[name]["inactive"])
            self.active_topbar = None

            if name in self.topbar_windows:
                self.topbar_windows[name].destroy()
                del self.topbar_windows[name]

        else:
            for key, item_id in self.topbar_items.items():
                self.canvas.itemconfig(item_id, image=self.topbar_icons[key]["inactive"])
                if key in self.topbar_windows:
                    self.topbar_windows[key].destroy()
                    del self.topbar_windows[key]

            self.canvas.itemconfig(self.topbar_items[name], image=self.topbar_icons[name]["active"])
            self.active_topbar = name

            popup = ctk.CTkToplevel(self.root)
            popup.withdraw()
            popup.overrideredirect(True)
            popup.resizable(False, False)
            popup.configure(bg="white")
            popup.lift()
            popup.attributes("-topmost", True)

            frame = ctk.CTkFrame(popup, fg_color="white", corner_radius=0)
            frame.pack(fill="both", expand=True)

            def place_popup():
                screen_width = popup.winfo_screenwidth()
                screen_height = popup.winfo_screenheight()

                if name in ["recitation", "message", "status"]:
                    x = (screen_width - popup_width) // 2
                    y = (screen_height - popup_height) // 2
                elif name == "notification":
                    x = screen_width - popup_width - 220
                    y = 170
                else:
                    x, y = 1050, 170

                popup.geometry(f"{popup_width}x{popup_height}+{x}+{y}")
                popup.deiconify()
                popup.overrideredirect(False)
                popup.update_idletasks()
                popup.overrideredirect(True)

            popup.after(50, place_popup)

            self.topbar_windows[name] = popup


    def load_navbar_features(self):
        db_inactive = Image.open("attendance/public/dashboard=Default.png").resize((50, 50), Image.LANCZOS)
        db_active = Image.open("attendance/public/dashboard=Active.png").resize((50, 50), Image.LANCZOS)
        self.db_inactive = ImageTk.PhotoImage(db_inactive)
        self.db_active = ImageTk.PhotoImage(db_active)

        attend_inactive = Image.open("attendance/public/attendance=Default.png").resize((55, 55), Image.LANCZOS)
        attend_active = Image.open("attendance/public/attendance=Active.png").resize((55, 55), Image.LANCZOS)
        self.attend_inactive = ImageTk.PhotoImage(attend_inactive)
        self.attend_active = ImageTk.PhotoImage(attend_active)

        sched_inactive = Image.open("attendance/public/schedule=Default.png").resize((55, 55), Image.LANCZOS)
        sched_active = Image.open("attendance/public/schedule=Active.png").resize((55, 55), Image.LANCZOS)
        self.sched_inactive = ImageTk.PhotoImage(sched_inactive)
        self.sched_active = ImageTk.PhotoImage(sched_active)

        add_inactive = Image.open("attendance/public/add class=Default.png").resize((57, 57), Image.LANCZOS)
        add_active = Image.open("attendance/public/add class=Active.png").resize((57, 57), Image.LANCZOS)
        self.add_inactive = ImageTk.PhotoImage(add_inactive)
        self.add_active = ImageTk.PhotoImage(add_active)

        self.dashboard = self.canvas.create_image(20, 100, image=self.db_inactive, anchor="nw", tags="dashboard")
        self.attendance = self.canvas.create_image(19, 175, image=self.attend_inactive, anchor="nw", tags="attendance")
        self.schedule = self.canvas.create_image(19, 250, image=self.sched_inactive, anchor="nw", tags="schedule")
        self.add_class = self.canvas.create_image(20, 325, image=self.add_inactive, anchor="nw", tags="add_class")

        self.feature_ids = [self.dashboard, self.attendance, self.schedule, self.add_class]

        self.canvas.tag_bind(self.dashboard, "<Button-1>", lambda e: self.on_nav_click("dashboard"))
        self.canvas.tag_bind(self.attendance, "<Button-1>", lambda e: self.on_nav_click("attendance"))
        self.canvas.tag_bind(self.schedule, "<Button-1>", lambda e: self.on_nav_click("schedule"))
        self.canvas.tag_bind(self.add_class, "<Button-1>", lambda e: self.on_nav_click("add_class"))

        self.active_nav = None
        self.set_active("dashboard")


    def hide_dashboard_ui(self):
        if hasattr(self, 'dashboard_widgets'):
            for widget in self.dashboard_widgets:
                self.canvas.delete(widget)
            self.dashboard_widgets.clear()


    def hide_attendance_ui(self):
        if hasattr(self, 'attendance_widgets'):
            for widget in self.attendance_widgets:
                self.canvas.delete(widget)
            self.attendance_widgets.clear()


    def hide_schedule_ui(self):
        if hasattr(self, 'schedule_widgets'):
            for widget in self.schedule_widgets:
                self.canvas.delete(widget)
            self.schedule_widgets.clear()


    def hide_adclass_ui(self):
        if hasattr(self, 'adclass_widgets'):
            for widget in self.adclass_widgets:
                self.canvas.delete(widget)
            self.adclass_widgets.clear()


    def switch_section(self, section_name):
        if hasattr(self, 'active_section'):
            if self.active_section == "dashboard":
                self.hide_dashboard_ui()
            elif self.active_section == "attendance":
                self.hide_attendance_ui()
            elif self.active_section == "schedule":
                self.hide_schedule_ui()
            elif self.active_section == "add_class":
                self.hide_adclass_ui()

        if section_name == "dashboard":
            self.show_dashboard_ui()
        elif section_name == "attendance":
            self.show_attendance_ui()
        elif section_name == "schedule":
            self.show_schedule_ui()
        elif section_name == "add_class":
            self.show_adclass_ui()

        self.active_section = section_name


    def on_nav_click(self, section):
        self.set_active(section)
        self.switch_section(section)
        
###########################################################################################




###########################################################################################
#                                         MAIN                                            #
###########################################################################################

    def top_bar_features(self):
        self.topbar_icons = {
            "notification": {
                "active": ImageTk.PhotoImage(Image.open("attendance/public/notif=active.png").resize((30, 30), Image.LANCZOS)),
                "inactive": ImageTk.PhotoImage(Image.open("attendance/public/notif=Default.png").resize((30, 30), Image.LANCZOS)),
            },
            "recitation": {
                "active": ImageTk.PhotoImage(Image.open("attendance/public/recit=active.png").resize((42, 42), Image.LANCZOS)),
                "inactive": ImageTk.PhotoImage(Image.open("attendance/public/recit=Default.png").resize((42, 42), Image.LANCZOS)),
            },
            "message": {
                "active": ImageTk.PhotoImage(Image.open("attendance/public/msg=active.png").resize((37, 37), Image.LANCZOS)),
                "inactive": ImageTk.PhotoImage(Image.open("attendance/public/msg=Default.png").resize((37, 37), Image.LANCZOS)),
            },
            "status": {
                "active": ImageTk.PhotoImage(Image.open("attendance/public/stat=active.png").resize((37, 37), Image.LANCZOS)),
                "inactive": ImageTk.PhotoImage(Image.open("attendance/public/stat=Default.png").resize((37, 37), Image.LANCZOS)),
            }
        }

        self.topbar_items = {
            "notification": self.canvas.create_image(1300, 25, image=self.topbar_icons["notification"]["inactive"], anchor="nw"),
            "recitation": self.canvas.create_image(650, 20, image=self.topbar_icons["recitation"]["inactive"], anchor="nw"),
            "message": self.canvas.create_image(550, 24, image=self.topbar_icons["message"]["inactive"], anchor="nw"),
            "status": self.canvas.create_image(445, 23, image=self.topbar_icons["status"]["inactive"], anchor="nw"),
        }

        for name in self.topbar_items:
            self.canvas.tag_bind(self.topbar_items[name], "<Button-1>", lambda e, n=name: self.set_topbar_active(n))

        self.active_topbar = None


    def account_settings(self): 
        # settings dropdown
        settings_dropdown = Image.open("attendance/public/image 9.png").resize((15, 15), Image.LANCZOS)
        self.dd = ImageTk.PhotoImage(settings_dropdown)

        # display picture
        dp = Image.open("attendance/public/display pic.png").resize((40, 40), Image.LANCZOS)
        self.dp = ImageTk.PhotoImage(dp)

        self.dropdown = self.canvas.create_image(1650, 32, image=self.dd, anchor="nw")
        self.display_pic = self.canvas.create_image(1600, 20, image=self.dp, anchor="nw")


    def show_dashboard_ui(self):
        self.dashboard_label = self.canvas.create_text(240, 140, text="Dashboard", font=("Tai Heritage Pro", 40, "bold"), fill="black")
        self.frame = ctk.CTkFrame(self.canvas, width=1385, height=340, corner_radius=20, fg_color="#ffffff")
        self.rect = self.canvas.create_window(200, 180, window=self.frame, anchor="nw")

        self.frame2 = ctk.CTkFrame(self.canvas, width=820, height=340, corner_radius=20, fg_color="#ffffff")
        self.rect2 = self.canvas.create_window(200, 550, window=self.frame2, anchor="nw")

        self.frame3 = ctk.CTkFrame(self.canvas, width=520, height=340, corner_radius=20, fg_color="#ffffff")
        self.rect3 = self.canvas.create_window(1060, 550, window=self.frame3, anchor="nw")

        self.dashboard_widgets = [self.dashboard_label, self.rect, self.rect2, self.rect3]
   

    def show_attendance_ui(self):
        self.attendance_label = self.canvas.create_text(240, 140, text="Attendance", font=("Tai Heritage Pro", 40, "bold"), fill="black")
        self.attendance_widgets = [self.attendance_label]


    def show_schedule_ui(self):
        self.schedule_label = self.canvas.create_text(240, 140, text="Schedule", font=("Tai Heritage Pro", 40, "bold"), fill="black")
        self.schedule_widgets = [self.schedule_label]


    def show_adclass_ui(self):
        self.adclass_label = self.canvas.create_text(240, 140, text="Add Class", font=("Tai Heritage Pro", 40, "bold"), fill="black")
        self.adclass_widgets = [self.adclass_label]

###########################################################################################

if __name__ == "__main__":
    app = NavigationPanel()
    app.run()
