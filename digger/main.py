import math

from gamedata import GameData
from systemx import SystemX


class Main:

    def __init__(self, d):
        self.dig = d
        self.digsprorder = [14, 13, 7, 6, 5, 4, 3, 2, 1, 12, 11, 10, 9, 8, 15, 0]
        self.gamedat = [GameData(), GameData()]
        self.pldispbuf = ""
        self.curplayer = 0
        self.nplayers = 0
        self.penalty = 0
        self.levnotdrawn = False
        self.flashplayer = False
        self.levfflag = False
        self.biosflag = False
        self.speedmul = 40
        self.delaytime = 0
        self.randv = 0
        self.leveldat = [["S   B     HHHHS", "V  CC  C  V B  ", "VB CC  C  V    ", "V  CCB CB V CCC", "V  CC  C  V CCC",
                          "HH CC  C  V CCC", " V    B B V    ", " HHHH     V    ", "C   V     V   C",
                          "CC  HHHHHHH  CC"],
                         ["SHHHHH  B B  HS", " CC  V       V ", " CC  V CCCCC V ", "BCCB V CCCCC V ", "CCCC V       V ",
                          "CCCC V B  HHHH ", " CC  V CC V    ", " BB  VCCCCV CC ", "C    V CC V CC ",
                          "CC   HHHHHH    "],
                         ["SHHHHB B BHHHHS", "CC  V C C V BB ", "C   V C C V CC ", " BB V C C VCCCC", "CCCCV C C VCCCC",
                          "CCCCHHHHHHH CC ", " CC  C V C  CC ", " CC  C V C     ", "C    C V C    C",
                          "CC   C H C   CC"],
                         ["SHBCCCCBCCCCBHS", "CV  CCCCCCC  VC", "CHHH CCCCC HHHC", "C  V  CCC  V  C", "   HHH C HHH   ",
                          "  B  V B V  B  ", "  C  VCCCV  C  ", " CCC HHHHH CCC ", "CCCCC CVC CCCCC",
                          "CCCCC CHC CCCCC"],
                         ["SHHHHHHHHHHHHHS", "VBCCCCBVCCCCCCV", "VCCCCCCV CCBC V", "V CCCC VCCBCCCV", "VCCCCCCV CCCC V",
                          "V CCCC VBCCCCCV", "VCCBCCCV CCCC V", "V CCBC VCCCCCCV", "VCCCCCCVCCCCCCV",
                          "HHHHHHHHHHHHHHH"],
                         ["SHHHHHHHHHHHHHS", "VCBCCV V VCCBCV", "VCCC VBVBV CCCV", "VCCCHH V HHCCCV", "VCC V CVC V CCV",
                          "VCCHH CVC HHCCV", "VC V CCVCC V CV", "VCHHBCCVCCBHHCV", "VCVCCCCVCCCCVCV",
                          "HHHHHHHHHHHHHHH"],
                         ["SHCCCCCVCCCCCHS", " VCBCBCVCBCBCV ", "BVCCCCCVCCCCCVB", "CHHCCCCVCCCCHHC", "CCV CCCVCCC VCC",
                          "CCHHHCCVCCHHHCC", "CCCCV CVC VCCCC", "CCCCHH V HHCCCC", "CCCCCV V VCCCCC",
                          "CCCCCHHHHHCCCCC"],
                         ["HHHHHHHHHHHHHHS", "V CCBCCCCCBCC V", "HHHCCCCBCCCCHHH", "VBV CCCCCCC VBV", "VCHHHCCCCCHHHCV",
                          "VCCBV CCC VBCCV", "VCCCHHHCHHHCCCV", "VCCCC V V CCCCV", "VCCCCCV VCCCCCV",
                          "HHHHHHHHHHHHHHH"]]

        self.dig = d

    def addlife(self, pl):
        self.gamedat[pl - 1].lives += 1
        self.dig.Sound.sound1up()

    def calibrate(self):
        self.dig.Sound.volume = math.trunc((self.dig.Pc.getkips() / 291))
        if self.dig.Sound.volume == 0:
            self.dig.Sound.volume = 1

    def checklevdone(self):
        if (self.dig.countem() == 0 or self.dig.Monster.monleft() == 0) and self.dig.digonscr:
            self.gamedat[self.curplayer].levdone = True
        else:
            self.gamedat[self.curplayer].levdone = False

    def cleartopline(self):
        self.dig.Drawing.outtext2("                          ", 0, 0, 3)
        self.dig.Drawing.outtext2(" ", 308, 0, 3)

    def drawscreen(self):
        self.dig.Drawing.creatembspr()
        self.dig.Drawing.drawstatics()
        self.dig.Bags.drawbags()
        self.dig.drawemeralds()
        self.dig.initdigger()
        self.dig.Monster.initmonsters()

    def getcplayer(self):
        return self.curplayer

    def getlevch(self, x, y, ll):
        if ll == 0:
            ll += 1
        return self.leveldat[ll - 1][y][x]

    def getlives(self, pl):
        return self.gamedat[pl - 1].lives

    def incpenalty(self):
        self.penalty += 1

    def initchars(self):
        self.dig.Drawing.initmbspr()
        self.dig.initdigger()
        self.dig.Monster.initmonsters()

    def initlevel(self):
        self.gamedat[self.curplayer].levdone = False
        self.dig.Drawing.makefield()
        self.dig.makeemfield()
        self.dig.Bags.initbags()
        self.levnotdrawn = True

    def levno(self):
        cur_play = self.gamedat[self.curplayer]
        lvl_no = cur_play.level
        return lvl_no

    def levof10(self):
        if self.gamedat[self.curplayer].level > 10:
            return 10
        return self.gamedat[self.curplayer].level

    def levplan(self):
        ll = self.levno()
        if ll > 8:
            ll = (ll & 3) + 5  # Level plan: 12345678, 678, (5678) 247 times, 5 forever
        return ll

    def main(self):
        x = 0

        self.randv = int(self.dig.Pc.gethrt())
        self.calibrate()

        self.dig.ftime = self.speedmul * 2000
        self.dig.Sprite.setretr(False)
        self.dig.Pc.ginit()
        self.dig.Sprite.setretr(True)
        self.dig.Pc.gpal(0)
        self.dig.Input.initkeyb()
        self.dig.Input.detectjoy()
        self.dig.Scores.loadscores()
        self.dig.Sound.initsound()

        self.dig.Scores.init()
        self.dig.Scores.updatescores(self.dig.Scores.scores)

        self.nplayers = 1
        condition = True
        while condition:
            self.dig.Sound.soundstop()
            self.dig.Sprite.setsprorder(self.digsprorder)
            self.dig.Drawing.creatembspr()
            self.dig.Input.detectjoy()
            self.dig.Pc.gclear()
            self.dig.Pc.gtitle()
            self.dig.Drawing.outtext2("D I G G E R", 100, 0, 3)
            self.shownplayers()
            self.dig.Scores.showtable()
            start = False
            frame = 0

            self.dig.time = self.dig.Pc.gethrt()

            while not start:
                start = self.dig.Input.teststart()
                if self.dig.Input.akeypressed == 27:
                    self.switchnplayers()
                    self.shownplayers()
                    self.dig.Input.akeypressed = 0
                    self.dig.Input.keypressed = 0
                if frame == 0:
                    for t in range(54, 173, 12):
                        self.dig.Drawing.outtext2("            ", 164, t, 0)
                if frame == 50:
                    self.dig.Sprite.movedrawspr(8, 292, 63)
                    x = 292
                if 50 < frame <= 77:
                    x -= 4
                    self.dig.Drawing.drawmon(0, True, 4, x, 63)
                if frame > 77:
                    self.dig.Drawing.drawmon(0, True, 0, 184, 63)
                if frame == 83:
                    self.dig.Drawing.outtext2("NOBBIN", 216, 64, 2)
                if frame == 90:
                    self.dig.Sprite.movedrawspr(9, 292, 82)
                    self.dig.Drawing.drawmon(1, False, 4, 292, 82)
                    x = 292
                if 90 < frame <= 117:
                    x -= 4
                    self.dig.Drawing.drawmon(1, False, 4, x, 82)
                if frame > 117:
                    self.dig.Drawing.drawmon(1, False, 0, 184, 82)
                if frame == 123:
                    self.dig.Drawing.outtext2("HOBBIN", 216, 83, 2)
                if frame == 130:
                    self.dig.Sprite.movedrawspr(0, 292, 101)
                    self.dig.Drawing.drawdigger(4, 292, 101, True)
                    x = 292
                if 130 < frame <= 157:
                    x -= 4
                    self.dig.Drawing.drawdigger(4, x, 101, True)
                if frame > 157:
                    self.dig.Drawing.drawdigger(0, 184, 101, True)
                if frame == 163:
                    self.dig.Drawing.outtext2("DIGGER", 216, 102, 2)
                if frame == 178:
                    self.dig.Sprite.movedrawspr(1, 184, 120)
                    self.dig.Drawing.drawgold(1, 0, 184, 120)
                if frame == 183:
                    self.dig.Drawing.outtext2("GOLD", 216, 121, 2)
                if frame == 198:
                    self.dig.Drawing.drawemerald(184, 141)
                if frame == 203:
                    self.dig.Drawing.outtext2("EMERALD", 216, 140, 2)
                if frame == 218:
                    self.dig.Drawing.drawbonus(184, 158)
                if frame == 223:
                    self.dig.Drawing.outtext2("BONUS", 216, 159, 2)
                self.dig.newframe()
                frame += 1
                if frame > 250:
                    frame = 0

            self.gamedat[0].level = 1
            self.gamedat[0].lives = 3
            if self.nplayers == 2:
                self.gamedat[1].level = 1
                self.gamedat[1].lives = 3
            else:
                self.gamedat[1].lives = 0
            self.dig.Pc.gclear()
            self.curplayer = 0
            self.initlevel()
            self.curplayer = 1
            self.initlevel()
            self.dig.Scores.zeroscores()
            self.dig.bonusvisible = True
            if self.nplayers == 2:
                self.flashplayer = True
            self.curplayer = 0

            while (self.gamedat[0].lives != 0 or self.gamedat[1].lives != 0) and not self.dig.Input.escape:
                self.gamedat[self.curplayer].dead = False
                while (not self.gamedat[self.curplayer].dead) and \
                        self.gamedat[self.curplayer].lives != 0 and not self.dig.Input.escape:
                    self.dig.Drawing.initmbspr()
                    self.play()
                if self.gamedat[1 - self.curplayer].lives != 0:
                    self.curplayer = 1 - self.curplayer
                    self.flashplayer = self.levnotdrawn = True
            self.dig.Input.escape = False
            condition = not False

    def play(self):
        if self.levnotdrawn:
            self.levnotdrawn = False
            self.drawscreen()
            self.dig.time = self.dig.Pc.gethrt()
            if self.flashplayer:
                self.flashplayer = False
                self.pldispbuf = "PLAYER "
                if self.curplayer == 0:
                    self.pldispbuf += "1"
                else:
                    self.pldispbuf += "2"
                self.cleartopline()
                for t in range(15):
                    for c in range(1, 3):
                        self.dig.Drawing.outtext(self.pldispbuf, 108, 0, c)
                        self.dig.Scores.writecurscore(c)
                        self.dig.newframe()
                        if self.dig.Input.escape:
                            return
                self.dig.Scores.drawscores()
                self.dig.Scores.addscore(0)
        else:
            self.initchars()
        self.dig.Input.keypressed = 0
        self.dig.Drawing.outtext2("        ", 108, 0, 3)
        self.dig.Scores.initscores()
        self.dig.Drawing.drawlives()
        self.dig.Sound.music(1)
        self.dig.Input.readdir()
        self.dig.time = self.dig.Pc.gethrt()
        while (not self.gamedat[self.curplayer].dead) and (
                not self.gamedat[self.curplayer].levdone) and not self.dig.Input.escape:
            self.penalty = 0
            self.dig.dodigger()
            self.dig.Monster.domonsters()
            self.dig.Bags.dobags()
            if self.penalty > 8:
                self.dig.Monster.incmont(self.penalty - 8)
            self.testpause()
            self.checklevdone()
        self.dig.erasedigger()
        self.dig.Sound.musicoff()
        t = 20
        while (self.dig.Bags.getnmovingbags() != 0 or t != 0) and not self.dig.Input.escape:
            if t != 0:
                t -= 1
            self.penalty = 0
            self.dig.Bags.dobags()
            self.dig.dodigger()
            self.dig.Monster.domonsters()
            if self.penalty < 8:
                t = 0
        self.dig.Sound.soundstop()
        self.dig.killfire()
        self.dig.erasebonus()
        self.dig.Bags.cleanupbags()
        self.dig.Drawing.savefield()
        self.dig.Monster.erasemonsters()
        self.dig.newframe()
        if self.gamedat[self.curplayer].levdone:
            self.dig.Sound.soundlevdone()
        if self.dig.countem() == 0:
            self.gamedat[self.curplayer].level += 1
            if self.gamedat[self.curplayer].level > 1000:
                self.gamedat[self.curplayer].level = 1000
            self.initlevel()
        if self.gamedat[self.curplayer].dead:
            self.gamedat[self.curplayer].lives -= 1
            self.dig.Drawing.drawlives()
            if self.gamedat[self.curplayer].lives == 0 and not self.dig.Input.escape:
                self.dig.Scores.endofgame()
        if self.gamedat[self.curplayer].levdone:
            self.gamedat[self.curplayer].level += 1
            if self.gamedat[self.curplayer].level > 1000:
                self.gamedat[self.curplayer].level = 1000
            self.initlevel()

    def randno(self, n):
        self.randv = self.randv * 0x15a4e35 + 1
        return (self.randv & 0x7fffffff) % n

    def setdead(self, bp6):
        self.gamedat[self.curplayer].dead = bp6

    def shownplayers(self):
        if self.nplayers == 1:
            self.dig.Drawing.outtext2("ONE", 220, 25, 3)
            self.dig.Drawing.outtext2(" PLAYER ", 192, 39, 3)
        else:
            self.dig.Drawing.outtext2("TWO", 220, 25, 3)
            self.dig.Drawing.outtext2(" PLAYERS", 184, 39, 3)

    def switchnplayers(self):
        self.nplayers = 3 - self.nplayers

    def testpause(self):
        if self.dig.Input.akeypressed == 32:
            self.dig.Input.akeypressed = 0
            self.dig.Sound.soundpause()
            self.dig.Sound.sett2val(40)
            self.dig.Sound.setsoundt2()
            self.cleartopline()
            self.dig.Drawing.outtext("PRESS ANY KEY", 80, 0, 1)
            self.dig.newframe()
            self.dig.Input.keypressed = 0
            while True:
                SystemX.sleep(50)
                if self.dig.Input.keypressed != 0:
                    break
            self.cleartopline()
            self.dig.Scores.drawscores()
            self.dig.Scores.addscore(0)
            self.dig.Drawing.drawlives()
            self.dig.newframe()
            self.dig.time = self.dig.Pc.gethrt() - self.dig.frametime
            self.dig.Input.keypressed = 0
        else:
            self.dig.Sound.soundpauseoff()
