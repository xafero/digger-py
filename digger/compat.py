class AppletCompat:
    @staticmethod
    def get_submit_parameter():
        return ""

    @staticmethod
    def get_speed_parameter():
        return 66

    def create_image(self, param):
        pass

    def request_focus(self):
        pass

    def set_focusable(self, value):
        pass

    def on_key_pressevent(self, e):
        num = self.convert_to_legacy(e.Key)
        if num >= 0:
            return self.on_key_pressevent(num)

    def on_key_releaseevent(self, e):
        num = self.convert_to_legacy(e.Key)
        if num >= 0:
            return self.on_key_releaseevent(num)

    @staticmethod
    def convert_to_legacy(net_code):
        switcher = {
            "Left": 1006,
            "leftarrow": 1006,
            "Right": 1007,
            "rightarrow": 1007,
            "Up": 1004,
            "uparrow": 1004,
            "Down": 1005,
            "downarrow": 1005,
            "F1": 1008,
            "F10": 1021,
            "plus": 1031,
            "minus": 1032
        }
        got = switcher.get(net_code, -1)
        if got == -1:
            got = ord(net_code)
        return got
