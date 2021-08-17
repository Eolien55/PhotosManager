import multiprocessing as mp
from collections import namedtuple
from queue import Empty


Msg = namedtuple("Msg", ["event", "args"])


class BaseProcess:
    pass


class BaseProcess(mp.Process):
    """A process backed by an internal queue for one-way message passing"""

    name = "Process"
    has_parent = False

    def __init__(self, *args, **kwgs):
        if self.has_parent:
            self.parent = args[0]
            args = args[1:]
        super().__init__(*args, **kwgs)

        self._start = super().start

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
            event, _ = msg
            if event == "END":
                del event, _
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

        self._start()

    def __lt__(self, other: BaseProcess):
        return self.queue.qsize() < other.queue.qsize()

    def __gt__(self, other: BaseProcess):
        return self.queue.qsize() > other.queue.qsize()
