import gi

from refresher import GtkRefresher

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class GtkDigger(Gtk.DrawingArea):
    def __init__(self, digger):
        super().__init__()
        self._digger = digger
        super().connect("draw", self.on_drawn)

    def set_focusable(self, param):
        pass

    def on_drawn(self, _, g):
        # width = da.get_allocated_width()
        # height = da.get_allocated_height()

        g.set_source_rgb(0, 0, 0)
        g.rectangle(0, 0, 3840, 2160)
        g.fill()

        g.scale(4, 4)

        pc = self._digger.get_pc()

        w = pc.get_width()
        h = pc.get_height()
        data = pc.get_pixels()
        model = pc.get_current_source().Model

        shift = 1

        for x in range(w):
            for y in range(h):
                array_index = y * w + x
                (sr, sg, sb) = model.get_color(data[array_index])
                g.set_source_rgb(sr, sg, sb)
                g.rectangle(x + shift, y + shift, 1, 1)
                g.fill()

        return False

    def do_key_up(self, key):
        return self._digger.key_up(key)

    def do_key_down(self, key):
        return self._digger.key_down(key)

    def create_refresher(self, _, model):
        return GtkRefresher(self, model)
