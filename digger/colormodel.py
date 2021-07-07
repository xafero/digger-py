class IndexColorModel:
    def __init__(self, bits, size, red, green, blue):
        self._bits = bits
        self._size = size
        self._r = red
        self._g = green
        self._b = blue

    def get_color(self, index):
        r = self._r[index]
        g = self._g[index]
        b = self._b[index]
        return r, g, b
