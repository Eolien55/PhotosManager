from photos import photo_employee_job
import exiftool
import os
from base.employee import BaseEmployee


class ExifEmployee:
    def __init__(self):
        self.et = exiftool.ExifTool()
        self.et.__enter__()

    def end(self):
        self.et.__exit__(0, 0, 0)

    def get_metadata(self, filename):
        return self.et.get_metadata(filename)


class PhotoEmployee(BaseEmployee):
    def before_loop(self):
        self.exif_employee = ExifEmployee()
        self.exif_employee.start()

    def after_loop(self):
        self.exif_employee.end()

    def get_exif(self, filename):
        return self.exif_employee.get_metadata(filename)

    def handle_new_file(self, filename):
        photo_employee_job(self.root, filename, self.get_exif)


class CleanEmployee(BaseEmployee):
    def before_loop(self):
        self.root

    def handle_new_file(self, filename):
        pass
