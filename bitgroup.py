from bitdic import BitDic
from basics import get_sdic, make_vkdic


class Half:
    def __init__(self, parent, bitdic, rank):
        self.rank = rank
        self.parent = parent
        self.bitdic = bitdic
        self.separate()

    def separate(self):
        for ln in [1, 2]:
            # vk.completion (def: 3), set for 1 and 2
            for kn in self.bitdic.ordered_vkdic[ln]:
                self.bitdic.vkdic[kn].completion = ln
        # the whole value-space
        vs = [i for i in range(2 ** self.bitdic.nov)]
        # values hit by kv-3(final hit)
        self.hitvs = []
        self.vsdic = {}
        # collecting final hits in hitvs, update vs
        for kn, vk in self.bitdic.vkdic.items():
            if vk.completion == 3:
                for v in vk.hit_valuelist():
                    if v not in self.hitvs:
                        self.hitvs.append(v)
                    if v in vs:
                        vs.remove(v)
        for ln in [1, 2]:
            for kn in self.bitdic.ordered_vkdic[ln]:
                vk = self.bitdic.vkdic[kn]
                hits = vk.hit_valuelist()
                for v in hits:
                    if v not in self.hitvs:
                        lst = self.vsdic.setdefault(v, set([])).add(kn)

    def find_sats(self, half0):
        sats = []
        for hv, hs in self.vsdic.items():
            for lv, ls in half0.vsdic.items():
                cs = hs.intersection(ls)
                if len(cs) == 0:
                    sats.append((hv, lv))
        return sats


class BitGroup:
    def __init__(self, gname, vkdic, nov):
        self.vkdic = vkdic
        self.nov = nov
        self.gname = gname
        self.rootbdic = BitDic("root", "seed", vkdic, nov)
        h_lower_bit = nov // 2
        hbitdic = self.rootbdic.subset(nov - 1, h_lower_bit)
        lbitdic = self.rootbdic.subset(h_lower_bit - 1, 0)
        self.half0 = Half(self, lbitdic, 0)
        self.half1 = Half(self, hbitdic, 1)

    def solve(self):
        sats = self.half1.find_sats(self.half0)
        return sats


if __name__ == '__main__':
    cfg_filename = 'cfg6-13.json'
    sdic = get_sdic('./configs/' + cfg_filename)
    vkdic = make_vkdic(sdic['kdic'], sdic['nov'])
    bg = BitGroup('group', vkdic, sdic['nov'])
    sats = bg.solve()
    print(f'sats: {sats}')
