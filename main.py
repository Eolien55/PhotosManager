from os import walk, name, system
from os.path import join, abspath
from .workers.managers import PhotosManager
from .clean import main_clean


def clear():

    # for windows
    if name == "nt":
        _ = system("cls")

    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system("clear")


def main(root):
    main_clean(root)
    manager = PhotosManager()
    manager.start()
    for dirname, _, files in walk(root):
        print(f"Doing '{dirname}'")
        for file in files:
            manager.send("new_file", join(abspath(dirname), file))
    manager.join()
    clear()
    print("Done!")
