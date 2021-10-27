from os.path import abspath, abspath
from os import walk, name, system
from os.path import join, abspath, abspath
from workers import PhotosManager
from clean import main_clean
from sys import argv
from multiprocessing import Lock
import time


def clear():

    # for windows
    if name == "nt":
        _ = system("cls")

    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system("clear")


def main(root):
    main_clean(root)
    lock = Lock()
    manager = PhotosManager(root, lock)
    manager.start()
    for dirname, _, files in walk(root):
        for file in files:
            manager.send("new_file", join(abspath(dirname), file))
    time.sleep(5)
    manager.join()
    clear()
    print("Done!")


if __name__ == "__main__":
    if len(argv) < 2:
        root = abspath(".")
    else:
        root = abspath(argv[1])
    while (
        res := input(
            "THIS WILL BREAK ALL THE ORGANISATION MADE IN {}. ARE YOU OKAY WITH THIS ? [Y/N] ".format(
                root
            )
        ).upper()
    ) not in ("Y", "N"):
        pass
    if res == "Y":
        main(root)
