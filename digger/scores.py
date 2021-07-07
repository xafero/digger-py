import math

from systemx import SystemX


class Scores:

    def __init__(self, d):
        self.dig = d
        self.scores = [[]]
        self.substr = ''
        self.highbuf = ['\0' for _ in range(10)]
        self.scorehigh = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.scoreinit = ['' for _ in range(11)]
        self.scoret = 0
        self.score1 = 0
        self.score2 = 0
        self.nextbs1 = 0
        self.nextbs2 = 0
        self.hsbuf = ''
        self.scorebuf = ['\0' for _ in range(512)]
        self.bonusscore = 20000
        self.gotinitflag = False

    def _submit(self, n, s):
        if self.dig.subaddr is not None:
            pass
            # ms = 16 + int((SystemX.current_millis() % (65536 - 16)))
            # self.substr = n + '+' + s + '+' + str(ms) + '+' + ((ms + 32768) * s) % 65536
            # (Thread(self)).start()
        return self.scores

    def updatescores(self, o):

        if o is None:
            return

        try:
            inx = ['' for _ in range(10)]
            sc = [0 for _ in range(10)]
            for i in range(10):
                inx[i] = str(o[i][0])
                sc[i] = int((int(o[i][1])))
            for i in range(10):
                self.scoreinit[i + 1] = inx[i]
                self.scorehigh[i + 2] = sc[i]
        except IndexError:
            pass

    def addscore(self, score):
        if self.dig.Main.getcplayer() == 0:
            self.score1 += score
            if self.score1 > 999999:
                self.score1 = 0
            self.writenum(self.score1, 0, 0, 6, 1)
            if self.score1 >= self.nextbs1:
                if self.dig.Main.getlives(1) < 5:
                    self.dig.Main.addlife(1)
                    self.dig.Drawing.drawlives()
                self.nextbs1 += self.bonusscore
        else:
            self.score2 += score
            if self.score2 > 999999:
                self.score2 = 0
            if self.score2 < 100000:
                self.writenum(self.score2, 236, 0, 6, 1)
            else:
                self.writenum(self.score2, 248, 0, 6, 1)
            if self.score2 > self.nextbs2:
                if self.dig.Main.getlives(2) < 5:
                    self.dig.Main.addlife(2)
                    self.dig.Drawing.drawlives()
                self.nextbs2 += self.bonusscore
        self.dig.Main.incpenalty()
        self.dig.Main.incpenalty()
        self.dig.Main.incpenalty()

    def drawscores(self):
        self.writenum(self.score1, 0, 0, 6, 3)
        if self.dig.Main.nplayers == 2:
            if self.score2 < 100000:
                self.writenum(self.score2, 236, 0, 6, 3)
            else:
                self.writenum(self.score2, 248, 0, 6, 3)

    def endofgame(self):
        self.addscore(0)
        if self.dig.Main.getcplayer() == 0:
            self.scoret = self.score1
        else:
            self.scoret = self.score2
        if self.scoret > self.scorehigh[11]:
            self.dig.Pc.gclear()
            self.drawscores()
            self.dig.Main.pldispbuf = "PLAYER "
            if self.dig.Main.getcplayer() == 0:
                self.dig.Main.pldispbuf += "1"
            else:
                self.dig.Main.pldispbuf += "2"
            self.dig.Drawing.outtext(self.dig.Main.pldispbuf, 108, 0, 2, True)
            self.dig.Drawing.outtext(" NEW HIGH SCORE ", 64, 40, 2, True)
            self.getinitials()
            self.updatescores(self._submit(self.scoreinit[0], int(self.scoret)))
            self.shufflehigh()
        else:
            self.dig.Main.cleartopline()
            self.dig.Drawing.outtext("GAME OVER", 104, 0, 3, True)
            self.updatescores(self._submit("...", int(self.scoret)))
            self.dig.Sound.killsound()
            for j in range(20):  # Number of times screen flashes * 2
                for i in range(2):
                    self.dig.Sprite.setretr(True)
                    self.dig.Pc.gpal(1 - (j & 1))
                    self.dig.Sprite.setretr(False)
                    for _ in range(111):
                        pass  # A delay loop
                    self.dig.Pc.gpal(0)
                    self.dig.Pc.ginten(1 - i & 1)
                    self.dig.newframe()
            self.dig.Sound.setupsound()
            self.dig.Drawing.outtext("         ", 104, 0, 3, True)
            self.dig.Sprite.setretr(True)

    @staticmethod
    def flashywait(n):
        SystemX.sleep(n * 2)

    def getinitial(self, x, y):
        self.dig.Input.keypressed = 0
        self.dig.Pc.gwrite2(x, y, ord('_'), 3, True)
        for j in range(5):
            for i in range(40):
                if (self.dig.Input.keypressed & 0x80) == 0 and self.dig.Input.keypressed != 0:
                    return self.dig.Input.keypressed
                self.flashywait(15)
            for i in range(40):
                if (self.dig.Input.keypressed & 0x80) == 0 and self.dig.Input.keypressed != 0:
                    self.dig.Pc.gwrite2(x, y, ord('_'), 3, True)
                    return self.dig.Input.keypressed
                self.flashywait(15)
        self.gotinitflag = True
        return 0

    def getinitials(self):
        self.dig.Drawing.outtext("ENTER YOUR", 100, 70, 3, True)
        self.dig.Drawing.outtext(" INITIALS", 100, 90, 3, True)
        self.dig.Drawing.outtext("_ _ _", 128, 130, 3, True)
        self.scoreinit[0] = "..."
        self.dig.Sound.killsound()
        self.gotinitflag = False
        for i in range(3):
            k = 0
            while k == 0 and not self.gotinitflag:
                k = self.getinitial(i * 24 + 128, 130)
                if i != 0 and k == 8:
                    i -= 1
                k = self.dig.Input.getasciikey(k)
            if k != 0:
                self.dig.Pc.gwrite2(i * 24 + 128, 130, k, 3, True)
                sb = self.scoreinit[0] + ""
                sbnew = sb[:i] + chr(k) + sb[i + 1:]
                self.scoreinit[0] = sbnew
        self.dig.Input.keypressed = 0
        for i in range(20):
            self.flashywait(15)
        self.dig.Sound.setupsound()
        self.dig.Pc.gclear()
        self.dig.Pc.gpal(0)
        self.dig.Pc.ginten(0)
        self.dig.newframe()
        self.dig.Sprite.setretr(True)

    def initscores(self):
        self.addscore(0)

    def loadscores(self):
        p = 1
        for i in range(1, 10):
            for x in range(3):
                self.scoreinit[i] = "..."
            p += 2
            for x in range(6):
                self.highbuf[x] = self.scorebuf[p]
                p += 1
            self.scorehigh[i + 1] = 0
        if self.scorebuf[0] != 's':
            for i in range(11):
                self.scorehigh[i + 1] = 0
                self.scoreinit[i] = "..."

    @staticmethod
    def numtostring(n):
        x = 0
        p = ""
        for x in range(6):
            p = str(n % 10) + p
            n = math.trunc(n / float(10))
            if n == 0:
                x += 1
                break
        while x < 6:
            p = ' ' + p
            x += 1
        return p

    def run(self):
        pass

    def scorebonus(self):
        self.addscore(1000)

    def scoreeatm(self):
        self.addscore(self.dig.eatmsc * 200)
        self.dig.eatmsc <<= 1

    def scoreemerald(self):
        self.addscore(25)

    def scoregold(self):
        self.addscore(500)

    def scorekill(self):
        self.addscore(250)

    def scoreoctave(self):
        self.addscore(250)

    def showtable(self):
        self.dig.Drawing.outtext2("HIGH SCORES", 16, 25, 3)
        col = 2
        for i in range(1, 10):
            self.hsbuf = self.scoreinit[i] + "  " + self.numtostring(self.scorehigh[i + 1])
            self.dig.Drawing.outtext2(self.hsbuf, 16, 31 + 13 * i, col)
            col = 1

    def shufflehigh(self):
        j = 0
        for j in range(10, 2, -1):
            if self.scoret < self.scorehigh[j]:
                break
        i = 10
        while i > j:
            self.scorehigh[i + 1] = self.scorehigh[i]
            self.scoreinit[i] = self.scoreinit[i - 1]
            i -= 1
        self.scorehigh[j + 1] = self.scoret
        self.scoreinit[j] = self.scoreinit[0]

    def writecurscore(self, bp6):
        if self.dig.Main.getcplayer() == 0:
            self.writenum(self.score1, 0, 0, 6, bp6)
        else:
            if self.score2 < 100000:
                self.writenum(self.score2, 236, 0, 6, bp6)
            else:
                self.writenum(self.score2, 248, 0, 6, bp6)

    def writenum(self, n, x, y, w, c):
        xp = (w - 1) * 12 + x
        while w > 0:
            d = int((n % 10))
            if w > 1 or d > 0:
                self.dig.Pc.gwrite2(xp, y, d + ord('0'), c, False)
            n = math.trunc(n / float(10))
            w -= 1
            xp -= 12

    def zeroscores(self):
        self.score2 = 0
        self.score1 = 0
        self.scoret = 0
        self.nextbs1 = self.bonusscore
        self.nextbs2 = self.bonusscore
