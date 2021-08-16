import os
from .workers.managers import CleanManager
from sys import argv


def main_clean(root):
    manager = CleanManager(root)
    manager.start()
    for dirpath, _, files in os.walk(root):
        for file in files:
            manager.send("new_file", os.path.join(os.path.abspath(dirpath), file))
    manager.send("END")
    manager.join()
    print("Done!")


if __name__ == "__main__":
    if len(argv) < 2:
        root = os.path.abspath(".")
    else:
        root = os.path.abspath(argv[1])
    main_clean(root)
