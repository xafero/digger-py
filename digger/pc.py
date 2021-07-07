import math

from alpha import Alpha
from cgagrafx import CgaGrafx
from systemx import SystemX


class Pc:

    def __init__(self, d):
        self.dig = d
        self.width = 320
        self.height = 200
        self.size = self.width * self.height
        self.pixels = []
        self.currentSource = None
        self.source = [None for _ in range(2)]
        self.pal = [[[0, 0x00, 0xAA, 0xAA], [0, 0xAA, 0x00, 0x54], [0, 0x00, 0x00, 0x00]],
                    [[0, 0x54, 0xFF, 0xFF], [0, 0xFF, 0x54, 0xFF], [0, 0x54, 0x54, 0x54]]]

    def gclear(self):
        i = 0
        while i < self.size:
            self.pixels[i] = 0
            i += 1
        self.currentSource.new_pixels_all()

    @staticmethod
    def gethrt():
        return SystemX.current_millis()

    @staticmethod
    def getkips():
        return 0

    def ggeti(self, x, y, p, w, h):

        src = 0
        dest = y * self.width + (x & 0xfffc)

        i = 0
        while i < h:
            d = dest
            j = 0
            while j < w:
                p[src] = ((((((self.pixels[d] << 2) | self.pixels[d + 1]) << 2) | self.pixels[d + 2]) << 2) |
                          self.pixels[d + 3])
                src += 1
                d += 4
                if src == len(p):
                    return
                j += 1
            dest += self.width
            i += 1

    def ggetpix(self, x, y):
        ofs = self.width * y + x & 0xfffc
        return (((((self.pixels[ofs] << 2) | self.pixels[ofs + 1]) << 2) | self.pixels[ofs + 2]) << 2) | self.pixels[
            ofs + 3]

    def ginit(self):
        pass

    def ginten(self, inten):
        self.currentSource = self.source[inten & 1]
        self.currentSource.new_pixels_all()

    def gpal(self, pal):
        pass

    def gputi2(self, x, y, p, w, h):
        self.gputi(x, y, p, w, h, 0)

    def gputi(self, x, y, p, w, h, _):

        src = 0
        dest = y * self.width + (x & 0xfffc)

        i = 0
        while i < h:
            d = dest
            j = 0
            while j < w:
                px = p[src]
                src += 1
                self.pixels[d + 3] = px & 3
                px >>= 2
                self.pixels[d + 2] = px & 3
                px >>= 2
                self.pixels[d + 1] = px & 3
                px >>= 2
                self.pixels[d] = px & 3
                d += 4
                if src == len(p):
                    return
                j += 1
            dest += self.width
            i += 1

    def gputim(self, x, y, ch, w, h):

        spr = CgaGrafx.cgatable[ch * 2]
        msk = CgaGrafx.cgatable[ch * 2 + 1]

        src = 0
        dest = y * self.width + (x & 0xfffc)

        i = 0
        while i < h:
            d = dest
            j = 0
            while j < w:
                px = spr[src]
                mx = msk[src]
                src += 1
                if (mx & 3) == 0:
                    self.pixels[d + 3] = px & 3
                px >>= 2
                if (mx & (3 << 2)) == 0:
                    self.pixels[d + 2] = px & 3
                px >>= 2
                if (mx & (3 << 4)) == 0:
                    self.pixels[d + 1] = px & 3
                px >>= 2
                if (mx & (3 << 6)) == 0:
                    self.pixels[d] = px & 3
                d += 4
                if src == len(spr) or src == len(msk):
                    return
                j += 1
            dest += self.width
            i += 1

    def gtitle(self):

        src = 0
        dest = 0

        while True:

            if src >= len(CgaGrafx.cgatitledat):
                break

            b = CgaGrafx.cgatitledat[src]
            src += 1

            if b == 0xfe:
                ll = CgaGrafx.cgatitledat[src]
                src += 1
                if ll == 0:
                    ll = 256
                c = CgaGrafx.cgatitledat[src]
                src += 1
            else:
                ll = 1
                c = b

            i = 0
            while i < ll:
                px = c
                if dest < 32768:
                    adst = (math.trunc(dest / float(320))) * 640 + dest % 320
                else:
                    adst = 320 + (math.trunc((dest - 32768) / float(320))) * 640 + (dest - 32768) % 320
                self.pixels[adst + 3] = px & 3
                px >>= 2
                self.pixels[adst + 2] = px & 3
                px >>= 2
                self.pixels[adst + 1] = px & 3
                px >>= 2
                self.pixels[adst + 0] = px & 3
                dest += 4
                if dest >= 65535:
                    break
                i += 1

            if dest >= 65535:
                break

    def gwrite(self, x, y, ch, c):
        self.gwrite2(x, y, ch, c, False)

    def gwrite2(self, x, y, ch, c, upd):

        dest = x + y * self.width
        ofs = 0
        color = c & 3

        ch -= 32
        if (ch < 0) or (ch > 0x5f):
            return

        chartab = Alpha.ascii2cga[ch]

        if chartab is None:
            return

        for i in range(12):
            d = dest
            for j in range(3):
                px = chartab[ofs]
                ofs += 1
                self.pixels[d + 3] = px & color
                px >>= 2
                self.pixels[d + 2] = px & color
                px >>= 2
                self.pixels[d + 1] = px & color
                px >>= 2
                self.pixels[d] = px & color
                d += 4
            dest += self.width

        if upd:
            self.currentSource.new_pixels(x, y, 12, 12)

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def get_pixels(self):
        return self.pixels

    def get_current_source(self):
        return self.currentSource
