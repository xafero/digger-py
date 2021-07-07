# sound has not been ported yet
import math

from systemx import SystemX


class Sound:

    def __init__(self, d):
        self.dig = d
        self.wavetype = 0
        self.t2val = 0
        self.t0val = 0
        self.musvol = 0
        self.spkrmode = 0
        self.timerrate = 0x7d0
        self.timercount = 0
        self.pulsewidth = 1
        self.volume = 0
        self.timerclock = 0
        self.soundflag = True
        self.musicflag = True
        self.sndflag = False
        self.soundpausedflag = False
        self.soundlevdoneflag = False
        self.nljpointer = 0
        self.nljnoteduration = 0
        self.newlevjingle = [0x8e8, 0x712, 0x5f2, 0x7f0, 0x6ac, 0x54c, 0x712, 0x5f2, 0x4b8, 0x474, 0x474]
        self.soundfallflag = False
        self.soundfallf = False
        self.soundfallvalue = 0
        self.soundfalln = 0
        self.soundbreakflag = False
        self.soundbreakduration = 0
        self.soundbreakvalue = 0
        self.soundwobbleflag = False
        self.soundwobblen = 0
        self.soundfireflag = False
        self.soundfirevalue = 0
        self.soundfiren = 0
        self.soundexplodeflag = False
        self.soundexplodevalue = 0
        self.soundexplodeduration = 0
        self.soundbonusflag = False
        self.soundbonusn = 0
        self.soundemflag = False
        self.soundemeraldflag = False
        self.soundemeraldduration = 0
        self.emerfreq = 0
        self.soundemeraldn = 0
        self.soundgoldflag = False
        self.soundgoldf = False
        self.soundgoldvalue1 = 0
        self.soundgoldvalue2 = 0
        self.soundgoldduration = 0
        self.soundeatmflag = False
        self.soundeatmvalue = 0
        self.soundeatmduration = 0
        self.soundeatmn = 0
        self.soundddieflag = False
        self.soundddien = 0
        self.soundddievalue = 0
        self.sound1upflag = False
        self.sound1upduration = 0
        self.musicplaying = False
        self.musicp = 0
        self.tuneno = 0
        self.noteduration = 0
        self.notevalue = 0
        self.musicmaxvol = 0
        self.musicattackrate = 0
        self.musicsustainlevel = 0
        self.musicdecayrate = 0
        self.musicnotewidth = 0
        self.musicreleaserate = 0
        self.musicstage = 0
        self.musicn = 0
        self.soundt0flag = False
        self.int8flag = False

    def initsound(self):
        self.wavetype = 2
        self.t0val = 12000
        self.musvol = 8
        self.t2val = 40
        self.soundt0flag = True
        self.sndflag = True
        self.spkrmode = 0
        self.int8flag = False
        self.setsoundt2()
        self.soundstop()
        self.startint8()
        self.timerrate = 0x4000

    def killsound(self):
        pass

    def music(self, tune):
        self.tuneno = tune
        self.musicp = 0
        self.noteduration = 0
        if tune == 0:
            self.musicmaxvol = 50
            self.musicattackrate = 20
            self.musicsustainlevel = 20
            self.musicdecayrate = 10
            self.musicreleaserate = 4
        elif tune == 1:
            self.musicmaxvol = 50
            self.musicattackrate = 50
            self.musicsustainlevel = 8
            self.musicdecayrate = 15
            self.musicreleaserate = 1
        elif tune == 2:
            self.musicmaxvol = 50
            self.musicattackrate = 50
            self.musicsustainlevel = 25
            self.musicdecayrate = 5
            self.musicreleaserate = 1
        self.musicplaying = True
        if tune == 2:
            self.soundddieoff()

    def musicoff(self):
        self.musicplaying = False
        self.musicp = 0

    def musicupdate(self):
        if not self.musicplaying:
            return
        if self.noteduration != 0:
            self.noteduration -= 1
        else:
            self.musicstage = self.musicn = 0
            if self.tuneno == 0:
                self.musicnotewidth = self.noteduration - 3
                self.musicp += 2
            elif self.tuneno == 1:
                self.musicnotewidth = 12
                self.musicp += 2
            elif self.tuneno == 2:
                self.musicnotewidth = self.noteduration - 10
                self.musicp += 2
        self.musicn += 1
        self.wavetype = 1
        self.t0val = self.notevalue
        if self.musicn >= self.musicnotewidth:
            self.musicstage = 2
        if self.musicstage == 0:
            if self.musvol + self.musicattackrate >= self.musicmaxvol:
                self.musicstage = 1
                self.musvol = self.musicmaxvol
                self.musicupdate_broken()
                return
            self.musvol += self.musicattackrate
        elif self.musicstage == 1:
            if self.musvol - self.musicdecayrate <= self.musicsustainlevel:
                self.musvol = self.musicsustainlevel
                self.musicupdate_broken()
                return
            self.musvol -= self.musicdecayrate
        elif self.musicstage == 2:
            if self.musvol - self.musicreleaserate <= 1:
                self.musvol = 1
                self.musicupdate_broken()
                return
            self.musvol -= self.musicreleaserate
        self.musicupdate_broken()

    def musicupdate_broken(self):
        if self.musvol == 1:
            self.t0val = 0x7d00

    def s0fillbuffer(self):
        pass

    def s0killsound(self):
        self.setsoundt2()
        self.stopint8()

    def s0setupsound(self):
        self.startint8()

    def setsoundmode(self):
        self.spkrmode = self.wavetype
        if (not self.soundt0flag) and self.sndflag:
            self.soundt0flag = True

    def setsoundt2(self):
        if self.soundt0flag:
            self.spkrmode = 0
            self.soundt0flag = False

    def sett0(self):
        if self.sndflag:
            if self.t0val < 1000 and (self.wavetype == 1 or self.wavetype == 2):
                self.t0val = 1000
            self.timerrate = self.t0val
            if self.musvol < 1:
                self.musvol = 1
            if self.musvol > 50:
                self.musvol = 50
            self.pulsewidth = self.musvol * self.volume
            self.setsoundmode()

    def sett2val(self, t2v):
        pass

    def setupsound(self):
        pass

    def sound1up(self):
        self.sound1upduration = 96
        self.sound1upflag = True

    def sound1upoff(self):
        self.sound1upflag = False

    def sound1upupdate(self):
        if self.sound1upflag:
            if (math.trunc(self.sound1upduration / float(3))) % 2 != 0:
                self.t2val = (self.sound1upduration << 2) + 600
            self.sound1upduration -= 1
            if self.sound1upduration < 1:
                self.sound1upflag = False

    def soundbonus(self):
        self.soundbonusflag = True

    def soundbonusoff(self):
        self.soundbonusflag = False
        self.soundbonusn = 0

    def soundbonusupdate(self):
        if self.soundbonusflag:
            self.soundbonusn += 1
            if self.soundbonusn > 15:
                self.soundbonusn = 0
            if 0 <= self.soundbonusn < 6:
                self.t2val = 0x4ce
            if 8 <= self.soundbonusn < 14:
                self.t2val = 0x5e9

    def soundbreak(self):
        self.soundbreakduration = 3
        if self.soundbreakvalue < 15000:
            self.soundbreakvalue = 15000
        self.soundbreakflag = True

    def soundbreakoff(self):
        self.soundbreakflag = False

    def soundbreakupdate(self):
        if self.soundbreakflag:
            if self.soundbreakduration != 0:
                self.soundbreakduration -= 1
                self.t2val = self.soundbreakvalue
            else:
                self.soundbreakflag = False

    def soundddie(self):
        self.soundddien = 0
        self.soundddievalue = 20000
        self.soundddieflag = True

    def soundddieoff(self):
        self.soundddieflag = False

    def soundddieupdate(self):
        if self.soundddieflag:
            self.soundddien += 1
            if self.soundddien == 1:
                self.musicoff()
            if 1 <= self.soundddien <= 10:
                self.soundddievalue = 20000 - self.soundddien * 1000
            if self.soundddien > 10:
                self.soundddievalue += 500
            if self.soundddievalue > 30000:
                self.soundddieoff()
            self.t2val = self.soundddievalue

    def soundeatm(self):
        self.soundeatmduration = 20
        self.soundeatmn = 3
        self.soundeatmvalue = 2000
        self.soundeatmflag = True

    def soundeatmoff(self):
        self.soundeatmflag = False

    def soundeatmupdate(self):
        if self.soundeatmflag:
            if self.soundeatmn != 0:
                if self.soundeatmduration != 0:
                    if (self.soundeatmduration % 4) == 1:
                        self.t2val = self.soundeatmvalue
                    if (self.soundeatmduration % 4) == 3:
                        self.t2val = self.soundeatmvalue - (self.soundeatmvalue >> 4)
                    self.soundeatmduration -= 1
                    self.soundeatmvalue -= (self.soundeatmvalue >> 4)
                else:
                    self.soundeatmduration = 20
                    self.soundeatmn -= 1
                    self.soundeatmvalue = 2000
            else:
                self.soundeatmflag = False

    def soundem(self):
        self.soundemflag = True

    def soundemerald(self, emocttime):
        if emocttime != 0:
            if self.emerfreq == 0x8e8:
                self.emerfreq = 0x7f0
            elif self.emerfreq == 0x7f0:
                self.emerfreq = 0x712
            elif self.emerfreq == 0x712:
                self.emerfreq = 0x6ac
            elif self.emerfreq == 0x6ac:
                self.emerfreq = 0x5f2
            elif self.emerfreq == 0x5f2:
                self.emerfreq = 0x54c
            elif self.emerfreq == 0x54c:
                self.emerfreq = 0x4b8
            elif self.emerfreq == 0x4b8:
                self.emerfreq = 0x474
                self.dig.Scores.scoreoctave()
            elif self.emerfreq == 0x474:
                self.emerfreq = 0x8e8
        else:
            self.emerfreq = 0x8e8
        self.soundemeraldduration = 7
        self.soundemeraldn = 0
        self.soundemeraldflag = True

    def soundemeraldoff(self):
        self.soundemeraldflag = False

    def soundemeraldupdate(self):
        if self.soundemeraldflag:
            if self.soundemeraldduration != 0:
                if self.soundemeraldn == 0 or self.soundemeraldn == 1:
                    self.t2val = self.emerfreq
                self.soundemeraldn += 1
                if self.soundemeraldn > 7:
                    self.soundemeraldn = 0
                    self.soundemeraldduration -= 1
            else:
                self.soundemeraldoff()

    def soundemoff(self):
        self.soundemflag = False

    def soundemupdate(self):
        if self.soundemflag:
            self.t2val = 1000
            self.soundemoff()

    def soundexplode(self):
        self.soundexplodevalue = 1500
        self.soundexplodeduration = 10
        self.soundexplodeflag = True
        self.soundfireoff()

    def soundexplodeoff(self):
        self.soundexplodeflag = False

    def soundexplodeupdate(self):
        if self.soundexplodeflag:
            if self.soundexplodeduration != 0:
                self.soundexplodevalue = self.t2val = self.soundexplodevalue - (self.soundexplodevalue >> 3)
                self.soundexplodeduration -= 1
            else:
                self.soundexplodeflag = False

    def soundfall(self):
        self.soundfallvalue = 1000
        self.soundfallflag = True

    def soundfalloff(self):
        self.soundfallflag = False
        self.soundfalln = 0

    def soundfallupdate(self):
        if self.soundfallflag:
            if self.soundfalln < 1:
                self.soundfalln += 1
                if self.soundfallf:
                    self.t2val = self.soundfallvalue
            else:
                self.soundfalln = 0
                if self.soundfallf:
                    self.soundfallvalue += 50
                    self.soundfallf = False
                else:
                    self.soundfallf = True

    def soundfire(self):
        self.soundfirevalue = 500
        self.soundfireflag = True

    def soundfireoff(self):
        self.soundfireflag = False
        self.soundfiren = 0

    def soundfireupdate(self):
        if self.soundfireflag:
            if self.soundfiren == 1:
                self.soundfiren = 0
                self.soundfirevalue += math.trunc(self.soundfirevalue / float(55))
                self.t2val = self.soundfirevalue + self.dig.Main.randno(self.soundfirevalue >> 3)
                if self.soundfirevalue > 30000:
                    self.soundfireoff()
            else:
                self.soundfiren += 1

    def soundgold(self):
        self.soundgoldvalue1 = 500
        self.soundgoldvalue2 = 4000
        self.soundgoldduration = 30
        self.soundgoldf = False
        self.soundgoldflag = True

    def soundgoldoff(self):
        self.soundgoldflag = False

    def soundgoldupdate(self):
        if self.soundgoldflag:
            if self.soundgoldduration != 0:
                self.soundgoldduration -= 1
            else:
                self.soundgoldflag = False
            if self.soundgoldf:
                self.soundgoldf = False
                self.t2val = self.soundgoldvalue1
            else:
                self.soundgoldf = True
                self.t2val = self.soundgoldvalue2
            self.soundgoldvalue1 += (self.soundgoldvalue1 >> 4)
            self.soundgoldvalue2 -= (self.soundgoldvalue2 >> 4)

    def soundint(self):
        self.timerclock += 1
        if self.soundflag and not self.sndflag:
            self.sndflag = self.musicflag = True
        if (not self.soundflag) and self.sndflag:
            self.sndflag = False
            self.setsoundt2()
        if self.sndflag and not self.soundpausedflag:
            self.t0val = 0x7d00
            self.t2val = 40
            if self.musicflag:
                self.musicupdate()
            self.soundemeraldupdate()
            self.soundwobbleupdate()
            self.soundddieupdate()
            self.soundbreakupdate()
            self.soundgoldupdate()
            self.soundemupdate()
            self.soundexplodeupdate()
            self.soundfireupdate()
            self.soundeatmupdate()
            self.soundfallupdate()
            self.sound1upupdate()
            self.soundbonusupdate()
            if self.t0val == 0x7d00 or self.t2val != 40:
                self.setsoundt2()
            else:
                self.setsoundmode()
                self.sett0()
            self.sett2val(self.t2val)

    @staticmethod
    def soundlevdone():
        SystemX.sleep(1000)

    def soundlevdoneoff(self):
        self.soundlevdoneflag = self.soundpausedflag = False

    def soundlevdoneupdate(self):
        if self.sndflag:
            if self.nljpointer < 11:
                self.t2val = self.newlevjingle[self.nljpointer]
            self.t0val = self.t2val + 35
            self.musvol = 50
            self.setsoundmode()
            self.sett0()
            self.sett2val(self.t2val)
            if self.nljnoteduration > 0:
                self.nljnoteduration -= 1
            else:
                self.nljnoteduration = 20
                self.nljpointer += 1
                if self.nljpointer > 10:
                    self.soundlevdoneoff()
        else:
            self.soundlevdoneflag = False

    def soundoff(self):
        pass

    def soundpause(self):
        self.soundpausedflag = True

    def soundpauseoff(self):
        self.soundpausedflag = False

    def soundstop(self):
        self.soundfalloff()
        self.soundwobbleoff()
        self.soundfireoff()
        self.musicoff()
        self.soundbonusoff()
        self.soundexplodeoff()
        self.soundbreakoff()
        self.soundemoff()
        self.soundemeraldoff()
        self.soundgoldoff()
        self.soundeatmoff()
        self.soundddieoff()
        self.sound1upoff()

    def soundwobble(self):
        self.soundwobbleflag = True

    def soundwobbleoff(self):
        self.soundwobbleflag = False
        self.soundwobblen = 0

    def soundwobbleupdate(self):
        if self.soundwobbleflag:
            self.soundwobblen += 1
            if self.soundwobblen > 63:
                self.soundwobblen = 0
            if self.soundwobblen == 0:
                self.t2val = 0x7d0
            elif (self.soundwobblen == 16) or (self.soundwobblen == 48):
                self.t2val = 0x9c4
            elif self.soundwobblen == 32:
                self.t2val = 0xbb8

    def startint8(self):
        if not self.int8flag:
            self.timerrate = 0x4000
            self.int8flag = True

    def stopint8(self):
        if self.int8flag:
            self.int8flag = False
        self.sett2val(40)
