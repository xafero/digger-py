import math


class Drawing:

    def __init__(self, d):
        self.dig = d
        self.field1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.field2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.field = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                      0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                      0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                      0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                      0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.diggerbuf = [0 for _ in range(480)]
        self.bagbuf1 = [0 for _ in range(480)]
        self.bagbuf2 = [0 for _ in range(480)]
        self.bagbuf3 = [0 for _ in range(480)]
        self.bagbuf4 = [0 for _ in range(480)]
        self.bagbuf5 = [0 for _ in range(480)]
        self.bagbuf6 = [0 for _ in range(480)]
        self.bagbuf7 = [0 for _ in range(480)]
        self.monbuf1 = [0 for _ in range(480)]
        self.monbuf2 = [0 for _ in range(480)]
        self.monbuf3 = [0 for _ in range(480)]
        self.monbuf4 = [0 for _ in range(480)]
        self.monbuf5 = [0 for _ in range(480)]
        self.monbuf6 = [0 for _ in range(480)]
        self.bonusbuf = [0 for _ in range(480)]
        self.firebuf = [0 for _ in range(128)]
        self.bitmasks = [0xfffe, 0xfffd, 0xfffb, 0xfff7, 0xffef, 0xffdf, 0xffbf, 0xff7f, 0xfeff, 0xfdff, 0xfbff, 0xf7ff]
        self.monspr = [0, 0, 0, 0, 0, 0]
        self.monspd = [0, 0, 0, 0, 0, 0]
        self.digspr = 0
        self.digspd = 0
        self.firespr = 0
        self.fireheight = 8

    def createdbfspr(self):
        self.digspd = 1
        self.digspr = 0
        self.firespr = 0
        self.dig.Sprite.createspr(0, 0, self.diggerbuf, 4, 15, 0, 0)
        self.dig.Sprite.createspr(14, 81, self.bonusbuf, 4, 15, 0, 0)
        self.dig.Sprite.createspr(15, 82, self.firebuf, 2, self.fireheight, 0, 0)

    def creatembspr(self):
        self.dig.Sprite.createspr(1, 62, self.bagbuf1, 4, 15, 0, 0)
        self.dig.Sprite.createspr(2, 62, self.bagbuf2, 4, 15, 0, 0)
        self.dig.Sprite.createspr(3, 62, self.bagbuf3, 4, 15, 0, 0)
        self.dig.Sprite.createspr(4, 62, self.bagbuf4, 4, 15, 0, 0)
        self.dig.Sprite.createspr(5, 62, self.bagbuf5, 4, 15, 0, 0)
        self.dig.Sprite.createspr(6, 62, self.bagbuf6, 4, 15, 0, 0)
        self.dig.Sprite.createspr(7, 62, self.bagbuf7, 4, 15, 0, 0)
        self.dig.Sprite.createspr(8, 71, self.monbuf1, 4, 15, 0, 0)
        self.dig.Sprite.createspr(9, 71, self.monbuf2, 4, 15, 0, 0)
        self.dig.Sprite.createspr(10, 71, self.monbuf3, 4, 15, 0, 0)
        self.dig.Sprite.createspr(11, 71, self.monbuf4, 4, 15, 0, 0)
        self.dig.Sprite.createspr(12, 71, self.monbuf5, 4, 15, 0, 0)
        self.dig.Sprite.createspr(13, 71, self.monbuf6, 4, 15, 0, 0)
        self.createdbfspr()
        for i in range(6):
            self.monspr[i] = 0
            self.monspd[i] = 1

    def drawbackg(self, ll):
        for y in range(14, 200, 4):
            for x in range(0, 320, 20):
                self.dig.Sprite.drawmiscspr(x, y, 93 + ll, 5, 4)

    def drawbonus(self, x, y):
        self.dig.Sprite.initspr(14, 81, 4, 15, 0, 0)
        self.dig.Sprite.movedrawspr(14, x, y)

    def drawbottomblob(self, x, y):
        self.dig.Sprite.initmiscspr(x - 4, y + 15, 6, 6)
        self.dig.Sprite.drawmiscspr(x - 4, y + 15, 105, 6, 6)
        self.dig.Sprite.getis()

    def drawdigger(self, t, x, y, f):
        self.digspr += self.digspd
        if self.digspr == 2 or self.digspr == 0:
            self.digspd = -self.digspd
        if self.digspr > 2:
            self.digspr = 2
        if self.digspr < 0:
            self.digspr = 0
        if 0 <= t <= 6 and not ((t & 1) != 0):
            self.dig.Sprite.initspr(0, (t + (0 if f else 1)) * 3 + self.digspr + 1, 4, 15, 0, 0)
            return self.dig.Sprite.drawspr(0, x, y)
        if 10 <= t <= 15:
            self.dig.Sprite.initspr(0, 40 - t, 4, 15, 0, 0)
            return self.dig.Sprite.drawspr(0, x, y)
        return 0

    def drawemerald(self, x, y):
        self.dig.Sprite.initmiscspr(x, y, 4, 10)
        self.dig.Sprite.drawmiscspr(x, y, 108, 4, 10)
        self.dig.Sprite.getis()

    def drawfield(self):
        for x in range(15):
            for y in range(10):
                if (self.field[y * 15 + x] & 0x2000) == 0:
                    xp = x * 20 + 12
                    yp = y * 18 + 18
                    if (self.field[y * 15 + x] & 0xfc0) != 0xfc0:
                        self.field[y * 15 + x] &= 0xd03f
                        self.drawbottomblob(xp, yp - 15)
                        self.drawbottomblob(xp, yp - 12)
                        self.drawbottomblob(xp, yp - 9)
                        self.drawbottomblob(xp, yp - 6)
                        self.drawbottomblob(xp, yp - 3)
                        self.drawtopblob(xp, yp + 3)
                    if (self.field[y * 15 + x] & 0x1f) != 0x1f:
                        self.field[y * 15 + x] &= 0xdfe0
                        self.drawrightblob(xp - 16, yp)
                        self.drawrightblob(xp - 12, yp)
                        self.drawrightblob(xp - 8, yp)
                        self.drawrightblob(xp - 4, yp)
                        self.drawleftblob(xp + 4, yp)
                    if x < 14:
                        if (self.field[y * 15 + x + 1] & 0xfdf) != 0xfdf:
                            self.drawrightblob(xp, yp)
                    if y < 9:
                        if (self.field[(y + 1) * 15 + x] & 0xfdf) != 0xfdf:
                            self.drawbottomblob(xp, yp)

    def drawfire(self, x, y, t):
        if t == 0:
            self.firespr += 1
            if self.firespr > 2:
                self.firespr = 0
            self.dig.Sprite.initspr(15, 82 + self.firespr, 2, self.fireheight, 0, 0)
        else:
            self.dig.Sprite.initspr(15, 84 + t, 2, self.fireheight, 0, 0)
        return self.dig.Sprite.drawspr(15, x, y)

    def drawfurryblob(self, x, y):
        self.dig.Sprite.initmiscspr(x - 4, y + 15, 6, 8)
        self.dig.Sprite.drawmiscspr(x - 4, y + 15, 107, 6, 8)
        self.dig.Sprite.getis()

    def drawgold(self, n, t, x, y):
        self.dig.Sprite.initspr(n, t + 62, 4, 15, 0, 0)
        return self.dig.Sprite.drawspr(n, x, y)

    def drawleftblob(self, x, y):
        self.dig.Sprite.initmiscspr(x - 8, y - 1, 2, 18)
        self.dig.Sprite.drawmiscspr(x - 8, y - 1, 104, 2, 18)
        self.dig.Sprite.getis()

    def drawlife(self, t, x, y):
        self.dig.Sprite.drawmiscspr(x, y, t + 110, 4, 12)

    def drawlives(self):
        n = self.dig.Main.getlives(1) - 1
        for ll in range(1, 5):
            self.drawlife(0 if n > 0 else 2, ll * 20 + 60, 0)
            n -= 1
        if self.dig.Main.nplayers == 2:
            n = self.dig.Main.getlives(2) - 1
            for ll in range(1, 5):
                self.drawlife(1 if n > 0 else 2, 244 - ll * 20, 0)
                n -= 1

    def drawmon(self, n, nobf, dirp, x, y):
        self.monspr[n] += self.monspd[n]
        if self.monspr[n] == 2 or self.monspr[n] == 0:
            self.monspd[n] = -self.monspd[n]
        if self.monspr[n] > 2:
            self.monspr[n] = 2
        if self.monspr[n] < 0:
            self.monspr[n] = 0
        if nobf:
            self.dig.Sprite.initspr(n + 8, self.monspr[n] + 69, 4, 15, 0, 0)
        else:
            if dirp == 0:
                self.dig.Sprite.initspr(n + 8, self.monspr[n] + 73, 4, 15, 0, 0)
            elif dirp == 4:
                self.dig.Sprite.initspr(n + 8, self.monspr[n] + 77, 4, 15, 0, 0)
        return self.dig.Sprite.drawspr(n + 8, x, y)

    def drawmondie(self, n, nobf, dirp, x, y):
        if nobf:
            self.dig.Sprite.initspr(n + 8, 72, 4, 15, 0, 0)
        else:
            if dirp == 0:
                self.dig.Sprite.initspr(n + 8, 76, 4, 15, 0, 0)
            elif dirp == 4:
                self.dig.Sprite.initspr(n + 8, 80, 4, 14, 0, 0)
        return self.dig.Sprite.drawspr(n + 8, x, y)

    def drawrightblob(self, x, y):
        self.dig.Sprite.initmiscspr(x + 16, y - 1, 2, 18)
        self.dig.Sprite.drawmiscspr(x + 16, y - 1, 102, 2, 18)
        self.dig.Sprite.getis()

    def drawsquareblob(self, x, y):
        self.dig.Sprite.initmiscspr(x - 4, y + 17, 6, 6)
        self.dig.Sprite.drawmiscspr(x - 4, y + 17, 106, 6, 6)
        self.dig.Sprite.getis()

    def drawstatics(self):
        for x in range(15):
            for y in range(10):
                if self.dig.Main.getcplayer() == 0:
                    self.field[y * 15 + x] = self.field1[y * 15 + x]
                else:
                    self.field[y * 15 + x] = self.field2[y * 15 + x]
        self.dig.Sprite.setretr(True)
        self.dig.Pc.gpal(0)
        self.dig.Pc.ginten(0)
        self.drawbackg(self.dig.Main.levplan())
        self.drawfield()
        self.dig.Pc.currentSource.new_pixels(0, 0, self.dig.Pc.width, self.dig.Pc.height)

    def drawtopblob(self, x, y):
        self.dig.Sprite.initmiscspr(x - 4, y - 6, 6, 6)
        self.dig.Sprite.drawmiscspr(x - 4, y - 6, 103, 6, 6)
        self.dig.Sprite.getis()

    def eatfield(self, x, y, dirp):
        h = math.trunc((x - 12) / float(20))
        xr = math.trunc(((x - 12) % 20) / float(4))
        v = math.trunc((y - 18) / float(18))
        yr = math.trunc(((y - 18) % 18) / float(3))
        self.dig.Main.incpenalty()
        if dirp == 0:
            h += 1
            self.field[v * 15 + h] &= self.bitmasks[xr]
            if (self.field[v * 15 + h] & 0x1f) != 0:
                return
            self.field[v * 15 + h] &= 0xdfff
        elif dirp == 4:
            xr -= 1
            if xr < 0:
                xr += 5
                h -= 1
            self.field[v * 15 + h] &= self.bitmasks[xr]
            if (self.field[v * 15 + h] & 0x1f) != 0:
                return
            self.field[v * 15 + h] &= 0xdfff
        elif dirp == 2:
            yr -= 1
            if yr < 0:
                yr += 6
                v -= 1
            self.field[v * 15 + h] &= self.bitmasks[6 + yr]
            if (self.field[v * 15 + h] & 0xfc0) != 0:
                return
            self.field[v * 15 + h] &= 0xdfff
        elif dirp == 6:
            v += 1
            self.field[v * 15 + h] &= self.bitmasks[6 + yr]
            if (self.field[v * 15 + h] & 0xfc0) != 0:
                return
            self.field[v * 15 + h] &= 0xdfff

    def eraseemerald(self, x, y):
        self.dig.Sprite.initmiscspr(x, y, 4, 10)
        self.dig.Sprite.drawmiscspr(x, y, 109, 4, 10)
        self.dig.Sprite.getis()

    def initdbfspr(self):
        self.digspd = 1
        self.digspr = 0
        self.firespr = 0
        self.dig.Sprite.initspr(0, 0, 4, 15, 0, 0)
        self.dig.Sprite.initspr(14, 81, 4, 15, 0, 0)
        self.dig.Sprite.initspr(15, 82, 2, self.fireheight, 0, 0)

    def initmbspr(self):
        self.dig.Sprite.initspr(1, 62, 4, 15, 0, 0)
        self.dig.Sprite.initspr(2, 62, 4, 15, 0, 0)
        self.dig.Sprite.initspr(3, 62, 4, 15, 0, 0)
        self.dig.Sprite.initspr(4, 62, 4, 15, 0, 0)
        self.dig.Sprite.initspr(5, 62, 4, 15, 0, 0)
        self.dig.Sprite.initspr(6, 62, 4, 15, 0, 0)
        self.dig.Sprite.initspr(7, 62, 4, 15, 0, 0)
        self.dig.Sprite.initspr(8, 71, 4, 15, 0, 0)
        self.dig.Sprite.initspr(9, 71, 4, 15, 0, 0)
        self.dig.Sprite.initspr(10, 71, 4, 15, 0, 0)
        self.dig.Sprite.initspr(11, 71, 4, 15, 0, 0)
        self.dig.Sprite.initspr(12, 71, 4, 15, 0, 0)
        self.dig.Sprite.initspr(13, 71, 4, 15, 0, 0)
        self.initdbfspr()

    def makefield(self):
        for x in range(15):
            for y in range(10):
                self.field[y * 15 + x] = -1
                c = self.dig.Main.getlevch(x, y, self.dig.Main.levplan())
                if c == 'S' or c == 'V':
                    self.field[y * 15 + x] &= 0xd03f
                if c == 'S' or c == 'H':
                    self.field[y * 15 + x] &= 0xdfe0
                if self.dig.Main.getcplayer() == 0:
                    self.field1[y * 15 + x] = self.field[y * 15 + x]
                else:
                    self.field2[y * 15 + x] = self.field[y * 15 + x]

    def outtext2(self, p, x, y, c):
        self.outtext(p, x, y, c, False)

    def outtext(self, p, x, y, c, b):
        rx = x
        i = 0
        while i < len(p):
            self.dig.Pc.gwrite(x, y, ord(p[i]), c)
            x += 12
            i += 1
        if b:
            self.dig.Pc.currentSource.new_pixels(rx, y, len(p) * 12, 12)

    def savefield(self):
        for x in range(15):
            for y in range(10):
                if self.dig.Main.getcplayer() == 0:
                    self.field1[y * 15 + x] = self.field[y * 15 + x]
                else:
                    self.field2[y * 15 + x] = self.field[y * 15 + x]
