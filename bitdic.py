from basics import *
from vklause import VKlause
from visualizer import Visualizer
from TransKlauseEngine import TransKlauseEngine


class BitDic:
    ''' maintain a bit-dict:
        self.dic: { 7:[ [C1,C6], -- 7-th bit, these Clauses have it be 0
                        []       -- 7-th bit, these Clauses have it be 1
                      ],
                    6: [[],[]],
                ...
        }
        self.dic[7][0] -> [<list of clause-names, that use this bit, value:0>]
        self.dic[7][1] -> [<list of clause-names, that use this bit, value:1>]
        '''

    def __init__(self, seed_name, bdname, vkdic, nov):   # O(m)
        perf_count["BitDic-init"] += 1
        self.seed_name = seed_name
        self.name = bdname
        self.nov = nov
        if nov == 3:
            self.check8set = set([0, 1, 2, 3, 4, 5, 6, 7])
        self.dic = {}   # keyed by bits, value: [[0-kns],[1-kns]]
        self.vkdic = vkdic
        self.parent = None  # the parent that generated / tx-to self
        self.done = False
        self.ordered_vkdic = {}
        for i in range(nov):        # number_of_variables from config
            self.dic[i] = [[], []]
        self.add_vklause()
        self.conversion = None
        self.vis = Visualizer(self.vkdic, self.nov)
    # ==== end of def __init__(..)

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
        new_nov = highbit - lowbit + 1
        b = lowbit
        while b <= highbit:
            zeros, ones = self.dic[b]  # lists of vks
            for kn in zeros + ones:    # zeros and ones have diff kns in them
                if kn not in vkd0:
                    vk = self.vkdic[kn].clone(drops, new_nov)
                    vkd0[kn] = vk
            b += 1

        return BitDic("subset",
                      self.name + "-child",
                      vkd0,
                      (highbit - lowbit) + 1)

    def split_topbit(self, single, debug):
        ''' if self.nov = 8, top bit is bit-7.
            now bit-7 will be dropped, and self be split into
            2 bitdic:
            - bitdic0     -- all vks with bit-7 == 0. no Tx.
            - bitdic_tmp  -- all vks with bit-7 == 1. Tx to
                bitdic1 with seed picked from bitdic_tmp's vks
            if bitdic0 or bitdic_tmp has sat, return <sat>, None
            else, return bitdic0, bitdic1
            '''
        perf_count["split_topbit"] += 1
        if self.nov < 3:
            debug0 = 1
        tb = self.nov - 1   # top bit number
        vkdic0 = {}     # vks with top-bit == 0
        vkdic1 = {}     # vks with top-bit == 1
        vkdic_mix = {}  # vks with top-bit not used

        kns = list(self.vkdic.keys())

        for kn in self.dic[tb][0]:
            kdic = self.vkdic[kn].dic.copy()  # clone the vklause.dic
            # on the clone, drop top bit, nov decrease by 1 (tp)
            if tb in kdic:
                kdic.pop(tb)
            vkdic0[kn] = VKlause(kn, kdic, tb)

        for kn in self.dic[tb][1]:
            kdic = self.vkdic[kn].dic.copy()  # clone the vklause.dic
            # n the clone, drop top bit, nov decrease by 1 (tp)
            if tb in kdic:
                kdic.pop(tb)
            vkdic1[kn] = VKlause(kn, kdic, tb)

        for kn in kns:
            if (kn not in vkdic0) and (kn not in vkdic1):
                # no need to drop top bit, they don't have it.
                vkdic_mix[kn] = VKlause(kn, self.vkdic[kn].dic, tb)

        vkdic0.update(vkdic_mix)  # add mix-dic to 0-dic
        vkdic1.update(vkdic_mix)  # add mix-dic to 1-dic

        if len(vkdic0) == 0:
            if single:
                vs = [0]
            else:
                N1 = 2 ** tb
                vs = [v for v in range(N1)]
            sats = get_sats(self, vs)
            perf_count['SATS'] += sats
            bitdic0 = None
            # return len(perf_count['SATS']), None
        else:
            bitdic0 = BitDic(
                self.seed_name,
                self.name + f"-{tb}'0",
                vkdic0,
                tb)

            # from self to bitdic0: bit<tb> with value 0 droped
            # when converting back, a 0 should be added on tb-bit
            bitdic0.conversion = f"{tb}'0"
            bitdic0.parent = self

            sats = test4_finish(bitdic0)
            if len(sats) > 0:
                perf_count['SATS'] += sats
                # return len(sats), None

        if len(vkdic1) == 0:
            N1 = 2 ** tb
            if single:
                vs = [N1]
            else:
                vs = [N1 + v for v in range(N1)]
            perf_count['SATS'] += get_sats(self, vs)
            bitdic1 = None
            # return len(perf_count['SATS']), None
        else:
            bdic = self.dic.copy()  # clone the bit-dic from self
            bdic.pop(tb)            # drop the top bit in bdic

            seed, top_bit = self.set_txseed(vkdic1, bdic)
            bitdic_tmp = BitDic(
                f'~{self.seed_name}',
                self.name + f"-{tb}'1",
                vkdic1,
                tb)
            # from self to bitdic_tmp: bit<tb> with value 1 droped
            # when converting back, a 1 should be added on tb-bit
            bitdic_tmp.conversion = f"{tb}'1"
            bitdic_tmp.parent = self

            # the 2 returning bitdics will be visualized in solver4
            # here is for visualize the tmp
            if debug:
                bitdic_tmp.visualize()

            sats = test4_finish(bitdic_tmp)
            if len(sats) > 0:
                perf_count['SATS'] += sats
                bitdic1 = bitdic_tmp
                # return len(sats), None
            else:
                if not bitdic_tmp.done:
                    vk = vkdic1[seed]
                    tx = TransKlauseEngine(seed, top_bit, vk, tb)
                    # bitdic1 be tx-ed on 1 of its shortkns
                    bitdic1 = tx.trans_bitdic(bitdic_tmp)
                else:
                    bitdic1 = bitdic_tmp
        return bitdic0, bitdic1
    # ==== end of def split_topbit(self, single, debug)

    def most_popular(self, d):
        ''' Among every bit of d[bit] = [[0-kns],[1-kns]]
            find which bit has the most sum: len([0-kns]) + len([1-kns])
            This is used as the power of this bit (how popular)
            make a dict keyed by power, value is bit-number
            return all kns(from both 0/1 bit-values) of 
            the most power-full, of most popular bit
            '''
        bit_powers = {}  # <power>:<bit-name>}
        for b in d:
            bit_powers[len(d[b][0]) + len(d[b][1])] = b
        ps = sorted(list(bit_powers.keys()), reverse=True)
        # all knames in both 0-kns and 1-kns
        best_bit = bit_powers[ps[0]]
        kns = d[best_bit][0] + d[best_bit][1]
        return set(kns), best_bit
    # ==== end of def most_popular(self, d)

    def set_txseed(self, vkdic=None, bdic=None):
        ''' pick/return a kn as seed, in vkdic with shortest dic, and
            also popular
            '''
        perf_count["set_txseed"] += 1
        initial = vkdic == None
        if initial:
            lst = list(self.vkdic.keys())
            bdic = self.dic
        else:
            L = 4     # bigger than any klause length, so it will bereplaced
            lst = []  # list of kns with the same shortest length
            for kn in vkdic:
                if vkdic[kn].nob <= L:
                    L = vkdic[kn].nob
                    # remove kns in lst with length > L
                    i = 0
                    while i < len(lst):
                        if self.vkdic[lst[i]].nob > L:
                            lst.pop(i)
                        else:
                            i += 1
                    lst.append(kn)
        if len(lst) == 0:
            x = 1
            return None, None
        popular_kns, top_bit = self.most_popular(bdic)
        for kn in lst:
            if kn in popular_kns:
                return kn, top_bit
        return lst[0], top_bit
    # ==== end of def set_txseed(self, vkdic=None, bdic=None)

    def add_vklause(self, vk=None):  # add vklause vk into bit-dict
        perf_count["add_vklause"] += 1

        def add_vk(self, vkn):
            vclause = self.vkdic[vkn]
            length = len(vclause.dic)
            lst = self.ordered_vkdic.setdefault(length, [])
            if vkn not in lst:
                lst.append(vclause.kname)
            if length == 0:
                # when klause is empty, it is in every bit-value
                for b in self.dic:
                    self.dic[b][0].append(vkn)
                    self.dic[b][1].append(vkn)
            else:
                for bit, v in vclause.dic.items():
                    # bit: bit-position, v: 0 or 1
                    # lst: [[<0-valued cs>],[<1-cs>]]
                    lst = self.dic.get(bit, [[], []])
                    if vkn not in lst[v]:  # v is bit-value: 0 or 1
                        # put vkn in 0-list, or 1-list
                        lst[v].append(vkn)
                return vclause
        # ---- end of def add_vk(self, vkn):

        if vk:
            return add_vk(self, vk)
        else:
            for vkn in self.vkdic:
                add_vk(self, vkn)
            return self
    # ==== end of def add_vklause(self, vk=None)

    def visualize(self):
        self.vis.output(self)


if __name__ == '__main__':
    ''' python bitdic.py config1.json 3
        this will cut between bit3 and bit-4, and output 2 sub-config files:
        config1-7-4.json and config1-3-0.json
        sitting on bit [7,6,5,4] and [3,2,1,0]
        '''
    import sys
    if len(sys.argv) == 3:
        infile_name = sys.argv[1]
        hbit = int(sys.argv[2])
        namebase = infile_name.split('.')[0]
    else:
        infile_name = 'config20_80.json'
        hbit = 10
        # infile_name = 'config1.json'
        # hbit = 3

    namebase = infile_name.split('.')[0]

    sdic = get_sdic(f'./configs/{infile_name}')
    topbit = sdic['nov'] - 1
    tlowbit = hbit + 1

    vkdic = make_vkdic(sdic['kdic'], sdic['nov'])
    bitdic = BitDic('test', 'test-name', vkdic, sdic['nov'])
    bitdic0 = bitdic.subset(hbit)
    bitdic1 = bitdic.subset(topbit, tlowbit)
    fn0 = f'{namebase}-{hbit}-0.json'
    fn1 = f'{namebase}-{topbit}-{tlowbit}.json'
    print(f'outputing: {fn0}  {fn1}')
    bitdic0.vis.output_config_file(bitdic0.vkdic, bitdic0.nov, fn0)
    bitdic1.vis.output_config_file(bitdic1.vkdic, bitdic1.nov, fn1)

    x = 1
