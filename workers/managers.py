from .employees import PhotoEmployee, CleanEmployee
from .base.manager import BaseManager


class PhotosManager(BaseManager):
    name = "PhotosManager"
    target = PhotoEmployee
    target_args = 1

    def handle_new_file(self, filename):
        least_used = self.least_used()

        least_used.send("new_file", filename)


class CleanManager(BaseManager):
    name = "CleanManager"
    target = CleanEmployee
    target_args = 1

    def handle_new_file(self, filename):
        least_used = self.least_used()

        least_used.send("new_file", filename)
