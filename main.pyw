from gui import Gui
from state import State

# ---------------------------- CONSTANTS ------------------------------- #


# ---------------------------- TIMER RESET ------------------------------- #

# ---------------------------- TIMER MECHANISM ------------------------------- # 

# ---------------------------- COUNTDOWN MECHANISM ------------------------------- # 

# ---------------------------- UI SETUP ------------------------------- #

state = State()
gui = Gui()


def on_click_start():
    state.start()


def on_click_reset():
    state.reset()


def on_tick():
    return state.on_tick()


def on_state_paused():
    gui.pause()


def on_pause_finished():
    gui.pause_end()


def on_work_started():
    gui.work()


def on_session_stopped():
    gui.stop()


gui.listen(on_click_reset=on_click_reset, on_click_start=on_click_start, on_tick=on_tick)
state.listen(on_state_paused, on_pause_finished, on_work_started, on_session_stopped)
gui.display()
