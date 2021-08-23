import os
from sys import argv
from workers import CleanManager


def main_clean(root):
    manager = CleanManager(root)
    manager.start()
    for dirpath, _, files in os.walk(root):
        for file in files:
            manager.send("new_file", os.path.join(os.path.abspath(dirpath), file))
    manager.join()
    print("\n\n")
    print("Done cleaning!")


if __name__ == "__main__":
    if len(argv) < 2:
        root = os.path.abspath(".")
    else:
        root = os.path.abspath(argv[1])
    while (
        res := input(
            "THIS WILL BREAK ALL THE ORGANISATION MADE IN {}. ARE YOU OKAY WITH THIS ? [Y/N] ".format(
                root
            )
        ).upper()
    ) not in ("Y", "N"):
        pass
    if res == "Y":
        main_clean(root)
