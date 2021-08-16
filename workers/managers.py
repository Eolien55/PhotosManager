from .employees import PhotoEmployee, CleanEmployee
from .base.manager import BaseManager


class PhotosManager(BaseManager):
    target = PhotoEmployee
    target_args = 0

    def handle_new_file(self, filename):
        less_used = self.least_used()

        less_used.send("new_file", filename)


class CleanManager(BaseManager):
    target = CleanEmployee
    target_args = 1

    def __init__(self, root, *args, **kwgs):
        super().__init__(root, *args, **kwgs)

        self.root = root

    def handle_new_file(self, filename):
        least_used = self.least_used()

        least_used.send("new_file", filename)
