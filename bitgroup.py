from bitdic import BitDic


class Half:
    def __init__(self, parent, bdic, rank):
        self.rank = rank
        self.parent = parent
        self.bidic = bdic

    def separate(self):
        pass


class BitGroup:
    def __init__(self, gname, vkdic, nov):
        self.vkdic = vkdic
        self.nov = nov
        self.gname = gname
        self.rootbdic = BitDic("root", "seed", vkdic, nov)
        h_lower_bit = nov // 2
        self.hbitdic = self.rootbdic.subset(nov - 1, h_lower_bit)
        self.lbitdic = self.rootbdic.subset(h_lower_bit - 1, 0)
        self.hhalf = Half(self, self.hbitdic)
        self.lhalf = Half(self, self.lbitdic)
        # self.pd1vkdic = {}
        # self.pd2vkdic = {}
        # self.set_pdvkdics()

    def subset(self, highbit, lowbit=0):
        ''' carve out [highbit..lowbit] - collect all kvs sitting on these bits
            and construct a new BitDic using these vks. Return the BitDic inst.
            '''
        vkd0 = {}
        bits = list(self.dic.keys())
        drops = []
        for b in bits:
            if b > highbit or b < lowbit:
                drops.append(b)

        b = lowbit
        while b <= highbit:
            zeros, ones = self.dic[b]  # lists of vks
            for kn in zeros + ones:    # zeros and ones have diff kns in them
                if kn not in vkd0:
                    vk = self.vkdic[kn].clone(drops, lowbit)
                    vkd0[kn] = vk
            b += 1

        return BitDic("subset",
                      self.name + "-child",
                      vkd0,
                      (highbit - lowbit) + 1)

    def set_pdvkdics(self):
        for kn, kv in self.bitdic.vkdic.items():
            if kv.nob == 1:
                self.pd1vkdic[kn] = kv
            elif kv.nob == 2:
                self.pd2vkdic[kn] = kv
