class BitGroup:
    def __init__(self, gname, bitdic):
        self.bitdic = bitdic
        self.nov = bitdic.nov
        self.gname = gname
        self.pd1vkdic = {}
        self.pd2vkdic = {}
        self.set_pdvkdics()

    def set_pdvkdics(self):
        for kn, kv in self.bitdic.vkdic.items():
            if kv.nob == 1:
                self.pd1vkdic[kn] = kv
            elif kv.nob == 2:
                self.pd2vkdic[kn] = kv
