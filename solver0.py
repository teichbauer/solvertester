import sys


class Klause:
    def __init__(self, cname, clause):
        '''  clause example: {7:1, 5:0, 2:1}  '''
        self.name = cname
        self.clause = clause
        self.set_filter_and_mask()

    def set_filter_and_mask(self):
        # For the example klause {7:1, 5:0, 2:1}
        '''               BITS:   7  6  5  4  3  2  1  0
        the relevant bits:        *     *        *
        {7:1, 5:0, 2:1}'s filter: 1  0  1  0  0  1  0  0
        surppose v = 135 bin(v):  1  0  0  0  0  1  1  1
        x = v AND filter =        1  0  0  0  0  1  0  0
        bits of v left(rest->0):  ^     ^        ^
        {7:1, 5:0, 2:1}' mask  :  1  0  0  0  0  1  0  0
        This methos set self.filter
        '''
        filter = 0
        mask = 0
        for k, v in self.clause.items():
            filter = filter | (1 << k)
            if v == 1:
                mask = mask | (1 << k)
        self.mask = mask
        self.filter = filter

    def hit(self, v):
        '''
        first only let the relevant 3 bits from v remain -> fv
        mask ^ fv : (False: unsat, or hit by the mask, True: not hit, or SAT)
        return the reverse of this
        '''
        fv = self.filter & v
        return not bool(self.mask ^ fv)


class Solver0:
    def __init__(self, sdic):
        self.nov = sdic['nov']
        self.N = 2 ** self.nov
        kdic = sdic['kdic']
        self.klauses = {kn: Klause(kn, kl) for kn, kl in kdic.items()}
        self.sats = []
        self.hit_dic = self.gen_coverage()

    def gen_coverage(self):
        dic = {}
        for v in range(self.N):
            clst = []
            for kn, kl in self.klauses.items():
                if kl.hit(v):
                    clst.append(kn)
                clst.sort()
            dic[v] = clst
            if len(clst) == 0:
                self.sats.append(v)
        return dic

    def gen_bin(self, v):
        m = bin(v)[2:].zfill(8)
        lst = [e for e in m]
        return '  '.join(lst)

    def output(self, fname):
        fil = open('./verify/' + fname, 'w')
        msg = f'sats: {self.sats}'
        fil.write(msg + '\n')
        print(msg)
        header = '------ 7  6  5  4  3  2  1  0 -------\n'
        fil.write(header)
        for v in range(self.N):
            vkey = str(v).zfill(5)
            vbin = self.gen_bin(v)
            cover = ' '.join(self.hit_dic[v])
            line = f'{vkey}: {vbin} $ {cover}'
            fil.write(line + '\n')
        fil.close()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f'python solver0.py <conf-file-name>')
        config_file_name = 'config8_38.json'
    else:
        config_file_name = sys.argv[1]
    da = open(f'configs/'+config_file_name).read()
    sdic = eval(da)
    solver0 = Solver0(sdic)
    outfile_name = config_file_name.split('.')[0] + '.txt'
    solver0.output(outfile_name)
