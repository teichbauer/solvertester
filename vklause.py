def get_bit(val, bit):
    return (val >> bit) & 1


def set_bit(val, bit_index, new_bit_value):
    """ Set the bit_index (0-based) bit of val to x (1 or 0)
        and return the new val.
        """
    mask = 1 << bit_index  # mask - integer with just hte chosen bit set.
    val &= ~mask           # Clear the bit indicated by the mask (if x == 0)
    if new_bit_value:
        val |= mask        # If x was True, set the bit indicated by the mask.
    return val             # Return the result, we're done.


def set_bits(val, d):
    for b, v in d.items():
        val = set_bit(val, b, v)
    return val


class VKlause:
    ''' veriable klause - klause with 1, 2 or 3 bits.
        nov is the value-space bit-count, or number-of-variables
        bits is a list of bits in ascending order
        '''
    # nov not used - remove it?

    def __init__(self, kname, dic, nov):
        self.kname = kname
        self.dic = dic  # { 7:1, 3: 0, 0: 1}, or {3:0, 1:1} or {3:1}
        self.nov = nov  # number of variables (here: 8) - bits of value space
        # all bits, in descending order
        self.bits = sorted(list(dic.keys()), reverse=True)  # [7,3,0]
        # void bits of the nov-bits
        bs = list(range(nov))
        self.nbits = [b for b in bs if b not in self.bits]  # [1,2,4,5,6]
        self.nob = len(self.bits)             # 1, 2 or 3
        self.set_filter_and_mask()
        self.completion = 'tt'  # can be: p1 (1 from 3), or p2 (2 of 3)

    def set_completion(self, cmpl):
        self.completion = cmpl

    def clone(self, drop_bits=[], lowbit=0):
        # drop_bits: list of bits to be dropped
        # lowbit: the new bit-0
        dic = self.dic.copy()
        for b in drop_bits:
            if b in dic:
                dic.pop(b, None)
        if lowbit > 0:
            d = {}
            for b in dic:
                d[b % lowbit] = dic[b]
            dic = d
        return VKlause(self.kname, dic, self.nov)

    def hit_values_nov3(self):
        if self.nov == 3:
            hvs = []
            if self.nob == 0:          # vklause.dic = {}
                return list(range(8))  # all 8 values are hit
            elif self.nob == 3:
                hvs.append(self.mask)
            elif self.nob == 2:
                # filter ca be: 3(011), 5(101), 6(110)
                # the 0-bit can take 0 or 1 as value
                # 2 hit-values are there
                if self.filter == 3:
                    hvs = [self.mask, 4 + self.mask]
                elif self.filter == 5:
                    hvs = [self.mask, 2 + self.mask]
                elif self.filter == 6:
                    hvs = [self.mask, 1 + self.mask]
                else:
                    raise('error in VKlause.hit_value_nov3 - 0')
            elif self.nob == 1:
                # filter can be: 1/001, 2/010, 4/100
                # the 0-bit can take 0 or 1 as value
                # 4 hit-values are there
                if self.filter == 1:    # filter: 001, mask = 000 or 001
                    hvs = [
                        self.mask,      # self.mask = m
                        self.mask + 2,  # 01m
                        self.mask + 4,  # 10m
                        self.mask + 6   # 11m
                    ]
                elif self.filter == 2:  # filter: 010, mask = 000 or 010
                    hvs = [
                        self.mask,      # self.mask = m: 0m0
                        self.mask + 1,  # 0m1
                        self.mask + 4,  # 1m0
                        self.mask + 5   # 1m1
                    ]
                elif self.filter == 4:  # filter: 100, mask = 000 or 100
                    hvs = [
                        self.mask,      # self.mask = m00
                        self.mask + 1,  # m01
                        self.mask + 2,  # m10
                        self.mask + 3   # m11
                    ]
            return hvs
        else:
            raise('error in VKlause.hit_value_nov3 - 1')

    def set_filter_and_mask(self):
        ''' For the example klause {7:1, 5:0, 2:1}
                              BITS:   7  6  5  4  3  2  1  0
            the relevant bits:        *     *        *
                        self.filter:  1  0  1  0  0  1  0  0
            surppose v = 135 bin(v):  1  0  0  0  0  1  1  1
            x = v AND filter =        1  0  0  0  0  1  0  0
            bits of v left(rest->0):  ^     ^        ^
                        self.mask  :  1  0  0  0  0  1  0  0
            This method set self.filter
            '''
        filter = 0
        mask = 0
        for k, v in self.dic.items():
            filter = filter | (1 << k)
            if v == 1:
                mask = mask | (1 << k)
        self.mask = mask
        self.filter = filter

    def value(self):
        return self.mask

    def position_value(self):
        ''' regardless v be 0 or 1, set the bit 1
            For I am caring only the position of the bits  '''
        return self.filter

    def hit(self, v):  # hit means here: v let this klause turn False
        fv = self.filter & v
        return not bool(self.mask ^ fv)

    def hit_valuelist(self):
        hits = []
        nbs = sorted(self.nbits, reverse=True)
        L = len(nbs)
        for x in range(2**L):
            d = {}
            for i in range(L):
                d[nbs[i]] = get_bit(x, i)
            hits.append(set_bits(self.mask, d))
        return hits


def hit_values():
    d = {5: 1, 3: 0, 2: 1}
    vk = VKlause('name', d, 6)
    hits = vk.hit_valuelist()


def test_hit_values_nov3():
    dics = [
        {2: 0, 1: 0, 0: 0},  # hvs: [0]
        {2: 1, 1: 0, 0: 0},  # hvs: [4]
        {2: 0, 1: 1, 0: 0},  # hvs: [2]
        {2: 0, 1: 1, 0: 1},  # hvs: [3]
        {2: 0, 1: 0},       # hvs: [0,1]
        {2: 1, 1: 0},       # hvs: [4,5]
        {2: 1, 1: 1},       # hvs: [6,7]
        {2: 0, 1: 1},       # hvs: [2,3]
        {2: 0},   # hvs: [1,2,3,4]
        {2: 1},   # hvs: [4,5,6,7]
        {1: 0},   # hvs: [1,3,5,7]
        {1: 1},   # hvs: [1,3,5,7]
        {0: 0},   # hvs: [1,3,5,7]
        {0: 1}    # hvs: [1,3,5,7]
    ]
    for dic in dics:
        vk = VKlause('test-vk', dic, 3)
        hvs = vk.hit_values_nov3()
        dic_str = str(dic)
        hvs_str = str(hvs)
        print(f'dic: {dic_str}: {hvs_str}')
        x = 1


if __name__ == '__main__':
    # test_hit_values_nov3()
    hit_values()
