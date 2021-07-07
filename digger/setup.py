from gi.repository import Gdk

from compat import AppletCompat


class Setup:
    @staticmethod
    def create_on_keypress(d):
        def func(_, ev):
            key_event = Gdk.keyval_name(ev.keyval)
            num = AppletCompat.convert_to_legacy(key_event)
            if num >= 0:
                d.key_down(num)

        return func

    @staticmethod
    def create_on_keyrelease(d):
        def func(_, ev):
            key_event = Gdk.keyval_name(ev.keyval)
            num = AppletCompat.convert_to_legacy(key_event)
            if num >= 0:
                d.key_up(num)

        return func
