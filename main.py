from os import walk, name, system
from os.path import join, abspath, abspath
from .workers.managers import PhotosManager
from .clean import main_clean
from sys import argv


def clear():

    # for windows
    if name == "nt":
        _ = system("cls")

    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system("clear")


def main(root):
    main_clean(root)
    manager = PhotosManager(root)
    manager.start()
    for dirname, _, files in walk(root):
        print(f"Doing '{dirname}'")
        for file in files:
            manager.send("new_file", join(abspath(dirname), file))
    manager.send("END")
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
