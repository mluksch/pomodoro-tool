from tkinter import *

import config
from utils import *


class Gui:
    def __init__(self):
        self.on_reset = None
        self.on_start = None
        root = Tk()
        root.config(bg=config.YELLOW, pady=3, padx=5)
        root.minsize(width=config.WIDTH, height=config.HEIGHT)
        root.wm_title("Pomodoro")
        root.resizable(False, False)
        self.rounds = 0
        self.root = root
        self._start_ticking()

        c = Canvas(root)
        c.config(width=140, height=40, bg=config.YELLOW)
        self.countdown_text = c.create_text(70, 20, fill="red",
                                            text=timer_text(mins_to_sec(config.WORK_PHASE)),
                                            font=(config.FONT_NAME, 30, "bold"))
        c.grid(column=1, row=1)
        self.canvas = c

        self.status_lbl = Label(text="Start")
        self.status_lbl.config(fg=config.GREEN, bg=config.YELLOW, font=(config.FONT_NAME, 12, "bold"))
        self.status_lbl.grid(column=1, row=0)

        btn_start = Button(text="Start", width=6, height=2, command=self._on_start)
        btn_start.grid(column=0, row=1, sticky="e")
        btn_start.focus()
        self.btn_start = btn_start

        btn_reset = Button(text="Reset", width=6, height=2, command=self._on_reset)
        btn_reset.grid(column=2, row=1, sticky="w")
        self._display_rounds()
        self.on_tick = None

    def _display_rounds(self):
        symbols = []
        for i in range(0, 4):
            symbols += config.CHECKMARK if i < self.rounds else config.EMPTYMARK
        lbl_rounds = Label(text=" ".join(symbols), bg=config.YELLOW, fg=config.GREEN,
                           font=(config.FONT_NAME, 15, "bold"))
        lbl_rounds.grid(column=1, row=2)

    def display(self):
        self.root.mainloop()

    def _display_status(self, status):
        self.status_lbl.config(text=status)

    def work(self):
        self._display_status("Try to work")
        self._put_window_to_front(put_back=False)

    def work_end(self):
        self._display_status("Session finished")
        self._put_window_to_front(put_back=False)

    def pause(self):
        self.rounds += 1
        self._display_rounds()
        self._display_status("Have a break")
        self._put_window_to_front()

    def pause_end(self):
        self._display_status("Break over")
        self._put_window_to_front(put_back=False)

    def stop(self):
        self.rounds = 0
        self._display_rounds()
        self._display_status("Start")
        self.root.bell()
        self.btn_start.focus()

    def _on_start(self):
        if self.on_start is not None:
            self.on_start()

    def _start_ticking(self):
        self.root.after(1000, self._tick)

    def _tick(self):
        if self.on_tick is not None:
            new_time = self.on_tick()
            self._update_countdown(new_time)
        self.root.after(1000, self._tick)

    def _on_reset(self):
        self.rounds = 0
        self._display_rounds()
        if self.on_reset is not None:
            self.on_reset()

    def _update_countdown(self, countdown):
        self.canvas.itemconfigure(self.countdown_text, text=countdown)

    def _put_window_to_front(self, put_back=True):
        self.root.bell()
        self.root.after(1, lambda: self.root.focus_force())
        self.root.after(2, lambda: self.btn_start.focus_force())
        self.root.attributes('-topmost', True)
        self.root.update()
        if put_back:
            self.root.after_idle(self.root.attributes, '-topmost', False)

    def listen(self, on_click_reset, on_click_start, on_tick):
        self.on_reset = on_click_reset
        self.on_start = on_click_start
        self.on_tick = on_tick
