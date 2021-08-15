import multiprocessing as mp
from collections import namedtuple

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
        if getattr(self, "before_loop"):
            self.before_loop()

        while True:
            msg = self.queue.get()
            if msg == "EOF":
                break
            self.dispatch(msg)

        if getattr(self, "after_loop"):
            self.after_loop()
