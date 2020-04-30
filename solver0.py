import sys
from klause import Klause
import time

_time_count = 0.0


class Solver0:
    def __init__(self, sdic, stop=False):
        self.nov = sdic['nov']
        self.N = 2 ** self.nov
        self.stop = stop   # stops when first sat hit
        kdic = sdic['kdic']
        self.klauses = {kn: Klause(kn, kl) for kn, kl in kdic.items()}
        self.kns = list(self.klauses.keys())
        self.sats = []

    def solve(self):
        sats = []
        for v in range(self.N):
            hit = False
            for kn in self.kns:
                hit = self.klauses[kn].hit(v)
                if hit:
                    break
            if not hit:
                sats.append(v)
        return sats

    def gen_coverage(self, stop=False):
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
                if stop:
                    return {v: 'SAT'}
        return dic

    def gen_bin(self, v):
        m = bin(v)[2:].zfill(8)
        lst = [e for e in m]
        return '  '.join(lst)

    def output2file(self, fname):
        self.hit_dic = self.gen_coverage(self.stop)
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
    _time_count = time.time()
    printout = False
    if len(sys.argv) == 3:
        printout = True
    if len(sys.argv) < 2:
        print(f'python solver0.py <conf-file-name>')
        config_file_name = 'config8_38.json'
    else:
        config_file_name = sys.argv[1]
    da = open(f'configs/'+config_file_name).read()
    sdic = eval(da)
    solver0 = Solver0(sdic, printout)
    if printout:
        outfile_name = config_file_name.split('.')[0] + '.txt'
        solver0.output2file(outfile_name)
    else:
        sats = solver0.solve()
        length = len(sats)
        print(f'{length} sats found: {sats}')
        time_used = time.time() - _time_count
        print(f'time used: {time_used}')
