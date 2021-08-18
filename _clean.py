import os
from .workers import CleanManager


def main_clean(root):
    manager = CleanManager(root)
    manager.start()
    for dirpath, _, files in os.walk(root):
        for file in files:
            manager.send("new_file", os.path.join(os.path.abspath(dirpath), file))
    manager.join()
    print("Done cleaning!")
