from .base import BaseSecretary
from .helpers import countfiles
from os import get_terminal_size


class FilesSecretary(BaseSecretary):
    def __init__(self, root, *args, **kwgs):
        super().__init__(*args, **kwgs)

        self.files_to_do = countfiles(root)
        if not self.files_to_do:
            self.files_to_do = 1

            self.files_done = 1
        else:
            self.files_done = 0

    def get_text_to_write(
        self,
        numerator=1,
        denominator=1,
        nofill=" ",
        fill="#",
        prefix="Progress :",
        suffix="Complete",
        usepercent=True,
        decimals=1,
    ):
        fraction = numerator / denominator
        if usepercent:
            percents_text = (" {0:." + str(decimals) + "f} ").format(fraction * 100)
        else:
            percents_text = " "

        columns, _ = get_terminal_size()
        if not columns:
            columns = 100

        length = (
            columns - 2 - len(prefix) - 2 - 2 - len(percents_text) - len(suffix) - 2
        )

        filled = fill * (round(fraction * length)) + nofill * (
            length - round(fraction * length)
        )

        return "\r  {} |{}|{}{}  ".format(prefix, filled, percents_text, suffix)

    def before_loop(self):
        print()
        print(self.get_text_to_write(self.files_done, self.files_to_do), end="")

    def handle_done_file(self):
        self.files_done += 1
        print(self.get_text_to_write(self.files_done, self.files_to_do), end="")
        if self.files_done == self.files_to_do:
            self.parent.send("END")
