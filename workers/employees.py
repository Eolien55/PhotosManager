from .helpers import photo_employee_job
import exiftool
from os.path import join, basename, exists
from shutil import move
from os import listdir, makedirs
from .base import BaseEmployee


class ExifEmployee:
    name = "ExifEmployee"

    def __init__(self):
        self.et = exiftool.ExifTool()
        self.et.__enter__()

    def end(self):
        self.et.__exit__(0, 0, 0)

    def get_metadata(self, filename):
        return self.et.get_metadata(filename)


class PhotoEmployee(BaseEmployee):
    name = "PhotoEmployee"

    def __init__(self, root, *args, **kwgs):
        super().__init__(*args, **kwgs)

        self.root = root

    def before_loop(self):
        self.exif_employee = ExifEmployee()

    def after_loop(self):
        self.exif_employee.end()

    def get_exif(self, filename):
        return self.exif_employee.get_metadata(filename)

    def handle_new_file(self, filename):
        photo_employee_job(self.root, filename, self.get_exif, self.process_id)
        self.parent.send("done_file")


class CleanEmployee(BaseEmployee):
    name = "CleanEmployee"

    def __init__(self, root, *args, **kwgs):
        super().__init__(*args, **kwgs)

        self.root = root
        if not exists(join(root, str(self.process_id))):
            makedirs(join(root, str(self.process_id)))

    def handle_new_file(self, filename):
        move(
            filename,
            join(
                self.root,
                str(self.process_id),
                str(len(listdir(join(self.root, str(self.process_id)))) + 1),
            )
            + (
                "." + basename(filename).split(".")[-1]
                if "." in basename(filename)
                else ""
            ),
        )
        self.parent.send("done_file")
