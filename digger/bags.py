import math

from bagdata import BagData


class Bags:

    def __init__(self, d):
        self.dig = d
        self.bagdat1 = [BagData(), BagData(), BagData(), BagData(), BagData(), BagData(), BagData(), BagData()]
        self.bagdat2 = [BagData(), BagData(), BagData(), BagData(), BagData(), BagData(), BagData(), BagData()]
        self.bagdat = [BagData(), BagData(), BagData(), BagData(), BagData(), BagData(), BagData(), BagData()]
        self.pushcount = 0
        self.goldtime = 0
        self.wblanim = [2, 0, 1, 0]

    def bagbits(self):
        bags = 0
        bag = 1
        b = 2
        while bag < 8:
            if self.bagdat[bag].exist:
                bags |= b
            bag += 1
            b <<= 1
        return bags

    def baghitground(self, bag):
        if self.bagdat[bag].dir == 6 and self.bagdat[bag].fallh > 1:
            self.bagdat[bag].gt = 1
        else:
            self.bagdat[bag].fallh = 0
        self.bagdat[bag].dir = -1
        self.bagdat[bag].wt = 15
        self.bagdat[bag].wobbling = False
        clbits = self.dig.Drawing.drawgold(bag, 0, self.bagdat[bag].x, self.bagdat[bag].y)
        self.dig.Main.incpenalty()
        bn = 1
        b = 2
        while bn < 8:
            if (b & clbits) != 0:
                self.removebag(bn)
            bn += 1
            b <<= 1

    def bagy(self, bag):
        return self.bagdat[bag].y

    def cleanupbags(self):
        self.dig.Sound.soundfalloff()
        for bpa in range(1, 7):
            if self.bagdat[bpa].exist and (
                    (self.bagdat[bpa].h == 7 and self.bagdat[bpa].v == 9) or self.bagdat[bpa].xr != 0 or
                    self.bagdat[bpa].yr != 0 or self.bagdat[bpa].gt != 0 or self.bagdat[bpa].fallh != 0 or
                    self.bagdat[bpa].wobbling):
                self.bagdat[bpa].exist = False
                self.dig.Sprite.erasespr(bpa)
            if self.dig.Main.getcplayer() == 0:
                self.bagdat1[bpa].copy_from(self.bagdat[bpa])
            else:
                self.bagdat2[bpa].copy_from(self.bagdat[bpa])

    def dobags(self):
        soundfalloffflag = True
        soundwobbleoffflag = True
        for bag in range(1, 7):
            if self.bagdat[bag].exist:
                if self.bagdat[bag].gt != 0:
                    if self.bagdat[bag].gt == 1:
                        self.dig.Sound.soundbreak()
                        self.dig.Drawing.drawgold(bag, 4, self.bagdat[bag].x, self.bagdat[bag].y)
                        self.dig.Main.incpenalty()
                    if self.bagdat[bag].gt == 3:
                        self.dig.Drawing.drawgold(bag, 5, self.bagdat[bag].x, self.bagdat[bag].y)
                        self.dig.Main.incpenalty()
                    if self.bagdat[bag].gt == 5:
                        self.dig.Drawing.drawgold(bag, 6, self.bagdat[bag].x, self.bagdat[bag].y)
                        self.dig.Main.incpenalty()
                    self.bagdat[bag].gt += 1
                    if self.bagdat[bag].gt == self.goldtime:
                        self.removebag(bag)
                    else:
                        if self.bagdat[bag].v < 9 and self.bagdat[bag].gt < self.goldtime - 10:
                            if (self.dig.Monster.getfield(self.bagdat[bag].h, self.bagdat[bag].v + 1) & 0x2000) == 0:
                                self.bagdat[bag].gt = self.goldtime - 10
                else:
                    self.updatebag(bag)
        for bag in range(1, 7):
            if self.bagdat[bag].dir == 6 and self.bagdat[bag].exist:
                soundfalloffflag = False
            if self.bagdat[bag].dir != 6 and self.bagdat[bag].wobbling and self.bagdat[bag].exist:
                soundwobbleoffflag = False
        if soundfalloffflag:
            self.dig.Sound.soundfalloff()
        if soundwobbleoffflag:
            self.dig.Sound.soundwobbleoff()

    def drawbags(self):
        for bag in range(1, 7):
            if self.dig.Main.getcplayer() == 0:
                self.bagdat[bag].copy_from(self.bagdat1[bag])
            else:
                self.bagdat[bag].copy_from(self.bagdat2[bag])
            if self.bagdat[bag].exist:
                self.dig.Sprite.movedrawspr(bag, self.bagdat[bag].x, self.bagdat[bag].y)

    def getbagdir(self, bag):
        if self.bagdat[bag].exist:
            return self.bagdat[bag].dir
        return -1

    def getgold(self, bag):
        clbits = self.dig.Drawing.drawgold(bag, 6, self.bagdat[bag].x, self.bagdat[bag].y)
        self.dig.Main.incpenalty()
        if (clbits & 1) != 0:
            self.dig.Scores.scoregold()
            self.dig.Sound.soundgold()
            self.dig.digtime = 0
        else:
            self.dig.Monster.mongold()
        self.removebag(bag)

    def getnmovingbags(self):
        n = 0
        for bag in range(1, 7):
            if self.bagdat[bag].exist and self.bagdat[bag].gt < 10 and (
                    self.bagdat[bag].gt != 0 or self.bagdat[bag].wobbling):
                n += 1
        return n

    def initbags(self):
        self.pushcount = 0
        self.goldtime = 150 - self.dig.Main.levof10() * 10
        for bag in range(1, 7):
            self.bagdat[bag].exist = False
        bag = 1
        for x in range(15):
            for y in range(10):
                if self.dig.Main.getlevch(x, y, self.dig.Main.levplan()) == 'B':
                    if bag < 8:
                        self.bagdat[bag].exist = True
                        self.bagdat[bag].gt = 0
                        self.bagdat[bag].fallh = 0
                        self.bagdat[bag].dir = -1
                        self.bagdat[bag].wobbling = False
                        self.bagdat[bag].wt = 15
                        self.bagdat[bag].unfallen = True
                        self.bagdat[bag].x = x * 20 + 12
                        self.bagdat[bag].y = y * 18 + 18
                        self.bagdat[bag].h = x
                        self.bagdat[bag].v = y
                        self.bagdat[bag].xr = 0
                        self.bagdat[bag].yr = 0
                        bag += 1
        if self.dig.Main.getcplayer() == 0:
            for i in range(1, 7):
                self.bagdat1[i].copy_from(self.bagdat[i])
        else:
            for i in range(1, 7):
                self.bagdat2[i].copy_from(self.bagdat[i])

    def pushbag(self, bag, dirp):
        push = True
        ox = x = self.bagdat[bag].x
        oy = y = self.bagdat[bag].y
        h = self.bagdat[bag].h
        v = self.bagdat[bag].v
        if self.bagdat[bag].gt != 0:
            self.getgold(bag)
            return True
        if self.bagdat[bag].dir == 6 and (dirp == 4 or dirp == 0):
            clbits = self.dig.Drawing.drawgold(bag, 3, x, y)
            self.dig.Main.incpenalty()
            if ((clbits & 1) != 0) and (self.dig.diggery >= y):
                self.dig.killdigger(1, bag)
            if (clbits & 0x3f00) != 0:
                self.dig.Monster.squashmonsters(bag, clbits)
            return True
        if (x == 292 and dirp == 0) or (x == 12 and dirp == 4) or (y == 180 and dirp == 6) or (y == 18 and dirp == 2):
            push = False
        if push:
            if dirp == 0:
                x += 4
            elif dirp == 4:
                x -= 4
            elif dirp == 6:
                if self.bagdat[bag].unfallen:
                    self.bagdat[bag].unfallen = False
                    self.dig.Drawing.drawsquareblob(x, y)
                    self.dig.Drawing.drawtopblob(x, y + 21)
                else:
                    self.dig.Drawing.drawfurryblob(x, y)
                self.dig.Drawing.eatfield(x, y, dirp)
                self.dig.killemerald(h, v)
                y += 6
            if dirp == 6:
                clbits = self.dig.Drawing.drawgold(bag, 3, x, y)
                self.dig.Main.incpenalty()
                if ((clbits & 1) != 0) and self.dig.diggery >= y:
                    self.dig.killdigger(1, bag)
                if (clbits & 0x3f00) != 0:
                    self.dig.Monster.squashmonsters(bag, clbits)
            elif (dirp == 0) or (dirp == 4):
                self.bagdat[bag].wt = 15
                self.bagdat[bag].wobbling = False
                clbits = self.dig.Drawing.drawgold(bag, 0, x, y)
                self.dig.Main.incpenalty()
                self.pushcount = 1
                if (clbits & 0xfe) != 0:
                    if not self.pushbags(dirp, clbits):
                        x = ox
                        y = oy
                        self.dig.Drawing.drawgold(bag, 0, ox, oy)
                        self.dig.Main.incpenalty()
                        push = False
                if ((clbits & 1) != 0) or ((clbits & 0x3f00) != 0):
                    x = ox
                    y = oy
                    self.dig.Drawing.drawgold(bag, 0, ox, oy)
                    self.dig.Main.incpenalty()
                    push = False
            if push:
                self.bagdat[bag].dir = dirp
            else:
                self.bagdat[bag].dir = self.dig.reversedir(dirp)
            self.bagdat[bag].x = x
            self.bagdat[bag].y = y
            self.bagdat[bag].h = math.trunc((x - 12) / float(20))
            self.bagdat[bag].v = math.trunc((y - 18) / float(18))
            self.bagdat[bag].xr = (x - 12) % 20
            self.bagdat[bag].yr = (y - 18) % 18
        return push

    def pushbags(self, dirp, bits):
        push = True
        bag = 1
        bit = 2
        while bag < 8:
            if (bits & bit) != 0:
                if not self.pushbag(bag, dirp):
                    push = False
            bag += 1
            bit <<= 1
        return push

    def pushudbags(self, bits):
        push = True
        bag = 1
        b = 2
        while bag < 8:
            if (bits & b) != 0:
                if self.bagdat[bag].gt != 0:
                    self.getgold(bag)
                else:
                    push = False
            bag += 1
            b <<= 1
        return push

    def removebag(self, bag):
        if self.bagdat[bag].exist:
            self.bagdat[bag].exist = False
            self.dig.Sprite.erasespr(bag)

    def removebags(self, bits):
        bag = 1
        b = 2
        while bag < 8:
            if self.bagdat[bag].exist and ((bits & b) != 0):
                self.removebag(bag)
            bag += 1
            b <<= 1

    def updatebag(self, bag):
        x = self.bagdat[bag].x
        h = self.bagdat[bag].h
        xr = self.bagdat[bag].xr
        y = self.bagdat[bag].y
        v = self.bagdat[bag].v
        yr = self.bagdat[bag].yr
        if self.bagdat[bag].dir == -1:
            if y < 180 and xr == 0:
                if self.bagdat[bag].wobbling:
                    if self.bagdat[bag].wt == 0:
                        self.bagdat[bag].dir = 6
                        self.dig.Sound.soundfall()
                        self.updatebag_broken(bag)
                        return
                    self.bagdat[bag].wt -= 1
                    wbl = self.bagdat[bag].wt % 8
                    if not ((wbl & 1) != 0):
                        self.dig.Drawing.drawgold(bag, self.wblanim[wbl >> 1], x, y)
                        self.dig.Main.incpenalty()
                        self.dig.Sound.soundwobble()
                else:
                    if (self.dig.Monster.getfield(h, v + 1) & 0xfdf) != 0xfdf:
                        if not self.dig.checkdiggerunderbag(h, v + 1):
                            self.bagdat[bag].wobbling = True
            else:
                self.bagdat[bag].wt = 15
                self.bagdat[bag].wobbling = False
        elif (self.bagdat[bag].dir == 0) or (self.bagdat[bag].dir == 4):
            if xr == 0:
                if y < 180 and (self.dig.Monster.getfield(h, v + 1) & 0xfdf) != 0xfdf:
                    self.bagdat[bag].dir = 6
                    self.bagdat[bag].wt = 0
                    self.dig.Sound.soundfall()
                else:
                    self.baghitground(bag)
        elif self.bagdat[bag].dir == 6:
            if yr == 0:
                self.bagdat[bag].fallh += 1
            if y >= 180:
                self.baghitground(bag)
            else:
                if (self.dig.Monster.getfield(h, v + 1) & 0xfdf) == 0xfdf:
                    if yr == 0:
                        self.baghitground(bag)
            self.dig.Monster.checkmonscared(self.bagdat[bag].h)
        self.updatebag_broken(bag)

    def updatebag_broken(self, bag):
        if self.bagdat[bag].dir != -1:
            if self.bagdat[bag].dir != 6 and self.pushcount != 0:
                self.pushcount -= 1
            else:
                self.pushbag(bag, self.bagdat[bag].dir)
