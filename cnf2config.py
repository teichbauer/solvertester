# -----------------------------------------------------------------------------
#  convert a cnf file from under ./data/* to a <fn>.json file with all clauses
# in the following format.
# The example has  <number of variables> = 8, <number of clauses>: 38
# {
#    "nov": <>,
#    "kdic": {
#       "C0001": {7: 0, 5: 1, 0: 0},  # highst bit: 7,set to 1, bit-0 set to 0
#       "C0002": {...},
#       ...
#       "C0038": {...}
#    }
# }
# ============================================================================
import sys
from verifyconfig import verify
from visualizer import Visualizer

def readfile(file_name):
    fil = open('data/' + file_name)
    lines = fil.readlines()
    nov = -1
    nok = -1
    clines = []
    for line in lines:
        if line.startswith('c'):
            continue
        elif line.startswith('p'):
            splt = line.split()
            nov = int(splt[2])
            nok = int(splt[-1])
        else:
            if line.startswith('%'):
                break
            splt = line.split()
            clines.append(tuple(splt[:3]))
    return nov, nok, clines


def print2file(sdic, filename):
    from pprint import pprint
    with open(filename, 'wt') as out:
        pprint(sdic, stream=out)


def make_sdic(nov, cls):
    kcount = 0
    sdic = {"nov": nov, "kdic": {}}
    for tup in cls:
        kcount += 1
        kname = 'C' + str(kcount).zfill(4)
        dic = {}
        for t in tup:
            i = int(t)
            bit = abs(i) - 1
            if i < 0:
                dic[bit] = 1
            else:
                dic[bit] = 0
        sdic["kdic"][kname] = dic
    return sdic


def verify_and_make_config(sdic, fnamebase):
    nov = sdic['nov']
    nok = len(sdic['kdic'])
    ok, kn, kn0 = verify(sdic['kdic'], sdic['nov'])
    if ok:
        fname = f'./configs/{fnamebase}'
        print2file(sdic, fname)
        print(f'{fname}  has been generated.')
    else:
        if kn0 == None:
            nov = sdic['nov']
            print(f'bit number higher than {nov}')
        else:
            print(f'{kn} and {kn0} are duplicates')


if __name__ == '__main__':
    fname = sys.argv[1]
    nv, nk, clines = readfile(fname)
    sdic = make_sdic(nv, clines)
    fnamebase = fname.split('.')[0]
    verify_and_make_config(sdic, fnamebase)
