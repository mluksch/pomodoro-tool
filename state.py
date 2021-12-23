import time

import config
from utils import *


class State:
    def __init__(self):
        self.round = 0
        self.start_time = 0
        self.mode = config.MODE_STOP
        self.on_state_paused = None
        self.on_pause_finished = None
        self.on_work_started = None
        self.on_session_stopped = None

    def listen(self, on_state_paused, on_pause_finished, on_work_started, on_session_stopped):
        self.on_state_paused = on_state_paused
        self.on_pause_finished = on_pause_finished
        self.on_work_started = on_work_started
        self.on_session_stopped = on_session_stopped

    def start(self):
        if self.mode == config.MODE_PLAY:
            pass
        elif self.mode == config.MODE_STOP:
            self.mode = config.MODE_PLAY
            if self.on_work_started is not None:
                self.on_work_started()
            self.start_time = time.time()
            self.round = 0
            self.start_time = time.time()
        elif self.mode == config.MODE_PAUSE_FINISHED:
            self.start_time = time.time()
            self.mode = config.MODE_PLAY
            if self.on_work_started is not None:
                self.on_work_started()

    def _get_timer_text(self):
        now = time.time()
        elapsed = round(now - self.start_time)
        diff = None
        if self.mode == config.MODE_PLAY:
            diff = max(mins_to_sec(config.WORK_PHASE) - elapsed, 0)
        elif self.mode == config.MODE_SMALL_PAUSE:
            diff = max(mins_to_sec(config.SMALL_PAUSE_PHASE) - elapsed, 0)
        elif self.mode == config.MODE_BIG_PAUSE:
            diff = max(mins_to_sec(config.BIG_PAUSE_PHASE) - elapsed, 0)
        elif self.mode == config.MODE_STOP:
            diff = max(mins_to_sec(config.WORK_PHASE), 0)
        return "00:00" if diff is None else timer_text(diff)

    def on_tick(self):
        timer = self._get_timer_text()
        if self.mode == config.MODE_STOP:
            pass
        elif self.mode == config.MODE_PLAY:
            if timer == "00:00":
                if self.round < 4:
                    self.mode = config.MODE_SMALL_PAUSE
                    if self.on_state_paused is not None:
                        self.on_state_paused()
                    self.round += 1
                    self.start_time = time.time()
                else:
                    self.mode = config.MODE_BIG_PAUSE
                    if self.on_state_paused is not None:
                        self.on_state_paused()
                    self.round += 1
                    self.start_time = time.time()
        elif self.mode == config.MODE_SMALL_PAUSE:
            if timer == "00:00":
                self.mode = config.MODE_PAUSE_FINISHED
                if self.on_pause_finished is not None:
                    self.on_pause_finished()
        elif self.mode == config.MODE_BIG_PAUSE:
            if timer == "00:00":
                self.mode = config.MODE_PAUSE_FINISHED
                if self.on_pause_finished is not None:
                    self.on_pause_finished()
        return timer

    def reset(self):
        self.mode = config.MODE_STOP
        if self.on_session_stopped is not None:
            self.on_session_stopped()
        self.round = 0
        self.start_time = 0
