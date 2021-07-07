class BagData:

    def __init__(self):
        self.x = 0
        self.y = 0
        self.h = 0
        self.v = 0
        self.xr = 0
        self.yr = 0
        self.dir = 0
        self.wt = 0
        self.gt = 0
        self.fallh = 0
        self.wobbling = False
        self.unfallen = False
        self.exist = False

    def copy_from(self, t):
        self.x = t.x
        self.y = t.y
        self.h = t.h
        self.v = t.v
        self.xr = t.xr
        self.yr = t.yr
        self.dir = t.dir
        self.wt = t.wt
        self.gt = t.gt
        self.fallh = t.fallh
        self.wobbling = t.wobbling
        self.unfallen = t.unfallen
        self.exist = t.exist
