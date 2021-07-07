class Sprite:

    def __init__(self, d):
        self.dig = d
        self.retrflag = True
        self.sprrdrwf = [False, False, False, False, False, False, False, False, False, False, False, False, False,
                         False, False, False, False]
        self.sprrecf = [False, False, False, False, False, False, False, False, False, False, False, False, False,
                        False, False, False, False]
        self.sprenf = [False, False, False, False, False, False, False, False, False, False, False, False, False, False,
                       False, False]
        self.sprch = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.sprmov = [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        self.sprx = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.spry = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.sprwid = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.sprhei = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.sprbwid = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.sprbhei = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.sprnch = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.sprnwid = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.sprnhei = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.sprnbwid = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.sprnbhei = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.defsprorder = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
        self.sprorder = self.defsprorder

    def bcollide(self, bx, si):
        if self.sprx[bx] >= self.sprx[si]:
            if self.sprx[bx] + self.sprbwid[bx] > self.sprwid[si] * 4 + self.sprx[si] - self.sprbwid[si] - 1:
                return False
        else:
            if self.sprx[si] + self.sprbwid[si] > self.sprwid[bx] * 4 + self.sprx[bx] - self.sprbwid[bx] - 1:
                return False
        if self.spry[bx] >= self.spry[si]:
            if self.spry[bx] + self.sprbhei[bx] <= self.sprhei[si] + self.spry[si] - self.sprbhei[si] - 1:
                return True
            return False
        if self.spry[si] + self.sprbhei[si] <= self.sprhei[bx] + self.spry[bx] - self.sprbhei[bx] - 1:
            return True
        return False

    def bcollides(self, bx):
        si = bx
        ax = 0
        dx = 0
        bx = 0
        condition = True
        while condition:
            if self.sprenf[bx] and bx != si:
                if self.bcollide(bx, si):
                    ax |= 1 << dx
                self.sprx[bx] += 320
                self.spry[bx] -= 2
                if self.bcollide(bx, si):
                    ax |= 1 << dx
                self.sprx[bx] -= 640
                self.spry[bx] += 4
                if self.bcollide(bx, si):
                    ax |= 1 << dx
                self.sprx[bx] += 320
                self.spry[bx] -= 2
            bx += 1
            dx += 1
            condition = dx != 16
        return ax

    def clearrdrwf(self):
        self.clearrecf()
        for i in range(17):
            self.sprrdrwf[i] = False

    def clearrecf(self):
        for i in range(17):
            self.sprrecf[i] = False

    def collide(self, bx, si):
        if self.sprx[bx] >= self.sprx[si]:
            if self.sprx[bx] > self.sprwid[si] * 4 + self.sprx[si] - 1:
                return False
        else:
            if self.sprx[si] > self.sprwid[bx] * 4 + self.sprx[bx] - 1:
                return False
        if self.spry[bx] >= self.spry[si]:
            if self.spry[bx] <= self.sprhei[si] + self.spry[si] - 1:
                return True
            return False
        if self.spry[si] <= self.sprhei[bx] + self.spry[bx] - 1:
            return True
        return False

    def createspr(self, n, ch, mov, wid, hei, bwid, bhei):
        self.sprnch[n & 15] = self.sprch[n & 15] = ch
        self.sprmov[n & 15] = mov
        self.sprnwid[n & 15] = self.sprwid[n & 15] = wid
        self.sprnhei[n & 15] = self.sprhei[n & 15] = hei
        self.sprnbwid[n & 15] = self.sprbwid[n & 15] = bwid
        self.sprnbhei[n & 15] = self.sprbhei[n & 15] = bhei
        self.sprenf[n & 15] = False

    def drawmiscspr(self, x, y, ch, wid, hei):
        self.sprx[16] = x & -4
        self.spry[16] = y
        self.sprch[16] = ch
        self.sprwid[16] = wid
        self.sprhei[16] = hei
        self.dig.Pc.gputim(self.sprx[16], self.spry[16], self.sprch[16], self.sprwid[16], self.sprhei[16])

    def drawspr(self, n, x, y):
        bx = n & 15
        x &= -4
        self.clearrdrwf()
        self.setrdrwflgs(bx)
        t1 = self.sprx[bx]
        t2 = self.spry[bx]
        t3 = self.sprwid[bx]
        t4 = self.sprhei[bx]
        self.sprx[bx] = x
        self.spry[bx] = y
        self.sprwid[bx] = self.sprnwid[bx]
        self.sprhei[bx] = self.sprnhei[bx]
        self.clearrecf()
        self.setrdrwflgs(bx)
        self.sprhei[bx] = t4
        self.sprwid[bx] = t3
        self.spry[bx] = t2
        self.sprx[bx] = t1
        self.sprrdrwf[bx] = True
        self.putis()
        self.sprx[bx] = x
        self.spry[bx] = y
        self.sprch[bx] = self.sprnch[bx]
        self.sprwid[bx] = self.sprnwid[bx]
        self.sprhei[bx] = self.sprnhei[bx]
        self.sprbwid[bx] = self.sprnbwid[bx]
        self.sprbhei[bx] = self.sprnbhei[bx]
        self.dig.Pc.ggeti(self.sprx[bx], self.spry[bx], self.sprmov[bx], self.sprwid[bx], self.sprhei[bx])
        self.putims()
        return self.bcollides(bx)

    def erasespr(self, n):
        bx = n & 15
        self.dig.Pc.gputi(self.sprx[bx], self.spry[bx], self.sprmov[bx], self.sprwid[bx], self.sprhei[bx], True)
        self.sprenf[bx] = False
        self.clearrdrwf()
        self.setrdrwflgs(bx)
        self.putims()

    def getis(self):
        for i in range(16):
            if self.sprrdrwf[i]:
                self.dig.Pc.ggeti(self.sprx[i], self.spry[i], self.sprmov[i], self.sprwid[i], self.sprhei[i])
        self.putims()

    def initmiscspr(self, x, y, wid, hei):
        self.sprx[16] = x
        self.spry[16] = y
        self.sprwid[16] = wid
        self.sprhei[16] = hei
        self.clearrdrwf()
        self.setrdrwflgs(16)
        self.putis()

    def initspr(self, n, ch, wid, hei, bwid, bhei):
        self.sprnch[n & 15] = ch
        self.sprnwid[n & 15] = wid
        self.sprnhei[n & 15] = hei
        self.sprnbwid[n & 15] = bwid
        self.sprnbhei[n & 15] = bhei

    def movedrawspr(self, n, x, y):
        bx = n & 15
        self.sprx[bx] = x & -4
        self.spry[bx] = y
        self.sprch[bx] = self.sprnch[bx]
        self.sprwid[bx] = self.sprnwid[bx]
        self.sprhei[bx] = self.sprnhei[bx]
        self.sprbwid[bx] = self.sprnbwid[bx]
        self.sprbhei[bx] = self.sprnbhei[bx]
        self.clearrdrwf()
        self.setrdrwflgs(bx)
        self.putis()
        self.dig.Pc.ggeti(self.sprx[bx], self.spry[bx], self.sprmov[bx], self.sprwid[bx], self.sprhei[bx])
        self.sprenf[bx] = True
        self.sprrdrwf[bx] = True
        self.putims()
        return self.bcollides(bx)

    def putims(self):
        for i in range(16):
            j = self.sprorder[i]
            if self.sprrdrwf[j]:
                self.dig.Pc.gputim(self.sprx[j], self.spry[j], self.sprch[j], self.sprwid[j], self.sprhei[j])

    def putis(self):
        for i in range(16):
            if self.sprrdrwf[i]:
                self.dig.Pc.gputi2(self.sprx[i], self.spry[i], self.sprmov[i], self.sprwid[i], self.sprhei[i])

    def setrdrwflgs(self, n):
        if not self.sprrecf[n]:
            self.sprrecf[n] = True
            for i in range(16):
                if self.sprenf[i] and i != n:
                    if self.collide(i, n):
                        self.sprrdrwf[i] = True
                        self.setrdrwflgs(i)
                    self.sprx[i] += 320
                    self.spry[i] -= 2
                    if self.collide(i, n):
                        self.sprrdrwf[i] = True
                        self.setrdrwflgs(i)
                    self.sprx[i] -= 640
                    self.spry[i] += 4
                    if self.collide(i, n):
                        self.sprrdrwf[i] = True
                        self.setrdrwflgs(i)
                    self.sprx[i] += 320
                    self.spry[i] -= 2

    def setretr(self, f):
        self.retrflag = f

    def setsprorder(self, newsprorder):
        if newsprorder is None:
            self.sprorder = self.defsprorder
        else:
            self.sprorder = newsprorder
