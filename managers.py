from employees import PhotoEmployee, CleanEmployee
from base.manager import BaseManager


class PhotosManager(BaseManager):
    target = PhotoEmployee

    def after_loop(self):
        self.send_all("EOF")

    def handle_new_file(self, filename):
        less_used = self.less_used()

        less_used.send("new_file", filename)


class CleanManager(BaseManager):
    target = CleanEmployee

    def __init__(self, root, *args, **kwgs):
        super().__init__(*args, **kwgs)

        self.root = root

    def handle_new_file(self, filename):
        less_used = self.less_used()

        less_used.send("new_file", filename)
