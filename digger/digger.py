import math

# WARNING! This code is ugly and highly non-object-oriented.
# It was ported from C almost mechanically!
import threading

from bags import Bags
from drawing import Drawing
from input import Input
from main import Main
from monster import Monster
from pc import Pc
from scores import Scores
from sound import Sound
from sprite import Sprite
from systemx import SystemX
from colormodel import IndexColorModel
from compat import AppletCompat


class Digger:

    def __init__(self, pgtk):
        self.width = 320
        self.height = 200
        self.frametime = 66
        self.subaddr = ''
        self.gamethread = None
        self.Bags = Bags(self)
        self.Main = Main(self)
        self.Sound = Sound(self)
        self.Monster = Monster(self)
        self.Scores = Scores(self)
        self.Sprite = Sprite(self)
        self.Drawing = Drawing(self)
        self.Input = Input(self)
        self.Pc = Pc(self)
        self.diggerx = 0
        self.diggery = 0
        self.diggerh = 0
        self.diggerv = 0
        self.diggerrx = 0
        self.diggerry = 0
        self.digmdir = 0
        self.digdir = 0
        self.digtime = 0
        self.rechargetime = 0
        self.firex = 0
        self.firey = 0
        self.firedir = 0
        self.expsn = 0
        self.deathstage = 0
        self.deathbag = 0
        self.deathani = 0
        self.deathtime = 0
        self.startbonustimeleft = 0
        self.bonustimeleft = 0
        self.eatmsc = 0
        self.emocttime = 0
        self.emmask = 0
        self.emfield = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.digonscr = False
        self.notfiring = False
        self.bonusvisible = False
        self.bonusmode = False
        self.diggervisible = False
        self.time = 0
        self.ftime = 50
        self.embox = [8, 12, 12, 9, 16, 12, 6, 9]
        self.deatharc = [3, 5, 6, 6, 5, 3, 0]
        self.Pc.source = [None for _ in range(11)]
        self.factory = AppletCompat()
        self.pgtk = pgtk

    MAX_RATE = 200
    MIN_RATE = 40

    def checkdiggerunderbag(self, h, v):
        if self.digmdir == 2 or self.digmdir == 6:
            if math.trunc((self.diggerx - 12) / float(20)) == h:
                if math.trunc((self.diggery - 18) / float(18)) == v or math.trunc(
                        (self.diggery - 18) / float(18)) + 1 == v:
                    return True
        return False

    def countem(self):
        n = 0
        for x in range(15):
            for y in range(10):
                if (self.emfield[y * 15 + x] & self.emmask) != 0:
                    n += 1
        return n

    def createbonus(self):
        self.bonusvisible = True
        self.Drawing.drawbonus(292, 18)

    def destroy(self):
        if self.gamethread is not None:
            self.gamethread.stop()

    def diggerdie(self):
        if self.deathstage == 1:
            if self.Bags.bagy(self.deathbag) + 6 > self.diggery:
                self.diggery = self.Bags.bagy(self.deathbag) + 6
            self.Drawing.drawdigger(15, self.diggerx, self.diggery, False)
            self.Main.incpenalty()
            if self.Bags.getbagdir(self.deathbag) + 1 == 0:
                self.Sound.soundddie()
                self.deathtime = 5
                self.deathstage = 2
                self.deathani = 0
                self.diggery -= 6
        elif self.deathstage == 2:
            if self.deathtime != 0:
                self.deathtime -= 1
                return
            if self.deathani == 0:
                self.Sound.music(2)
            clbits = self.Drawing.drawdigger(14 - self.deathani, self.diggerx, self.diggery, False)
            self.Main.incpenalty()
            if self.deathani == 0 and ((clbits & 0x3f00) != 0):
                self.Monster.killmonsters(clbits)
            if self.deathani < 4:
                self.deathani += 1
                self.deathtime = 2
            else:
                self.deathstage = 4
                if self.Sound.musicflag:
                    self.deathtime = 60
                else:
                    self.deathtime = 10
        elif self.deathstage == 3:
            self.deathstage = 5
            self.deathani = 0
            self.deathtime = 0
        elif self.deathstage == 5:
            if 0 <= self.deathani <= 6:
                self.Drawing.drawdigger(15, self.diggerx, self.diggery - self.deatharc[self.deathani], False)
                if self.deathani == 6:
                    self.Sound.musicoff()
                self.Main.incpenalty()
                self.deathani += 1
                if self.deathani == 1:
                    self.Sound.soundddie()
                if self.deathani == 7:
                    self.deathtime = 5
                    self.deathani = 0
                    self.deathstage = 2
        elif self.deathstage == 4:
            if self.deathtime != 0:
                self.deathtime -= 1
            else:
                self.Main.setdead(True)

    def dodigger(self):
        self.newframe()
        if self.expsn != 0:
            self.drawexplosion()
        else:
            self.updatefire()
        if self.diggervisible:
            if self.digonscr:
                if self.digtime != 0:
                    self.Drawing.drawdigger(self.digmdir, self.diggerx, self.diggery,
                                            self.notfiring and self.rechargetime == 0)
                    self.Main.incpenalty()
                    self.digtime -= 1
                else:
                    self.updatedigger()
            else:
                self.diggerdie()
        if self.bonusmode and self.digonscr:
            if self.bonustimeleft != 0:
                self.bonustimeleft -= 1
                if self.startbonustimeleft != 0 or self.bonustimeleft < 20:
                    self.startbonustimeleft -= 1
                    if (self.bonustimeleft & 1) != 0:
                        self.Pc.ginten(0)
                        self.Sound.soundbonus()
                    else:
                        self.Pc.ginten(1)
                        self.Sound.soundbonus()
                    if self.startbonustimeleft == 0:
                        self.Sound.music(0)
                        self.Sound.soundbonusoff()
                        self.Pc.ginten(1)
            else:
                self.endbonusmode()
                self.Sound.soundbonusoff()
                self.Sound.music(1)
        if self.bonusmode and not self.digonscr:
            self.endbonusmode()
            self.Sound.soundbonusoff()
            self.Sound.music(1)
        if self.emocttime > 0:
            self.emocttime -= 1

    def drawemeralds(self):
        self.emmask = 1 << self.Main.getcplayer()
        for x in range(15):
            for y in range(10):
                if (self.emfield[y * 15 + x] & self.emmask) != 0:
                    self.Drawing.drawemerald(x * 20 + 12, y * 18 + 21)

    def drawexplosion(self):
        if self.expsn == 1:
            self.Sound.soundexplode()
        if (self.expsn == 1) or (self.expsn == 2) or (self.expsn == 3):
            self.Drawing.drawfire(self.firex, self.firey, self.expsn)
            self.Main.incpenalty()
            self.expsn += 1
        else:
            self.killfire()
            self.expsn = 0

    def endbonusmode(self):
        self.bonusmode = False
        self.Pc.ginten(0)

    def erasebonus(self):
        if self.bonusvisible:
            self.bonusvisible = False
            self.Sprite.erasespr(14)
        self.Pc.ginten(0)

    def erasedigger(self):
        self.Sprite.erasespr(0)
        self.diggervisible = False

    @staticmethod
    def get_applet_info():
        return "The Digger Remastered -- http://www.digger.org, Copyright (c) Andrew Jenner & Marek Futrega / MAF"

    def getfirepflag(self):
        return self.Input.firepflag

    def hitemerald(self, x, y, rx, ry, dirp):
        hit = False
        if dirp < 0 or dirp > 6 or ((dirp & 1) != 0):
            return hit
        if dirp == 0 and rx != 0:
            x += 1
        if dirp == 6 and ry != 0:
            y += 1
        if dirp == 0 or dirp == 4:
            r = rx
        else:
            r = ry
        if (self.emfield[y * 15 + x] & self.emmask) != 0:
            if r == self.embox[dirp]:
                self.Drawing.drawemerald(x * 20 + 12, y * 18 + 21)
                self.Main.incpenalty()
            if r == self.embox[dirp + 1]:
                self.Drawing.eraseemerald(x * 20 + 12, y * 18 + 21)
                self.Main.incpenalty()
                hit = True
                self.emfield[y * 15 + x] &= ~self.emmask
        return hit

    def init(self):

        if self.gamethread is not None:
            # self.gamethread.stop()
            pass

        self.subaddr = self.factory.get_submit_parameter()

        self.frametime = int(self.factory.get_speed_parameter())
        if self.frametime > self.MAX_RATE:
            self.frametime = self.MAX_RATE
        elif self.frametime < self.MIN_RATE:
            self.frametime = self.MIN_RATE

        self.Pc.pixels = [0 for _ in range(65536)]

        for i in range(2):
            model = IndexColorModel(8, 4, self.Pc.pal[i][0], self.Pc.pal[i][1], self.Pc.pal[i][2])
            self.Pc.source[i] = self.pgtk.create_refresher(self, model)
            self.Pc.source[i].set_animated(True)
            self.Pc.source[i].new_pixels_all()

        self.Pc.currentSource = self.Pc.source[0]

        self.gamethread = threading.Thread(daemon=True, target=self.run, args=())
        self.gamethread.start()

    def initbonusmode(self):
        self.bonusmode = True
        self.erasebonus()
        self.Pc.ginten(1)
        self.bonustimeleft = 250 - self.Main.levof10() * 20
        self.startbonustimeleft = 20
        self.eatmsc = 1

    def initdigger(self):
        self.diggerv = 9
        self.digmdir = 4
        self.diggerh = 7
        self.diggerx = self.diggerh * 20 + 12
        self.digdir = 0
        self.diggerrx = 0
        self.diggerry = 0
        self.digtime = 0
        self.digonscr = True
        self.deathstage = 1
        self.diggervisible = True
        self.diggery = self.diggerv * 18 + 18
        self.Sprite.movedrawspr(0, self.diggerx, self.diggery)
        self.notfiring = True
        self.emocttime = 0
        self.bonusvisible = self.bonusmode = False
        self.Input.firepressed = False
        self.expsn = 0
        self.rechargetime = 0

    def key_down(self, key):
        if key == 1006:
            self.Input.processkey(0x4b)
        elif key == 1007:
            self.Input.processkey(0x4d)
        elif key == 1004:
            self.Input.processkey(0x48)
        elif key == 1005:
            self.Input.processkey(0x50)
        elif key == 1008:
            self.Input.processkey(0x3b)
        else:
            key &= 0x7f
            if (key >= 65) and (key <= 90):
                key += (97 - 65)
            self.Input.processkey(key)
        return True

    def key_up(self, key):
        if key == 1006:
            self.Input.processkey(0xcb)
        elif key == 1007:
            self.Input.processkey(0xcd)
        elif key == 1004:
            self.Input.processkey(0xc8)
        elif key == 1005:
            self.Input.processkey(0xd0)
        elif key == 1008:
            self.Input.processkey(0xbb)
        else:
            key &= 0x7f
            if (key >= 65) and (key <= 90):
                key += (97 - 65)
            self.Input.processkey(0x80 | key)
        return True

    def killdigger(self, stage, bag):
        if self.deathstage < 2 or self.deathstage > 4:
            self.digonscr = False
            self.deathstage = stage
            self.deathbag = bag

    def killemerald(self, x, y):
        if (self.emfield[y * 15 + x + 15] & self.emmask) != 0:
            self.emfield[y * 15 + x + 15] &= ~self.emmask
            self.Drawing.eraseemerald(x * 20 + 12, (y + 1) * 18 + 21)

    def killfire(self):
        if not self.notfiring:
            self.notfiring = True
            self.Sprite.erasespr(15)
            self.Sound.soundfireoff()

    def makeemfield(self):
        self.emmask = 1 << self.Main.getcplayer()
        for x in range(15):
            for y in range(10):
                if self.Main.getlevch(x, y, self.Main.levplan()) == 'C':
                    self.emfield[y * 15 + x] |= self.emmask
                else:
                    self.emfield[y * 15 + x] &= ~self.emmask

    def newframe(self):
        self.Input.checkkeyb()
        self.time += self.frametime
        wait = self.time - self.Pc.gethrt()
        if wait > 0:
            SystemX.sleep(wait)
        self.Pc.currentSource.new_pixels_all()

    @staticmethod
    def reversedir(dirp):
        if dirp == 0:
            return 4
        if (dirp == 0) or (dirp == 4):
            return 0
        if (dirp == 0) or (dirp == 4) or (dirp == 2):
            return 6
        if (dirp == 0) or (dirp == 4) or (dirp == 2) or (dirp == 6):
            return 2
        return dirp

    def run(self):
        self.Main.main()

    def start(self):
        self.factory.request_focus()

    def updatedigger(self):
        push = False
        self.Input.readdir()
        dirp = self.Input.getdir()
        if dirp == 0 or dirp == 2 or dirp == 4 or dirp == 6:
            ddir = dirp
        else:
            ddir = -1
        if self.diggerrx == 0 and (ddir == 2 or ddir == 6):
            self.digdir = self.digmdir = ddir
        if self.diggerry == 0 and (ddir == 4 or ddir == 0):
            self.digdir = self.digmdir = ddir
        if dirp == -1:
            self.digmdir = -1
        else:
            self.digmdir = self.digdir
        if (self.diggerx == 292 and self.digmdir == 0) or (self.diggerx == 12 and self.digmdir == 4) or (
                self.diggery == 180 and self.digmdir == 6) or (self.diggery == 18 and self.digmdir == 2):
            self.digmdir = -1
        diggerox = self.diggerx
        diggeroy = self.diggery
        if self.digmdir != -1:
            self.Drawing.eatfield(diggerox, diggeroy, self.digmdir)
        if self.digmdir == 0:
            self.Drawing.drawrightblob(self.diggerx, self.diggery)
            self.diggerx += 4
        elif self.digmdir == 4:
            self.Drawing.drawleftblob(self.diggerx, self.diggery)
            self.diggerx -= 4
        elif self.digmdir == 2:
            self.Drawing.drawtopblob(self.diggerx, self.diggery)
            self.diggery -= 3
        elif self.digmdir == 6:
            self.Drawing.drawbottomblob(self.diggerx, self.diggery)
            self.diggery += 3
        if self.hitemerald(math.trunc((self.diggerx - 12) / 20), math.trunc((self.diggery - 18) / 18),
                           (self.diggerx - 12) % 20, (self.diggery - 18) % 18, self.digmdir):
            self.Scores.scoreemerald()
            self.Sound.soundem()
            self.Sound.soundemerald(self.emocttime)
            self.emocttime = 9
        clbits = self.Drawing.drawdigger(self.digdir, self.diggerx, self.diggery,
                                         self.notfiring and self.rechargetime == 0)
        self.Main.incpenalty()
        if (self.Bags.bagbits() & clbits) != 0:
            if self.digmdir == 0 or self.digmdir == 4:
                push = self.Bags.pushbags(self.digmdir, clbits)
                self.digtime += 1
            else:
                if not self.Bags.pushudbags(clbits):
                    push = False
            if not push:
                self.diggerx = diggerox
                self.diggery = diggeroy
                self.Drawing.drawdigger(self.digmdir, self.diggerx, self.diggery,
                                        self.notfiring and self.rechargetime == 0)
                self.Main.incpenalty()
                self.digdir = self.reversedir(self.digmdir)
        if ((clbits & 0x3f00) != 0) and self.bonusmode:
            nmon = self.Monster.killmonsters(clbits)
            while nmon != 0:
                self.Sound.soundeatm()
                self.Scores.scoreeatm()
                nmon -= 1
        if (clbits & 0x4000) != 0:
            self.Scores.scorebonus()
            self.initbonusmode()
        self.diggerh = math.trunc((self.diggerx - 12) / 20)
        self.diggerrx = (self.diggerx - 12) % 20
        self.diggerv = math.trunc((self.diggery - 18) / 18)
        self.diggerry = (self.diggery - 18) % 18

    def updatefire(self):
        pix = 0
        if self.notfiring:
            if self.rechargetime != 0:
                self.rechargetime -= 1
            else:
                if self.getfirepflag():
                    if self.digonscr:
                        self.rechargetime = self.Main.levof10() * 3 + 60
                        self.notfiring = False
                        if self.digdir == 0:
                            self.firex = self.diggerx + 8
                            self.firey = self.diggery + 4
                        elif self.digdir == 4:
                            self.firex = self.diggerx
                            self.firey = self.diggery + 4
                        elif self.digdir == 2:
                            self.firex = self.diggerx + 4
                            self.firey = self.diggery
                        elif self.digdir == 6:
                            self.firex = self.diggerx + 4
                            self.firey = self.diggery + 8
                        self.firedir = self.digdir
                        self.Sprite.movedrawspr(15, self.firex, self.firey)
                        self.Sound.soundfire()
        else:
            if self.firedir == 0:
                self.firex += 8
                pix = self.Pc.ggetpix(self.firex, self.firey + 4) | self.Pc.ggetpix(self.firex + 4, self.firey + 4)
            elif self.firedir == 4:
                self.firex -= 8
                pix = self.Pc.ggetpix(self.firex, self.firey + 4) | self.Pc.ggetpix(self.firex + 4, self.firey + 4)
            elif self.firedir == 2:
                self.firey -= 7
                pix = (self.Pc.ggetpix(self.firex + 4, self.firey) | self.Pc.ggetpix(self.firex + 4,
                                                                                     self.firey + 1) | self.Pc.ggetpix(
                    self.firex + 4,
                    self.firey + 2) | self.Pc.ggetpix(
                    self.firex + 4, self.firey + 3) | self.Pc.ggetpix(self.firex + 4, self.firey + 4) | self.Pc.ggetpix(
                    self.firex + 4,
                    self.firey + 5) | self.Pc.ggetpix(
                    self.firex + 4, self.firey + 6)) & 0xc0
            elif self.firedir == 6:
                self.firey += 7
                pix = (self.Pc.ggetpix(self.firex, self.firey) | self.Pc.ggetpix(self.firex,
                                                                                 self.firey + 1) | self.Pc.ggetpix(
                    self.firex,
                    self.firey + 2) | self.Pc.ggetpix(
                    self.firex, self.firey + 3) | self.Pc.ggetpix(self.firex, self.firey + 4) | self.Pc.ggetpix(
                    self.firex, self.firey + 5) | self.Pc.ggetpix(
                    self.firex,
                    self.firey + 6)) & 3
            clbits = self.Drawing.drawfire(self.firex, self.firey, 0)
            self.Main.incpenalty()
            if (clbits & 0x3f00) != 0:
                mon = 0
                b = 256
                while mon < 6:
                    if (clbits & b) != 0:
                        self.Monster.killmon(mon)
                        self.Scores.scorekill()
                        self.expsn = 1
                    mon += 1
                    b <<= 1
            if (clbits & 0x40fe) != 0:
                self.expsn = 1
            if self.firedir == 0:
                if self.firex > 296:
                    self.expsn = 1
                else:
                    if pix != 0 and clbits == 0:
                        self.expsn = 1
                        self.firex -= 8
                        self.Drawing.drawfire(self.firex, self.firey, 0)
            elif self.firedir == 4:
                if self.firex < 16:
                    self.expsn = 1
                else:
                    if pix != 0 and clbits == 0:
                        self.expsn = 1
                        self.firex += 8
                        self.Drawing.drawfire(self.firex, self.firey, 0)
            elif self.firedir == 2:
                if self.firey < 15:
                    self.expsn = 1
                else:
                    if pix != 0 and clbits == 0:
                        self.expsn = 1
                        self.firey += 7
                        self.Drawing.drawfire(self.firex, self.firey, 0)
            elif self.firedir == 6:
                if self.firey > 183:
                    self.expsn = 1
                else:
                    if pix != 0 and clbits == 0:
                        self.expsn = 1
                        self.firey -= 7
                        self.Drawing.drawfire(self.firex, self.firey, 0)

    def get_pc(self):
        return self.Pc
