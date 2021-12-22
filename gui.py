import base64
from tkinter import *

from tomato_pic import tomato_pic


class Gui:
    def __init__(self):
        root = Tk()
        root.minsize(width=500, height=400)
        root.wm_title("Pomodoro-Technique")
        root.resizable(False, False)

        bg_img = PhotoImage(data=base64.b64decode(tomato_pic.encode("utf-8")))
        bg_lbl = Label(image=bg_img)
        bg_lbl.place(x=0, y=0, relheight=1.0, relwidth=1.0)

        root.mainloop()
