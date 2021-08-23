from .employees import PhotoEmployee, CleanEmployee
from .base import BaseManager
from .secretaries import FilesSecretary


class PhotosManager(BaseManager):
    # Auto processed parameters
    name = "PhotosManager"
    target = PhotoEmployee
    target_args = 1
    muted = True
    secretary = FilesSecretary

    def handle_new_file(self, filename):
        least_used = self.least_used()

        least_used.send("new_file", filename)

    def handle_done_file(self):
        self.secretary.send("done_file")


class CleanManager(BaseManager):
    name = "CleanManager"
    target = CleanEmployee
    target_args = 1
    secretary = FilesSecretary
    muted = True

    def handle_new_file(self, filename):
        least_used = self.least_used()

        least_used.send("new_file", filename)

    def handle_done_file(self):
        self.secretary.send("done_file")
