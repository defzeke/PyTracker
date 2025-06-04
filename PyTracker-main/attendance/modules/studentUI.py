import tkinter as tk
import customtkinter as ctk
from PIL import ImageTk, Image
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
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
        animate()

    def draw_top_bar(self):
        width = self.canvas.winfo_width()

        if width > 0:   
            top_bar = self.canvas.create_rectangle(0, 0, width, 80, fill="white", outline="")
            self.canvas.tag_lower(top_bar) 
        else:
            self.root.after(100, self.draw_top_bar)
###########################################################################################

    def test(self):
        pass


if __name__ == "__main__":
    app = NavigationPanel()
    app.run()
