class Input:

    def __init__(self, d):
        self.dig = d
        self.leftpressed = False
        self.rightpressed = False
        self.uppressed = False
        self.downpressed = False
        self.f1pressed = False
        self.firepressed = False
        self.minuspressed = False
        self.pluspressed = False
        self.f10pressed = False
        self.escape = False
        self.keypressed = 0
        self.akeypressed = 0
        self.dynamicdir = -1
        self.staticdir = -1
        self.joyx = 0
        self.joyy = 0
        self.joybut1 = False
        self.joybut2 = False
        self.keydir = 0
        self.jleftthresh = 0
        self.jupthresh = 0
        self.jrightthresh = 0
        self.jdownthresh = 0
        self.joyanax = 0
        self.joyanay = 0
        self.firepflag = False
        self.joyflag = False

    def checkkeyb(self):
        if self.pluspressed:
            if self.dig.frametime > self.dig.MIN_RATE:
                self.dig.frametime -= 5
        if self.minuspressed:
            if self.dig.frametime < self.dig.MAX_RATE:
                self.dig.frametime += 5
        if self.f10pressed:
            self.escape = True

    def detectjoy(self):
        self.joyflag = False
        self.staticdir = self.dynamicdir = -1

    @staticmethod
    def getasciikey(make):
        if (make == ord(' ')) or ((make >= ord('a')) and (make <= ord('z'))) or ((make >= ord('0')) and (make <= ord('9'))):
            return make
        else:
            return 0

    def getdir(self):
        bp2 = self.keydir
        return bp2

    def initkeyb(self):
        pass

    def key_downpressed(self):
        self.downpressed = True
        self.dynamicdir = self.staticdir = 6

    def key_downreleased(self):
        self.downpressed = False
        if self.dynamicdir == 6:
            self.setdirec()

    def key_f1pressed(self):
        self.firepressed = True
        self.f1pressed = True

    def key_f1released(self):
        self.f1pressed = False

    def key_leftpressed(self):
        self.leftpressed = True
        self.dynamicdir = self.staticdir = 4

    def key_leftreleased(self):
        self.leftpressed = False
        if self.dynamicdir == 4:
            self.setdirec()

    def key_rightpressed(self):
        self.rightpressed = True
        self.dynamicdir = self.staticdir = 0

    def key_rightreleased(self):
        self.rightpressed = False
        if self.dynamicdir == 0:
            self.setdirec()

    def key_uppressed(self):
        self.uppressed = True
        self.dynamicdir = self.staticdir = 2

    def key_upreleased(self):
        self.uppressed = False
        if self.dynamicdir == 2:
            self.setdirec()

    def processkey(self, key):
        self.keypressed = key
        if key > 0x80:
            self.akeypressed = key & 0x7f
        if key == 0x4b:
            self.key_leftpressed()
        elif key == 0xcb:
            self.key_leftreleased()
        elif key == 0x4d:
            self.key_rightpressed()
        elif key == 0xcd:
            self.key_rightreleased()
        elif key == 0x48:
            self.key_uppressed()
        elif key == 0xc8:
            self.key_upreleased()
        elif key == 0x50:
            self.key_downpressed()
        elif key == 0xd0:
            self.key_downreleased()
        elif key == 0x3b:
            self.key_f1pressed()
        elif key == 0xbb:
            self.key_f1released()
        elif key == 0x78:
            self.f10pressed = True
        elif key == 0xf8:
            self.f10pressed = False
        elif key == 0x2b:
            self.pluspressed = True
        elif key == 0xab:
            self.pluspressed = False
        elif key == 0x2d:
            self.minuspressed = True
        elif key == 0xad:
            self.minuspressed = False

    def readdir(self):
        self.keydir = self.staticdir
        if self.dynamicdir != -1:
            self.keydir = self.dynamicdir
        self.staticdir = -1
        if self.f1pressed or self.firepressed:
            self.firepflag = True
        else:
            self.firepflag = False
        self.firepressed = False

    def readjoy(self):
        pass

    def setdirec(self):
        self.dynamicdir = -1
        if self.uppressed:
            self.dynamicdir = self.staticdir = 2
        if self.downpressed:
            self.dynamicdir = self.staticdir = 6
        if self.leftpressed:
            self.dynamicdir = self.staticdir = 4
        if self.rightpressed:
            self.dynamicdir = self.staticdir = 0

    def teststart(self):
        startf = False
        if self.keypressed != 0 and (self.keypressed & 0x80) == 0 and self.keypressed != 27:
            startf = True
            self.joyflag = False
            self.keypressed = 0
        if not startf:
            return False
        return True
