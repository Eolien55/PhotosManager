import multiprocessing as mp
import threading as th
from collections import namedtuple
from queue import Empty
import sys
import os

mp.freeze_support()


Msg = namedtuple("Msg", ["event", "args"])


class BaseThing:
    def __init__(self, *args) -> None:
        pass

    def __getitem__(self, item: str):
        if isinstance(item, str):
            if item.upper() == "THREAD":
                parent_class = th.Thread
            elif item.upper() == "PROCESS":
                parent_class = mp.Process
            else:
                raise NotImplementedError(
                    "I don't know what '{}' means, and at this point, i'm too afraid to ask".format(
                        item
                    )
                )
        else:
            parent_class = item

        class BaseWorker:
            pass

        class BaseWorker(parent_class):
            """A process backed by an internal queue for one-way message passing"""

            name = "Process"
            has_parent = False
            muted = False

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

            def dispatch(self, msg: Msg):
                """Calls handler depending on the message"""
                event, args = msg

                handler = getattr(self, f"handle_{event}", None)
                if not handler:
                    raise NotImplementedError(
                        f"{self.name} has no handler for [{event}]"
                    )

                handler(*args)

            def run(self):
                if self.muted:
                    sys.stdout = open(os.devnull, "w")

                if hasattr(self, "before_loop"):
                    self.before_loop()

                while True:
                    msg: Msg = self.queue.get()
                    if msg[0] == "END":
                        break
                    self.dispatch(msg)

                try:
                    while True:
                        self.queue.get_nowait()
                except Empty:
                    pass

                if hasattr(self, "after_loop"):
                    self.after_loop()

            def start(self):
                if hasattr(self, "before_start"):
                    self.before_start()

                self._start()

            def __lt__(self, other: BaseWorker):
                return self.queue.qsize() < other.queue.qsize()

            def __gt__(self, other: BaseWorker):
                return self.queue.qsize() > other.queue.qsize()

        return BaseWorker


@BaseThing
class Base:
    pass
