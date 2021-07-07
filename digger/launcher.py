import gi

from digger import Digger
from gtkdig import GtkDigger
from setup import Setup

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

if __name__ == '__main__':
    pgtk = GtkDigger(None)
    game = Digger(pgtk)
    pgtk.set_focusable(True)
    game.init()
    game.start()

    frame = Gtk.Window()
    frame.set_title("Digger Remastered")
    frame.connect("destroy", Gtk.main_quit)
    frame.set_size_request(game.width * 4.03, game.height * 4.15)
    frame.set_position(Gtk.WindowPosition.CENTER)

    icon = "./res/icons/digger.png"
    frame.set_icon_from_file(icon)

    pgtk._digger = game
    frame.add(pgtk)
    frame.show_all()

    frame.connect("key-press-event", Setup.create_on_keypress(game))
    frame.connect("key-release-event", Setup.create_on_keyrelease(game))

    Gtk.main()
