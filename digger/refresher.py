import gi

gi.require_version("Gtk", "3.0")
from gi.repository import GLib


class GtkRefresher:
    def __init__(self, area, model):
        self._area = area
        self.Model = model

    def get_model(self):
        return self.Model

    def new_pixels(self, x, y, w, h):
        a = self._area

        def handle():
            a.queue_draw_area(x, y, w, h)

        GLib.timeout_add(0, handle)

    def new_pixels_all(self):
        a = self._area

        def handle():
            a.queue_draw()

        GLib.timeout_add(0, handle)

    def get_color(self, index):
        return self.Model.get_color(index)

    def set_animated(self, val):
        pass
