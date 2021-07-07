import math

from monsterdata import MonsterData


class Monster:

    def __init__(self, d):
        self.dig = d
        self.mondat = [MonsterData(), MonsterData(), MonsterData(), MonsterData(), MonsterData(), MonsterData()]
        self.nextmonster = 0
        self.totalmonsters = 0
        self.maxmononscr = 0
        self.nextmontime = 0
        self.mongaptime = 0
        self.unbonusflag = False
        self.mongotgold = False

        self.dig = d

    def checkcoincide(self, mon, bits):
        m = 0
        b = 256
        while m < 6:
            if ((bits & b) != 0) and (self.mondat[mon].dir == self.mondat[m].dir) and (self.mondat[m].stime == 0) and (
                    self.mondat[mon].stime == 0):
                self.mondat[m].dir = self.dig.reversedir(self.mondat[m].dir)
            m += 1
            b <<= 1

    def checkmonscared(self, h):
        for m in range(6):
            if (h == self.mondat[m].h) and (self.mondat[m].dir == 2):
                self.mondat[m].dir = 6

    def createmonster(self):
        for i in range(6):
            if not self.mondat[i].flag:
                self.mondat[i].flag = True
                self.mondat[i].alive = True
                self.mondat[i].t = 0
                self.mondat[i].nob = True
                self.mondat[i].hnt = 0
                self.mondat[i].h = 14
                self.mondat[i].v = 0
                self.mondat[i].x = 292
                self.mondat[i].y = 18
                self.mondat[i].xr = 0
                self.mondat[i].yr = 0
                self.mondat[i].dir = 4
                self.mondat[i].hdir = 4
                self.nextmonster += 1
                self.nextmontime = self.mongaptime
                self.mondat[i].stime = 5
                self.dig.Sprite.movedrawspr(i + 8, self.mondat[i].x, self.mondat[i].y)
                break

    def domonsters(self):
        if self.nextmontime > 0:
            self.nextmontime -= 1
        else:
            if self.nextmonster < self.totalmonsters and self.nmononscr() < self.maxmononscr \
                    and self.dig.digonscr and not self.dig.bonusmode:
                self.createmonster()
            if self.unbonusflag and self.nextmonster == self.totalmonsters and self.nextmontime == 0:
                if self.dig.digonscr:
                    self.unbonusflag = False
                    self.dig.createbonus()
        for i in range(6):
            if self.mondat[i].flag:
                if self.mondat[i].hnt > 10 - self.dig.Main.levof10():
                    if self.mondat[i].nob:
                        self.mondat[i].nob = False
                        self.mondat[i].hnt = 0
                if self.mondat[i].alive:
                    if self.mondat[i].t == 0:
                        self.monai(i)
                        if self.dig.Main.randno(15 - self.dig.Main.levof10()) == 0 and self.mondat[i].nob:
                            self.monai(i)
                    else:
                        self.mondat[i].t -= 1
                else:
                    self.mondie(i)

    def erasemonsters(self):
        for i in range(6):
            if self.mondat[i].flag:
                self.dig.Sprite.erasespr(i + 8)

    def fieldclear(self, dirp, x, y):
        if dirp == 0:
            if x < 14:
                if (self.getfield(x + 1, y) & 0x2000) == 0:
                    if (self.getfield(x + 1, y) & 1) == 0 or (self.getfield(x, y) & 0x10) == 0:
                        return True
        elif dirp == 4:
            if x > 0:
                if (self.getfield(x - 1, y) & 0x2000) == 0:
                    if (self.getfield(x - 1, y) & 0x10) == 0 or (self.getfield(x, y) & 1) == 0:
                        return True
        elif dirp == 2:
            if y > 0:
                if (self.getfield(x, y - 1) & 0x2000) == 0:
                    if (self.getfield(x, y - 1) & 0x800) == 0 or (self.getfield(x, y) & 0x40) == 0:
                        return True
        elif dirp == 6:
            if y < 9:
                if (self.getfield(x, y + 1) & 0x2000) == 0:
                    if (self.getfield(x, y + 1) & 0x40) == 0 or (self.getfield(x, y) & 0x800) == 0:
                        return True
        return False

    def getfield(self, x, y):
        return self.dig.Drawing.field[y * 15 + x]

    def incmont(self, n):
        if n > 6:
            n = 6
        m = 1
        while m < n:
            self.mondat[m].t += 1
            m += 1

    def incpenalties(self, bits):
        m = 0
        b = 256
        while m < 6:
            if (bits & b) != 0:
                self.dig.Main.incpenalty()
            b <<= 1
            m += 1
            b <<= 1

    def initmonsters(self):
        for i in range(6):
            self.mondat[i].flag = False
        self.nextmonster = 0
        self.mongaptime = 45 - (self.dig.Main.levof10() << 1)
        self.totalmonsters = self.dig.Main.levof10() + 5
        if self.dig.Main.levof10() == 1:
            self.maxmononscr = 3
        elif (self.dig.Main.levof10() == 2) or (self.dig.Main.levof10() == 3) or (self.dig.Main.levof10() == 4) or (
                self.dig.Main.levof10() == 5) or (self.dig.Main.levof10() == 6) or (self.dig.Main.levof10() == 7):
            self.maxmononscr = 4
        elif (self.dig.Main.levof10() == 8) or (self.dig.Main.levof10() == 9) or (self.dig.Main.levof10() == 10):
            self.maxmononscr = 5
        self.nextmontime = 10
        self.unbonusflag = True

    def killmon(self, mon):
        if self.mondat[mon].flag:
            self.mondat[mon].flag = self.mondat[mon].alive = False
            self.dig.Sprite.erasespr(mon + 8)
            if self.dig.bonusmode:
                self.totalmonsters += 1

    def killmonsters(self, bits):
        n = 0
        m = 0
        b = 256
        while m < 6:
            if (bits & b) != 0:
                self.killmon(m)
                n += 1
            m += 1
            b <<= 1
        return n

    def monai(self, mon):
        monox = self.mondat[mon].x
        monoy = self.mondat[mon].y
        if self.mondat[mon].xr == 0 and self.mondat[mon].yr == 0:

            # If we are here the monster needs to know which way to turn next. 

            # Turn hobbin back into nobbin if it's had its time 

            if self.mondat[mon].hnt > 30 + (self.dig.Main.levof10() << 1):
                if not self.mondat[mon].nob:
                    self.mondat[mon].hnt = 0
                    self.mondat[mon].nob = True

            # Set up monster direction properties to chase dig 

            if abs(self.dig.diggery - self.mondat[mon].y) > abs(self.dig.diggerx - self.mondat[mon].x):
                if self.dig.diggery < self.mondat[mon].y:
                    mdirp1 = 2
                    mdirp4 = 6
                else:
                    mdirp1 = 6
                    mdirp4 = 2
                if self.dig.diggerx < self.mondat[mon].x:
                    mdirp2 = 4
                    mdirp3 = 0
                else:
                    mdirp2 = 0
                    mdirp3 = 4
            else:
                if self.dig.diggerx < self.mondat[mon].x:
                    mdirp1 = 4
                    mdirp4 = 0
                else:
                    mdirp1 = 0
                    mdirp4 = 4
                if self.dig.diggery < self.mondat[mon].y:
                    mdirp2 = 2
                    mdirp3 = 6
                else:
                    mdirp2 = 6
                    mdirp3 = 2

            # In bonus mode, run away from digger 

            if self.dig.bonusmode:
                t = mdirp1
                mdirp1 = mdirp4
                mdirp4 = t
                t = mdirp2
                mdirp2 = mdirp3
                mdirp3 = t

            # Adjust priorities so that monsters don't reverse direction unless they really have to

            dirp = self.dig.reversedir(self.mondat[mon].dir)
            if dirp == mdirp1:
                mdirp1 = mdirp2
                mdirp2 = mdirp3
                mdirp3 = mdirp4
                mdirp4 = dirp
            if dirp == mdirp2:
                mdirp2 = mdirp3
                mdirp3 = mdirp4
                mdirp4 = dirp
            if dirp == mdirp3:
                mdirp3 = mdirp4
                mdirp4 = dirp

            # Introduce a randno element on levels <6 : occasionally swap p1 and p3 

            if self.dig.Main.randno(self.dig.Main.levof10() + 5) == 1 and self.dig.Main.levof10() < 6:
                t = mdirp1
                mdirp1 = mdirp3
                mdirp3 = t

            # Check field and find direction 

            if self.fieldclear(mdirp1, self.mondat[mon].h, self.mondat[mon].v):
                dirp = mdirp1
            else:
                if self.fieldclear(mdirp2, self.mondat[mon].h, self.mondat[mon].v):
                    dirp = mdirp2
                else:
                    if self.fieldclear(mdirp3, self.mondat[mon].h, self.mondat[mon].v):
                        dirp = mdirp3
                    else:
                        if self.fieldclear(mdirp4, self.mondat[mon].h, self.mondat[mon].v):
                            dirp = mdirp4

            # Hobbins don't care about the field: they go where they want. 

            if not self.mondat[mon].nob:
                dirp = mdirp1

            # Monsters take a time penalty for changing direction 

            if self.mondat[mon].dir != dirp:
                self.mondat[mon].t += 1

            # Save the new direction 

            self.mondat[mon].dir = dirp

        # If monster is about to go off edge of screen, stop it. 

        if (self.mondat[mon].x == 292 and self.mondat[mon].dir == 0) or (
                self.mondat[mon].x == 12 and self.mondat[mon].dir == 4) or (
                self.mondat[mon].y == 180 and self.mondat[mon].dir == 6) or (
                self.mondat[mon].y == 18 and self.mondat[mon].dir == 2):
            self.mondat[mon].dir = -1

        # Change hdir for hobbin 

        if self.mondat[mon].dir == 4 or self.mondat[mon].dir == 0:
            self.mondat[mon].hdir = self.mondat[mon].dir

        # Hobbins digger 

        if not self.mondat[mon].nob:
            self.dig.Drawing.eatfield(self.mondat[mon].x, self.mondat[mon].y, self.mondat[mon].dir)

        # (Draw new tunnels) and move monster

        if self.mondat[mon].dir == 0:
            if not self.mondat[mon].nob:
                self.dig.Drawing.drawrightblob(self.mondat[mon].x, self.mondat[mon].y)
            self.mondat[mon].x += 4
        elif self.mondat[mon].dir == 4:
            if not self.mondat[mon].nob:
                self.dig.Drawing.drawleftblob(self.mondat[mon].x, self.mondat[mon].y)
            self.mondat[mon].x -= 4
        elif self.mondat[mon].dir == 2:
            if not self.mondat[mon].nob:
                self.dig.Drawing.drawtopblob(self.mondat[mon].x, self.mondat[mon].y)
            self.mondat[mon].y -= 3
        elif self.mondat[mon].dir == 6:
            if not self.mondat[mon].nob:
                self.dig.Drawing.drawbottomblob(self.mondat[mon].x, self.mondat[mon].y)
            self.mondat[mon].y += 3

        # Hobbins can eat emeralds 

        if not self.mondat[mon].nob:
            self.dig.hitemerald(math.trunc((self.mondat[mon].x - 12) / float(20)),
                                math.trunc((self.mondat[mon].y - 18) / float(18)), (self.mondat[mon].x - 12) % 20,
                                (self.mondat[mon].y - 18) % 18, self.mondat[mon].dir)

        # If digger's gone, don't bother 

        if not self.dig.digonscr:
            self.mondat[mon].x = monox
            self.mondat[mon].y = monoy

        # If monster's just started, don't move yet 

        if self.mondat[mon].stime != 0:
            self.mondat[mon].stime -= 1
            self.mondat[mon].x = monox
            self.mondat[mon].y = monoy

        # Increase time counter for hobbin 

        if (not self.mondat[mon].nob) and self.mondat[mon].hnt < 100:
            self.mondat[mon].hnt += 1

        # Draw monster 

        push = True
        clbits = self.dig.Drawing.drawmon(mon, self.mondat[mon].nob, self.mondat[mon].hdir, self.mondat[mon].x,
                                          self.mondat[mon].y)
        self.dig.Main.incpenalty()

        # Collision with another monster 

        if (clbits & 0x3f00) != 0:
            self.mondat[mon].t += 1  # Time penalty
            self.checkcoincide(mon, clbits)  # Ensure both aren't moving in the same dir.
            self.incpenalties(clbits)

        # Check for collision with bag 

        if (clbits & self.dig.Bags.bagbits()) != 0:
            self.mondat[mon].t += 1  # Time penalty
            self.mongotgold = False
            if self.mondat[mon].dir == 4 or self.mondat[mon].dir == 0:
                push = self.dig.Bags.pushbags(self.mondat[mon].dir, clbits)
                self.mondat[mon].t += 1  # Time penalty
            else:
                if not self.dig.Bags.pushudbags(clbits):  # Vertical push
                    push = False
            if self.mongotgold:  # No time penalty if monster eats gold
                self.mondat[mon].t = 0
            if (not self.mondat[mon].nob) and self.mondat[mon].hnt > 1:
                self.dig.Bags.removebags(clbits)  # Hobbins eat bags

        # Increase hobbin cross counter 

        if self.mondat[mon].nob and ((clbits & 0x3f00) != 0) and self.dig.digonscr:
            self.mondat[mon].hnt += 1

        # See if bags push monster back 

        if not push:
            self.mondat[mon].x = monox
            self.mondat[mon].y = monoy
            self.dig.Drawing.drawmon(mon, self.mondat[mon].nob, self.mondat[mon].hdir, self.mondat[mon].x,
                                     self.mondat[mon].y)
            self.dig.Main.incpenalty()
            if self.mondat[mon].nob:  # The other way to create hobbin: stuck on h-bag
                self.mondat[mon].hnt += 1
            if (self.mondat[mon].dir == 2 or self.mondat[mon].dir == 6) and self.mondat[mon].nob:
                self.mondat[mon].dir = self.dig.reversedir(self.mondat[mon].dir)  # If vertical, give up

        # Collision with digger 

        if ((clbits & 1) != 0) and self.dig.digonscr:
            if self.dig.bonusmode:
                self.killmon(mon)
                self.dig.Scores.scoreeatm()
                self.dig.Sound.soundeatm()  # Collision in bonus mode
            else:
                self.dig.killdigger(3, 0)  # Kill digger

        # Update co-ordinates 

        self.mondat[mon].h = math.trunc((self.mondat[mon].x - 12) / float(20))
        self.mondat[mon].v = math.trunc((self.mondat[mon].y - 18) / float(18))
        self.mondat[mon].xr = (self.mondat[mon].x - 12) % 20
        self.mondat[mon].yr = (self.mondat[mon].y - 18) % 18

    def mondie(self, mon):
        if self.mondat[mon].death == 1:
            if self.dig.Bags.bagy(self.mondat[mon].bag) + 6 > self.mondat[mon].y:
                self.mondat[mon].y = self.dig.Bags.bagy(self.mondat[mon].bag)
            self.dig.Drawing.drawmondie(mon, self.mondat[mon].nob, self.mondat[mon].hdir, self.mondat[mon].x,
                                        self.mondat[mon].y)
            self.dig.Main.incpenalty()
            if self.dig.Bags.getbagdir(self.mondat[mon].bag) == -1:
                self.mondat[mon].dtime = 1
                self.mondat[mon].death = 4
        elif self.mondat[mon].death == 4:
            if self.mondat[mon].dtime != 0:
                self.mondat[mon].dtime -= 1
            else:
                self.killmon(mon)
                self.dig.Scores.scorekill()

    def mongold(self):
        self.mongotgold = True

    def monleft(self):
        return self.nmononscr() + self.totalmonsters - self.nextmonster

    def nmononscr(self):
        n = 0
        for i in range(6):
            if self.mondat[i].flag:
                n += 1
        return n

    def squashmonster(self, mon, death, bag):
        self.mondat[mon].alive = False
        self.mondat[mon].death = death
        self.mondat[mon].bag = bag

    def squashmonsters(self, bag, bits):
        m = 0
        b = 256
        while m < 6:
            if (bits & b) != 0:
                if self.mondat[m].y >= self.dig.Bags.bagy(bag):
                    self.squashmonster(m, 1, bag)
            m += 1
            b <<= 1
