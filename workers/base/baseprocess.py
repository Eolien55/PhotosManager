import multiprocessing as mp
from collections import namedtuple
import os

Msg = namedtuple("Msg", ["event", "args"])


class BaseProcess(mp.Process):
    """A process backed by an internal queue for one-way message passing"""

    name = "Process"

    def __init__(self, *args, **kwgs):
        super().__init__(*args, **kwgs)

        self.queue = mp.Queue()

    def send(self, event, *args):
        """Puts the event and args as a `Msg` on the queue"""
        msg = Msg(event, args)

        self.queue.put(msg)

    def dispatch(self, msg):
        """Calls handler depending on the message"""
        event, args = msg

        handler = getattr(self, f"handle_{event}", None)
        if not handler:
            raise NotImplementedError(f"{self.name} has no handler for [{event}]")

        handler(*args)

    def run(self):
        if hasattr(self, "before_loop"):
            self.before_loop()

        while True:
            msg = self.queue.get()
            if msg == "END":
                break
            self.dispatch(msg)
        try:
            while True:
                self.queue.get_nowait()
        except Exception:
            pass

        if hasattr(self, "after_loop"):
            self.after_loop()

    def start(self):
        if hasattr(self, "before_start"):
            self.before_start()

        self._check_closed()
        assert self._popen is None, "cannot start a process twice"
        assert (
            self._parent_pid == os.getpid()
        ), "can only start a process object created by current process"
        assert not mp._current_process._config.get(
            "daemon"
        ), "daemonic processes are not allowed to have children"
        mp._cleanup()
        self._popen = self._Popen(self)
        self._sentinel = self._popen.sentinel
        # Avoid a refcycle if the target function holds an indirect
        # reference to the process object (see bpo-30775)
        del self._target, self._args, self._kwargs
        mp._children.add(self)
