import gi
from main.main_sort import main

gi.require_version("Gtk", "3.0")

from gi.repository import Gtk


class AskYesNo(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(title="ATTENTION", transient_for=parent, flags=0)

        self.add_buttons(
            Gtk.STOCK_NO,
            False,
            Gtk.STOCK_YES,
            True,
        )

        self.set_default_size(150, 100)

        label = Gtk.Label(
            label="Cela détruira tous les fichiers qui ne sont pas des images. Voules-vous trier les photos de ce dossier ?"
        )

        box = self.get_content_area()
        box.add(label)
        self.show_all()


def choose_file(*args):
    dialog = Gtk.FileChooserDialog(
        title="Please choose a file",
        parent=window,
        action=Gtk.FileChooserAction.SELECT_FOLDER,
    )

    dialog.add_buttons(
        Gtk.STOCK_CANCEL,
        Gtk.ResponseType.CANCEL,
        Gtk.STOCK_OPEN,
        Gtk.ResponseType.OK,
    )

    response = dialog.run()
    if response == Gtk.ResponseType.OK:
        input_file.set_text(dialog.get_filename())
    elif response == Gtk.ResponseType.CANCEL:
        pass
    dialog.destroy()


def run(*args):
    dialog = AskYesNo(window)
    response = dialog.run()
    dialog.destroy()

    if response:
        global root

        root = input_file.get_text()
        Gtk.main_quit()


def show(title: str, text) -> None:
    """Function that displays a message with : a title, and a main text (title and text)"""
    title, text = str(title), str(text)
    dialog: Gtk.MessageDialog = Gtk.MessageDialog(
        transient_for=window,
        flags=0,
        message_type=Gtk.MessageType.INFO,
        buttons=Gtk.ButtonsType.OK,
        text=title,
    )
    dialog.format_secondary_text(text)
    dialog.run()

    dialog.destroy()


window = Gtk.Window()
window.set_title("Classeur de photos")
window.set_wmclass("Classeur de photos", "Classeur de photos")

window.set_default_size(300, 0)
window.set_resizable(False)

box = Gtk.Box(spacing=5, orientation=Gtk.Orientation.VERTICAL)
input_file = Gtk.Entry()
button_files = Gtk.Button(label="Sélectionner un dossier")
button_run = Gtk.Button(label="Démarrer")

input_file.set_halign(Gtk.Align.CENTER)
button_files.set_halign(Gtk.Align.CENTER)
button_run.set_halign(Gtk.Align.CENTER)

box.pack_start(input_file, False, False, 0)
box.pack_start(button_files, False, False, 0)
box.pack_start(button_run, False, False, 0)

window.add(box)

button_files.connect("clicked", choose_file)
button_run.connect("clicked", run)
window.connect("delete-event", Gtk.main_quit)

window.show_all()

Gtk.main()

main(root)
